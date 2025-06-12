import csv
import io

class ListaCurso:
    def __init__(self, file):
        self.__file = file
        # Envolve o stream em um leitor de texto com codificação UTF-8
        text_stream = io.TextIOWrapper(file.stream, encoding='utf-8')
        reader = csv.DictReader(text_stream, delimiter=',')
        self.dicionario = list(reader)

    @property
    def file(self):
        return self.__file

