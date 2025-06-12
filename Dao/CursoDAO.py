from core.database import engine, SessionLocal, Base
from models.curso import Cursos

# 🏗 Cria as tabelas no banco, se ainda não existirem
def criar_tabelas():
    Base.metadata.create_all(bind=engine)

# ➕ Inserir um novo curso
def inserir_curso(nome, descricao):
    criar_tabelas()
    db = SessionLocal()
    try:
        novo = Cursos(nomecursos=nome, descricaocursos=descricao)
        db.add(novo)
        db.commit()
        print(f"Curso '{nome}' inserido com sucesso.")
    finally:
        db.close()

# 🔍 Consultar todos os cursos
def consultar_cursos():
    db = SessionLocal()
    criar_tabelas()
    try:
        resultados = db.query(Cursos).all()
    finally:
        db.close()
    if len(resultados) > 0:
        return resultados
    else:
        return []

# 📝 Atualizar a descrição de um curso
def atualizar_curso(nome_antigo, nova_descricao):
    db = SessionLocal()
    try:
        curso = db.query(Cursos).filter(Cursos.nomecursos == nome_antigo).first()
        if curso:
            curso.descricaocursos = nova_descricao
            db.commit()
            print(f"Curso '{nome_antigo}' atualizado.")
        else:
            print(f"Curso '{nome_antigo}' não encontrado.")
    finally:
        db.close()

# ❌ Deletar um curso pelo nome
def deletar_curso(nome):
    db = SessionLocal()
    try:
        curso = db.query(Cursos).filter(Cursos.nomecursos == nome).first()
        if curso:
            db.delete(curso)
            db.commit()
            print(f"Curso '{nome}' deletado.")
        else:
            print(f"Curso '{nome}' não encontrado.")
    finally:
        db.close()
# 🧹 Deletar todos os cursos do banco de dados
def deletar_todos_os_cursos():
    db = SessionLocal()
    try:
        cursos = db.query(Cursos).all()
        if cursos:
            for curso in cursos:
                db.delete(curso)
            db.commit()
            print("Todos os cursos foram deletados com sucesso.")
        else:
            print("Nenhum curso encontrado para deletar.")
    finally:
        db.close()
# 📥 Inserir vários cursos a partir de uma lista
def inserir_multiplos_cursos(lista_cursos):
    """
    Insere múltiplos cursos no banco de dados.

    Parâmetro:
        lista_cursos (list): Lista de dicionários ou tuplas com 'nome' e 'descricao'.
        Exemplo:
            [
                {"nome": "Python", "descricao": "Curso de Python básico"},
                {"nome": "SQL", "descricao": "Curso de banco de dados relacional"}
            ]
    """
    for item in lista_cursos:
        inserir_curso(item['Curso'],item['Descricao'])
