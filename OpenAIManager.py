from json import loads

import openai
from OpenAIFunctions import functions, function_descriptions


class OpenAIManager:
    """
    Manages OpenAI API communications
    """
    def __init__(self, settings):
        openai.organization = "org-mvUlF4kJZ6gVdyLaeZeNMDx7"
        openai.api_key = settings.OAI_API_KEY

        self._MAX_TOKENS = settings.get('oai', default={}).get('max_tokens', default=150)
        self._TEMPERATURE = settings.get('oai', default={}).get('temperature', default=1)
        self._TOP_P = settings.get('oai', default={}).get('top_p', default=1)

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
        chat_completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',  # 'gpt-4'
            max_tokens=self._MAX_TOKENS,
            temperature=self._TEMPERATURE,
            top_p=self._TOP_P,
            messages=messages,
            stream=True,
            functions=function_descriptions
        )
        total_output = ''
        total_function = {'name': '', 'arguments': ''}
        current_output = ''
        first = True
        for chunk in chat_completion:
            current_output, new_phrase, first, partial_func = self._handle_chunk(chunk, current_output, phrase_callback, first)
            total_output += new_phrase
            total_function = {
                'name': total_function['name'] + partial_func['name'],
                'arguments': total_function['arguments'] + partial_func['arguments']
            }
        function_output = ''
        if total_function['name']:
            function_output = functions[total_function['name']](loads(total_function['arguments']))
        return total_output, total_function['name'], function_output

    def _handle_chunk(self, chunk, current_output, phrase_callback, first):
        delta = chunk['choices'][0]['delta']
        message_substr = delta.get('content')
        function_call = delta.get('function_call')
        if function_call:
            function_call = {
                'name': function_call.get('name') if function_call.get('name') else '',
                'arguments': function_call.get('arguments') if function_call.get('arguments') else ''
            }
        else:
            function_call = {'name': '', 'arguments': ''}
        to_append, new_output = self._split_response(message_substr)
        current_output += to_append
        full_phrase = ''
        if new_output is not None:
            phrase_callback(current_output, first)
            full_phrase = current_output
            current_output = new_output
            first = False
        return current_output, full_phrase, first, function_call

    def _split_response(self, message):
        """
        Cleans the response from ChatGPT
        :param choice: The choice object containing the message and reason for the message termination
        :return: The cleaned message
        """
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
        """
        Gets the last index of a character in a string, or -1 if it doesn't exist
        :param string: The string to search
        :param char: The char to search for
        :return: The last position of the character if it exists, otherwise -1
        """
        return string.rindex(char) if char in string else -1
