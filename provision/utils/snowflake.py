import time
import threading
from django.utils.functional import LazyObject


class SnowflakeGenerator:
    def __init__(self, datacenter_id=1, worker_id=1, epoch=1288834974657):
        self.datacenter_id = datacenter_id
        self.worker_id = worker_id
        self.epoch = epoch
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = threading.Lock()

        # bit allocation
        self.worker_bits = 5
        self.datacenter_bits = 5
        self.sequence_bits = 12

        self.max_worker_id = -1 ^ (-1 << self.worker_bits)
        self.max_datacenter_id = -1 ^ (-1 << self.datacenter_bits)
        self.max_sequence = -1 ^ (-1 << self.sequence_bits)

        self.worker_shift = self.sequence_bits
        self.datacenter_shift = self.sequence_bits + self.worker_bits
        self.timestamp_shift = self.sequence_bits + self.worker_bits + self.datacenter_bits

    def _current_millis(self):
        return int(time.time() * 1000)

    def _wait_next_millis(self, last_timestamp):
        ts = self._current_millis()
        while ts <= last_timestamp:
            ts = self._current_millis()
        return ts

    def generate(self):
        with self.lock:
            ts = self._current_millis()
            if ts < self.last_timestamp:
                ts = self._wait_next_millis(self.last_timestamp)

            if ts == self.last_timestamp:
                self.sequence = (self.sequence + 1) & self.max_sequence
                if self.sequence == 0:
                    ts = self._wait_next_millis(self.last_timestamp)
            else:
                self.sequence = 0

            self.last_timestamp = ts
            value = (
                ((ts - self.epoch) << self.timestamp_shift)
                | (self.datacenter_id << self.datacenter_shift)
                | (self.worker_id << self.worker_shift)
                | self.sequence
            )
            return str(value)  # 🔑 ép sang string luôn


# Singleton
class LazySnowflake(LazyObject):
    def _setup(self):
        self._wrapped = SnowflakeGenerator()


snowflake = LazySnowflake()
