import re
import string
import pandas as pd
from rosette.api import API, RosetteException,DocumentParameters

class TextPreprocessor:
    def __init__(self, api_key=None, api_url=None):
            """
            Initialize the TextPreprocessor with optional Rosette API key and URL for transliteration.
            """
            self.api_key = api_key
            self.api_url = api_url
            self.rosette_api = API(user_key=api_key, service_url=api_url) if api_key else None

    def transliterate_part(self, text):
        """
        Transliterate a part of the text using the Rosette API.
        """
        try:
            params = DocumentParameters()
            params["content"] = text
            response = self.rosette_api.transliteration(params)
            return response.get('transliteration', text) 
        except RosetteException as e:
            print(f"Rosette API error: {e}")
            return text 

    def transliterate_input(self, input_sentence):
        """
        Transliterate an input sentence, handling both Arabic and Latin script.
        """
        if pd.isna(input_sentence): 
            return input_sentence

        # Regex to separate Arabic and Latin segments
        regex_split = re.compile(r'([\u0600-\u06FF]+|[a-zA-Z0-9 ]+)')
        parts = regex_split.findall(input_sentence)

        transliterated_parts = []
        for part in parts:
            if re.search(r"[\u0600-\u06FF]", part):  # Arabic script: keep as is
                transliterated_parts.append(part)
            else:  # Latin script: transliterate
                transliterated_parts.append(self.transliterate_part(part))

        return " ".join(transliterated_parts)

    @staticmethod
    def remove_diacritics(text):
        """
        Remove diacritics from the text.
        """
        diacritics = re.compile(r'[\u064B-\u0652]')
        return diacritics.sub('', text)

    @staticmethod
    def remove_punctuation(text):
        """
        Remove punctuation from the text.
        """
        return text.translate(str.maketrans('', '', string.punctuation))

    @staticmethod
    def reduce_repeated_characters(text):
        """
        Reduce repeated characters to a maximum of two occurrences.
        """
        return re.sub(r'(.)\1{2,}', r'\1\1', text)

    @staticmethod
    def clean_whitespace(text):
        """
        Strip leading/trailing whitespace and reduce multiple spaces to a single space.
        """
        return re.sub(r'\s+', ' ', text.strip())

    def preprocess(self, text,transliteration=False):
        """
        Apply all preprocessing steps to the given text.
        """
        if transliteration: 
            text = self.transliterate_input(text)
        text = self.remove_diacritics(text)
        text = self.clean_whitespace(text)
        text = self.reduce_repeated_characters(text)
        text = self.remove_punctuation(text)
        return text


