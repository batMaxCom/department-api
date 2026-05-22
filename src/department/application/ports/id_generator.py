from abc import ABC, abstractmethod


class IntegerIdGenerator(ABC):
    @abstractmethod
    async def next_id(self) -> int:
        """Return the next integer id"""