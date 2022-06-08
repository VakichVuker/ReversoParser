import requests
from bs4 import BeautifulSoup
from TranslatorExceptions import BadConnectionException, WrongWordException, UndefinedLanguageException


class Translator:
    translate_variants = {
        "1": "Arabic",
        "2": "German",
        "3": "English",
        "4": "Spanish",
        "5": "French",
        "6": "Hebrew",
        "7": "Japanese",
        "8": "Dutch",
        "9": "Polish",
        "10": "Portuguese",
        "11": "Romanian",
        "12": "Russian",
        "13": "Turkish"
    }

    def __init__(self, word_to_translate, language_from, language_to):
        self.word_to_translate = word_to_translate
        self.language_from = language_from
        self.language_to = language_to
        self.translated_word = list()
        self.examples_sentence = list()

    def __str__(self):
        word_before = Translator.translate_variants[self.language_to] + ' '
        header1 = word_before + 'Translations:\n'
        word = self.translated_word[0][0] + ' ' + self.translated_word[0][1] + '\n\n'
        header2 = word_before + 'Example:\n'
        example = f'{self.examples_sentence[0][0]}\n{self.examples_sentence[0][1]}\n\n\n'
        return header1 + word + header2 + example

    def translate(self):
        headers = {'User-Agent': 'Mozilla/5.0'}
        language_pair = str(Translator.translate_variants[self.language_from] + '-' + Translator.translate_variants[self.language_to]).lower()
        url = 'https://context.reverso.net/translation/{}/{}' .format(language_pair, self.word_to_translate)
        page = requests.get(url, headers=headers)
        if page.status_code != 200 and page.status_code != 404:
            print(page.status_code)
            raise BadConnectionException
        soup = BeautifulSoup(page.content, 'html.parser')
        translated_word_range_soup = soup.find_all('span', {'class': "display-term"})
        if len(translated_word_range_soup) == 0:
            raise WrongWordException(self.word_to_translate)
        all_translated_words = [word.text for word in translated_word_range_soup].copy()

        words_with_gender = dict()
        all_a = soup.find_all('a')
        for a_tag in all_a:
            word_in_a = a_tag.find('span', {'class': "display-term"})
            gender_in_a = a_tag.find('span', {'class': "gender"})
            if word_in_a and gender_in_a:
                words_with_gender[word_in_a.text] = gender_in_a.text

        list_word_with_gender = [name for name, _ in words_with_gender.items()]
        for translated_word in all_translated_words:
            if translated_word in list_word_with_gender:
                word_to_add = [translated_word, words_with_gender[translated_word]]
            else:
                word_to_add = [translated_word, '']
            self.translated_word.append(word_to_add)

        range_examples = soup.find_all('div', {'class': "example"})
        list_in_every_range = [example.find_all('span', {'class': "text"}) for example in range_examples]
        self.examples_sentence = Translator.soup_lists_to_text_list(list_in_every_range).copy()

    def print_all_examples_and_all_word(self):
        word_before = Translator.translate_variants[self.language_to] + ' '
        print('\n' + word_before + 'Translations:')
        for word in self.translated_word:
            print(word)
        print('\n' + word_before + 'Examples:')
        for block_example in self.examples_sentence:
            print(f'{block_example[0]}\n{block_example[1]}\n')

    def print_one_example_and_word(self):
        word_before = Translator.translate_variants[self.language_to] + ' '
        print('\n' + word_before + 'Translations:')
        print(self.translated_word[0])
        print('\n' + word_before + 'Example:')
        print(f'{self.examples_sentence[0][0]}\n{self.examples_sentence[0][1]}\n')

    @staticmethod
    def print_all_enabled_languages():
        for num, language in Translator.translate_variants.items():
            print(f'{num}. {language}')

    @staticmethod
    def define_num_lang(name_lang):
        result = None
        if name_lang == 'all':
            result = '0'
        else:
            for num, language in Translator.translate_variants.items():
                if str(language).lower() == name_lang:
                    result = num
                    break
        if result is None:
            raise UndefinedLanguageException(name_lang)
        return result

    @staticmethod
    def soup_lists_to_text_list(list_of_lists):
        res_list = list()
        for list_range in list_of_lists:
            one_block = list()
            for one_finding in list_range:
                correct_string = one_finding.text
                one_block.append(" ".join(correct_string.split()))
            res_list.append(one_block)
        return res_list
