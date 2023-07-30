
from abc import ABC, abstractmethod


class FunctionModule(ABC):
    """
    Provides interface for providing functions to OpenAI
    """
    def __init__(self, service_provider):
        self._service_provider = service_provider

    @abstractmethod
    def get_funcs(self):
        """
        Gets the function dictionary
        """

    @abstractmethod
    def get_function_descriptions(self):
        """
        Gets the function descriptors
        """
