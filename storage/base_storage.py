from abc import ABC, abstractmethod


class Storage(ABC):

    @abstractmethod
    def fetch(self, *args, **kwargs):
        pass

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
