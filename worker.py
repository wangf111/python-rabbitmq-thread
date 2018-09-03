import pika
import json
from scraper import Scraper
from concurrent.futures import ThreadPoolExecutor
import time
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',datefmt='%Y-%m-%d')

parameters = pika.ConnectionParameters(host='localhost')
parameters.heartbeat = 5

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
tasks_queue = channel.queue_declare(queue='tasks.queue', durable=True)
scraping_result_queue = channel.queue_declare(queue='scrapingResult.queue', durable=True)
executor = ThreadPoolExecutor(10)

logging.info(' [*] Waiting for tasks. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print("callback start")
    executor.submit(calculate, body)


def calculate(body):
    url = json.loads(body)['url']
    scraper = Scraper()
    result = scraper.scrape(url.strip())
    time.sleep(10)
    j = json.dumps(result.__dict__)
    publish_result(j)


def publish_result(body):
    properties = pika.BasicProperties(content_type="application/json")
    channel.basic_publish(exchange='', routing_key='scrapingResult.queue', body=body, properties=properties)


channel.basic_consume(callback, queue='tasks.queue', no_ack=True)
channel.start_consuming()
