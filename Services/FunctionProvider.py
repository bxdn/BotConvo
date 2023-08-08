
from oai_functions.time_funcs import TimeFuncs


class FunctionProvider:
    """
    Provides functions for OpenAI to use
    """
    def __init__(self, service_provider):
        self._FUNCTION_MODULES = [
            TimeFuncs(service_provider)
        ]

    def get_functions(self):
        """
        Gets the dictionary of all function names to function definitions in function modules
        """
        funcs = {}
        for module in self._FUNCTION_MODULES:
            funcs = {**funcs, **module.get_funcs()}
        return funcs

    def get_function_descriptions(self):
        """
        Gets the descriptions of all functions in function modules
        """
        descriptions = []
        for module in self._FUNCTION_MODULES:
            descriptions += module.get_function_descriptions()
        return descriptions
