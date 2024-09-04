import asyncio
import json
import os
from typing import Set
from uuid import uuid4

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from kafka import TopicPartition


class KafkaServer:
    def __init__(self):
        self.loop = None
        self.partitions = None
        self.consumer = None
        self.producer = None

        # env variables
        self.KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'test')
        self.KAFKA_CONSUMER_GROUP_ID = os.getenv('KAFKA_CONSUMER_GROUP_ID', 'group_id')
        self.KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

    async def initialize(self):
        self.loop = asyncio.get_running_loop()

        group_id = f'{self.KAFKA_CONSUMER_GROUP_ID}'
        self.consumer = AIOKafkaConsumer(self.KAFKA_TOPIC,
                                         loop=self.loop,
                                         bootstrap_servers=self.KAFKA_BOOTSTRAP_SERVERS,
                                         group_id=group_id)
        # get consumer
        await self.consumer.start()
        # get producer
        self.producer = AIOKafkaProducer(loop=self.loop, bootstrap_servers=self.KAFKA_BOOTSTRAP_SERVERS)
        await self.producer.start()
        # get cluster layout and initial topic/partition leadership information
        self.partitions: Set[TopicPartition] = self.consumer.assignment()

        for tp in self.partitions:
            # get the log_end_offset
            end_offset_dict = await self.consumer.end_offsets([tp])
            end_offset = end_offset_dict[tp]

            if end_offset == 0:
                return

            self.consumer.seek(tp, end_offset - 1)
            msg = await self.consumer.getone()
            return

    async def produce(self, message):
        value = {'message_id': str(uuid4()), 'message': message}
        value_json = json.dumps(value).encode('utf-8')
        await self.producer.send_and_wait(self.KAFKA_TOPIC, value_json)

    async def consume(self):
        msg = await self.consumer.getone()
        return msg
