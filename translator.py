import sys
import requests

from ReversoTranslator import Translator
from TranslatorExceptions import BadConnectionException, WrongWordException, UndefinedLanguageException


def main():
    args = sys.argv
    try:
        language_from = Translator.define_num_lang(args[1])
        language_to = Translator.define_num_lang(args[2])
        word = args[3]
        translators = list()
        if language_to == '0':
            for num_language, _ in Translator.translate_variants.items():
                if num_language != language_from:
                    new_translator = Translator(word, language_from, num_language)
                    new_translator.translate()
                    print(str(new_translator), end='')
                    translators.append(new_translator)
        else:
            my_translator = Translator(word, language_from, language_to)
            my_translator.translate()
            translators.append(my_translator)
            # my_translator.print_all_examples_and_all_word()
            print(str(my_translator), end='')
        with open(word + '.txt', 'w', encoding='utf8') as f:
            for translator in translators:
                f.write(str(translator))
    except UndefinedLanguageException as err:
        print(err)
    except WrongWordException as err:
        print(err)
    except BadConnectionException as err:
        print(err)


if __name__ == '__main__':
    main()



