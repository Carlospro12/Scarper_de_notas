from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta, date
from airflow.models import Variable
from airflow import DAG
import lxml.html as html
import requests
import os


HOME_URL = Variable.get('home_url')
SLACK_WEBHOK = Variable.get('slack_webhook')
FILE_PATH_OUTPUT = '/home/airflow/gcs/data/output/'

XPATH_LINK_TO_ARTICLE = '//text-fill/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/h2/span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/descendant-or-self::*/text()'


def parse_notice(link,today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\n','')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            with open(f'{FILE_PATH_OUTPUT+today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    if p.endswith('.'):
                        f.write(p)
                        f.write('\n')
                    else: 
                        f.write(p)

        else:
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:
        print(ve)


def parse_home(**kwargs):
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)

            today = date.today().strftime('%d-%m-%Y')

            if not os.path.isdir(FILE_PATH_OUTPUT+today):
                os.mkdir(FILE_PATH_OUTPUT+today)
            
            for link in links_to_notices:
                parse_notice(link,today)
            
            num_notes = len(os.listdir(FILE_PATH_OUTPUT+today))

        else: 
            raise ValueError(f'Error: {response.status_code}')
        
    except ValueError as ve:
        print(ve)

    kwargs['ti'].xcom_push(key='number_of_notes', value=num_notes)

def send_msg(**kwargs):
    number_of_notes = kwargs['ti'].xcom_pull(key='number_of_notes', task_ids=['parse_home'])[0]
    text = f"""
---------------------------------------------   
{number_of_notes} notas listas para ser analisadas.
---------------------------------------------
    """
    requests.post(SLACK_WEBHOK, json = {'text':text})

# --------------------------------
# DAG definition
# --------------------------------

# Define the defualt args
default_args = {
    'owner': 'Carlos Estevez',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 31),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'provide_context': True}

# Create the DAG object
with DAG(
    dag_id='scraper',
    description='extrae las notas del diario y envia una alerta cuando ha finalizado',
    schedule_interval= '0 12 * * *',
    default_args = default_args,
    catchup=True
) as scraper:
    t1 = PythonOperator(task_id='parse_home',
                        python_callable=parse_home)
    t2 = PythonOperator(task_id='send_msg',
                        python_callable=send_msg)
# Set the dependencies
    t1 >> t2  

