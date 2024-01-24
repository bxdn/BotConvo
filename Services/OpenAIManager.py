
from json import loads

import openai


class OpenAIManager:
    """
    Manages OpenAI API communications
    """

    def __init__(self, settings, service_provider):
        openai.organization = "org-mvUlF4kJZ6gVdyLaeZeNMDx7"
        openai.api_key = settings.OAI_API_KEY

        self._MAX_TOKENS = settings.get('oai', default={}).get('max_tokens', default=150)
        self._TEMPERATURE = settings.get('oai', default={}).get('temperature', default=1)
        self._TOP_P = settings.get('oai', default={}).get('top_p', default=1)

        self._use_funcs = settings.get('use_funcs')

        self._service_provider = service_provider

        print('OpenAI Ready...')

    @staticmethod
    def transcribe(audio_file):
        """
        Transcribes an audio file
        :param audio_file: The audio file to transcribe
        :return: The transcription
        """
        return openai.Audio.transcribe("whisper-1", audio_file)['text']

    def get_response(self, messages, phrase_callback):
        """
        Gets a response from GPT
        :return: The response string
        """
        chat_completion = self._make_completion(messages)
        message, function_call = _OutputParser().handle_completion(chat_completion, phrase_callback)
        function_output = ''
        if function_call['name'] and self._use_funcs:
            function_output = self._make_function_call(function_call)
        return message, function_call['name'], function_output

    def _make_function_call(self, function_call):
        args = loads(function_call['arguments'])
        function = self._service_provider.function_service().get_functions()[function_call['name']]
        return function(args)

    def _make_completion(self, messages):
        kwargs = {
            'model': 'gpt-3.5-turbo',
            'max_tokens': self._MAX_TOKENS,
            'temperature': self._TEMPERATURE,
            'top_p': self._TOP_P,
            'messages': messages,
            'stream': True
        }
        if self._use_funcs:
            descs = self._service_provider.function_service().get_function_descriptions()
            return openai.ChatCompletion.create(**kwargs, functions=descs)
        else:
            return openai.ChatCompletion.create(**kwargs)


class _OutputParser:

    def __init__(self):
        self._total_output = ''
        self._total_function_name = ''
        self._total_function_args = ''
        self._current_output = ''

    def handle_completion(self, completion, phrase_callback):
        """
        Handles the output of an OpenAI response
        """
        for chunk in completion:
            self._handle_chunk(chunk, phrase_callback)
        return self._total_output, {'name': self._total_function_name, 'arguments': self._total_function_args}

    def _handle_chunk(self, chunk, phrase_callback):
        delta = chunk['choices'][0]['delta']
        partial_message = delta.get('content')
        if partial_message:
            self._total_output += partial_message
        function_call = delta.get('function_call')
        if function_call:
            self._handle_function_call(function_call)
        current_output_addition, start_of_next_phrase = self._split_response(partial_message)
        self._current_output += current_output_addition
        if start_of_next_phrase is not None:
            phrase_callback(self._current_output)
            self._current_output = start_of_next_phrase

    def _handle_function_call(self, function_call):
        if function_call.get('name'):
            self._total_function_name += function_call['name']
        if function_call.get('arguments'):
            self._total_function_args += function_call['arguments']

    def _split_response(self, message):  # Splits partial message into 2 strings based on sentence separators
        if not message:
            return '', None
        last_idx = max(
            self._get_last_idx(message, '.'),
            self._get_last_idx(message, '?'),
            self._get_last_idx(message, '!')
        )
        if last_idx < 0:
            return message, None
        return message[:last_idx + 1], message[last_idx + 1:]

    @staticmethod
    def _get_last_idx(string, char):
        return string.rindex(char) if char in string else -1
