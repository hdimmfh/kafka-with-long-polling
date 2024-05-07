import asyncio
import json
import os
from random import randint
from typing import Any, Set

import aiokafka
from aiokafka import AIOKafkaProducer
from kafka import TopicPartition


class KafkaServer:
    def __init__(self, log):
        self.log = log
        self.loop = asyncio.get_event_loop()
        self.partitions = None
        self.consumer = None
        self._state = 0

        # env variables
        self.KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
        self.KAFKA_CONSUMER_GROUP_ID = os.getenv('KAFKA_CONSUMER_GROUP_ID', 'group_id')
        self.KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

    async def initialize(self):
        group_id = f'{self.KAFKA_CONSUMER_GROUP_ID}'
        self.log.info(f'Initializing KafkaConsumer for topic {self.KAFKA_TOPIC}, group_id {group_id}'
                      f' and using bootstrap servers {self.KAFKA_BOOTSTRAP_SERVERS}')
        self.consumer = aiokafka.AIOKafkaConsumer(self.KAFKA_TOPIC,
                                                  loop=self.loop,
                                                  bootstrap_servers=self.KAFKA_BOOTSTRAP_SERVERS,
                                                  group_id=group_id)
        # get consumer
        # get cluster layout and join group
        await self.consumer.start()
        # get cluster layout and initial topic/partition leadership information
        # get producer
        self.producer = AIOKafkaProducer(loop=self.loop, bootstrap_servers=self.KAFKA_BOOTSTRAP_SERVERS)
        await self.producer.start()

        self.partitions: Set[TopicPartition] = self.consumer.assignment()
        nr_partitions = len(self.partitions)
        if nr_partitions != 1:
            self.log.warning(f'Found {nr_partitions} partitions for topic {self.KAFKA_TOPIC}. Expecting '
                             f'only one, remaining partitions will be ignored!')

        for tp in self.partitions:
            # get the log_end_offset
            end_offset_dict = await self.consumer.end_offsets([tp])
            end_offset = end_offset_dict[tp]

            if end_offset == 0:
                self.log.warning(f'Topic ({self.KAFKA_TOPIC}) has no messages (log_end_offset: '
                                 f'{end_offset}), skipping initialization ...')
                return

            self.log.debug(f'Found log_end_offset: {end_offset} seeking to {end_offset - 1}')
            self.consumer.seek(tp, end_offset - 1)
            msg = await self.consumer.getone()
            self.log.info(f'Initializing API with data from msg: {msg}')

            # update the API state
            self._update_state(msg)
            return

    def _update_state(self, message: Any) -> None:
        # JSON decoding, variable 'message.value' is expected like {"state" : 0} form.
        value = json.loads(message.value)
        self._state = value['state']

    async def send(self, message):
        # produce message
        msg_id = f'{randint(1, 10000)}'
        # message contents
        value = {'message_id': msg_id, 'message': message, 'state': 200}
        value_json = json.dumps(value).encode('utf-8')
        await self.producer.send_and_wait(self.KAFKA_TOPIC, value_json)

    async def get(self):
        msg = await self.consumer.getone()
        return msg
