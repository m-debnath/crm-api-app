import json

from django.conf import settings
from kafka_logger.handlers import KafkaLoggingHandler


class MyKafkaLoggingHandler(KafkaLoggingHandler):
    def __init__(self):
        super().__init__(
            settings.KAFKA_BOOTSTRAP_SERVERS,
            settings.KAFKA_TOPIC,
            security_protocol="PLAINTEXT",
            kafka_producer_init_retries=settings.KAFKA_PRODUCER_INIT_RETRIES,
            flush_buffer_size=settings.KAFKA_FLUSH_BUFFER_SIZE,
            flush_interval=settings.KAFKA_FLUSH_INTERVAL,
        )

    def prepare_record_dict(self, record):
        return json.loads(record.getMessage())
