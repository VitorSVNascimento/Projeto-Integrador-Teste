class Curso:
    def __init__(self, nome: str, justificativa: str):
        self.nome = nome
        self.justificativa = justificativa

    def __repr__(self):
        return f"Curso(nome='{self.nome}', justificativa='{self.justificativa}')"

    def to_dict(self):
        return {
            "nome": self.nome,
            "justificativa": self.justificativa
        }
