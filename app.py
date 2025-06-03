from flask import Flask, render_template,request
from backend.models.generativeai import CareerAdvisor
import os

advisor = CareerAdvisor(os.getenv('API_KEY'))
app = Flask(__name__)

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index')
def mainPaga():
    return render_template('index.html')

# Rota para a página de login
@app.route('/login')
def login():
    return render_template('login.html')

# Rota para o formulário de avaliação vocacional
@app.route('/formulario')
def formulario():
    return render_template('formulario.html')

# Rota para a listagem dos cursos recomendados ou disponíveis
@app.route('/cursos')
def cursos():
    return render_template('cursos.html')

@app.route('/processar_formulario', methods=['POST'])
def processar_formulario():
    respostas = []
    for i in range(1,11):
        respostas.append( f'{i} - {request.form.get(f"q{i}")}')

    # Aqui você pode tratar, salvar no banco ou processar como quiser

    resultado = advisor.generate(respostas)

    
    result_list = resultado.split('NEXT')
    print(f'Result list len === {len(result_list)}')
    nome_cursos = []
    justificativa = []
    for curso in result_list:
        print(f'Curso === {curso}')
        print(f'NOME CURSO === {curso.split('-')[0]}')
        print(f'JUST CURSO === {curso.split('-')[1]}')
        nome_cursos.append(curso.split('-')[0])
        justificativa.append(curso.split('-')[1])
    
    lista_final = list(zip(nome_cursos, justificativa))
    # Pode enviar para uma página de resultado ou agradecimento
    return render_template('resultado.html', lista=lista_final,respostas=resultado)

if __name__ == '__main__':
    app.run()
