class UndefinedLanguageException(Exception):
    def __init__(self, language):
        self.message = f'Sorry, the program doesn\'t support {language}'
        super().__init__(self.message)


class BadConnectionException(Exception):
    def __str__(self):
        return 'Something wrong with your internet connection'


class WrongWordException(Exception):
    def __init__(self, word):
        self.message = f'Sorry, unable to find {word}'
        super().__init__(self.message)
