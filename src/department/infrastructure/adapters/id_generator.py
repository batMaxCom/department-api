import asyncio
import time

from department.application.common.application_error import ApplicationError, ApplicationTypeError
from department.application.ports.id_generator import IntegerIdGenerator
from department.entrypoint.web.config import AppConfig


class IntegerIdGeneratorImpl(IntegerIdGenerator):
    """A class for generating unique identifiers. Snowflake technology."""

    def __init__(self, config: AppConfig) -> None:

        self.machine_id = config.machine_id

        self.sequence = 0
        self.last_timestamp = -1

        self.lock = asyncio.Lock()

        self.epoch = 1609459200000

        self.machine_id_bits = 10
        self.sequence_bits = 12

        self.max_sequence = (1 << self.sequence_bits) - 1

        self.machine_shift = self.sequence_bits
        self.timestamp_shift = self.sequence_bits + self.machine_id_bits

    @staticmethod
    def _current_millis() -> int:
        return int(time.time() * 1000)

    async def _wait_next_millis(self, last_timestamp: int) -> int:
        timestamp = self._current_millis()
        while timestamp <= last_timestamp:
            await asyncio.sleep(0)
            timestamp = self._current_millis()
        return timestamp

    async def next_id(self) -> int:
        async with self.lock:
            timestamp = self._current_millis()

            if timestamp < self.last_timestamp:
                raise ApplicationError(
                    type=ApplicationTypeError.APPLICATION,
                    message="Clock moved backwards."
                )
            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & self.max_sequence

                if self.sequence == 0:
                    timestamp = await self._wait_next_millis(self.last_timestamp)
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            return (
                ((timestamp - self.epoch) << self.timestamp_shift)
                | (self.machine_id << self.machine_shift)
                | self.sequence
            )
