class CursoResposta():
    def __init__(self,nome,descricao):
        self.__nome=nome
        self.__descricao=descricao

    @property
    def nome(self):
        return self.__nome
    
    @property
    def descricao(self):
        return self.__descricao

    @staticmethod
    def transforma_texto(linha:str):
        linha=linha.split("-")
        primeira_parte=linha[0]
        segunda_parte=linha[1]
        curso=CursoResposta(primeira_parte,segunda_parte)
        return curso
    
    def __str__(self):
        print(f'{self.nome} - {self.descricao}')
