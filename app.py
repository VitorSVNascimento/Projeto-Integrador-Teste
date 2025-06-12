from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from functools import wraps
from carrerAdvisor import CareerAdvisor
from cursoresposta import CursoResposta
from listaCurso import ListaCurso
import Dao.CursoDAO as cursoDAO
import pandas as pd
import unicodedata
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)
app.secret_key = 'admin123' 
# Cria a pasta de log
if not os.path.exists('logs'):
    os.mkdir('logs')

# Configura o arquivo de log
file_handler = RotatingFileHandler('logs/erro.log', maxBytes=10240, backupCount=3)
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s [%(levelname)s] %(message)s [em %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(file_handler)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def ind():
    return render_template('index.html')

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if usuario == "admin@senac.com" and senha == "123":
            session["usuario"] = usuario
            return redirect(url_for("index"))
        else:
            flash("Usuário ou senha inválidos.")
            return render_template("login.html")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('usuario', None)
    return redirect(url_for("login"))

@app.route("/erro")
def erro():
    return render_template('erro.html')

@app.route("/upload", methods=["POST"])
@login_required
def upload():
    if 'planilha' not in request.files:
        return 'Nenhum arquivo enviado', 400

    file = request.files['planilha']

    if file.filename == '':
        return 'Nome de arquivo vazio', 400

    # Verifica extensão
    if file.filename.endswith('.csv'):
        lista_cursos=ListaCurso(file)
    else:
        return render_template("erro.html", mensagem="Formato de arquivo não suportado")
    
    cursoDAO.deletar_todos_os_cursos()
    cursoDAO.inserir_multiplos_cursos(lista_cursos.dicionario)

    return render_template('planilha.html')


@app.route("/planilha")
@login_required
def planilha():
    return render_template('planilha.html')

@app.route("/formulario")
def formulario():
    return render_template('formulario.html')

@app.route("/sobre")
def sobre():
    return render_template('sobre.html')

# função para remover acentos na busca 
def remover_acentos(texto):
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')

@app.route("/cursos")
def cursos():
    pagina = int(request.args.get('pagina', 1))
    por_pagina = 9
    termo_busca = request.args.get('busca', '').lower()
    termo_busca = remover_acentos(termo_busca)  # Remover acento do que o usuário digitou

    cursos_todos = cursoDAO.consultar_cursos()

    if termo_busca:
        cursos_todos = [
            c for c in cursos_todos
            if termo_busca in remover_acentos(c.nomecursos.lower())
            or termo_busca in remover_acentos(c.descricaocursos.lower())
        ]

    total = len(cursos_todos)
    inicio = (pagina - 1) * por_pagina
    fim = inicio + por_pagina
    cursos = cursos_todos[inicio:fim]

    tem_anterior = pagina > 1
    tem_proxima = fim < total

    return render_template(
        'cursos.html',
        cursos=cursos,
        pagina=pagina,
        tem_anterior=tem_anterior,
        tem_proxima=tem_proxima
    )

@app.route("/matricula")
def matricula():
    return render_template('matricula.html')

@app.route("/processamento",methods=['POST'])
def processamento():
    """
    Adiciona as 10 alternativas dadas pelo usuário em uma lista e baseado nessas respostas a IA gera três recomendações de curso

    Return: página de resultado
    """
    lista_respostas=[]
    lista_recomendacao=[]
    for i in range (1,11):
        request.form.get('q{i}')
        lista_respostas.append(request.form.get(f'q{i}'))
    gerador=CareerAdvisor(os.getenv('API_KEY'))
    recomendacao=gerador.generate(lista_respostas)
    recomendacao=recomendacao.strip().split("\n")
    for i in recomendacao:
        curso_recomendacao=CursoResposta.transforma_texto(i)
        lista_recomendacao.append(curso_recomendacao)
    return render_template('resultado.html',lista_recomendacao=lista_recomendacao)

def erro_500(e):
    app.logger.error("Erro 500: %s", e, exc_info=True)
    return render_template("erro.html", mensagem="Erro interno do servidor."), 500

@app.errorhandler(404)
def page_not_found(e):
    app.logger.error("Erro inesperado: %s", e, exc_info=True)
    return render_template("erro.html", mensagem="Ocorreu um erro inesperado."), 404

@app.errorhandler(Exception)
def erro500(e):
    app.logger.error("Erro inesperado: %s", e, exc_info=True)
    return render_template("erro.html", mensagem="Ocorreu um erro inesperado."), 500


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")