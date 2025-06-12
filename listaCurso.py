import pandas as pd

class ListaCurso:
    def __init__(self, file):
        self.__file=file
        df=pd.read_csv(file,sep=',')
        self.dicionario=df.to_dict(orient='records')

    @property
    def file(self):
        return self.__file
