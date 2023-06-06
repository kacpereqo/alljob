from abc import ABC, abstractmethod


class OffertFactory(ABC):

    @abstractmethod
    def get_offerts() -> None:
        pass
