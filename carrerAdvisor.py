import google.generativeai as genai
import Dao.CursoDAO as cursoDAO


class CareerAdvisor:
    def __init__(self, api_key: str):
        lista_cursos=cursoDAO.consultar_cursos()
        resultado=''  
        genai.configure(api_key=api_key)
        for curso in lista_cursos:
            resultado+=f"{curso.nomecursos} - {curso.descricaocursos}"
        # Define o modelo
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=(
        f"""
            Você é um analisador de perfil vocacional. Receberá respostas (A, B, C ou D) para um questionário de 10 perguntas, com o objetivo de identificar o perfil de interesse do usuário e recomendar cursos adequados.


            Os cursos disponíveis são os segunites:
            {resultado}

            Cada letra corresponde a um perfil:

            A → Tecnologia e Raciocínio Lógico

            B → Humanas e Sociais

            C → Criatividade e Artes

            D → Ciência e Investigação

            Perguntas do questionário:

            O que você mais gosta de fazer no seu tempo livre?
            A) Explorar tecnologia, resolver desafios de lógica ou programar pequenos projetos
            B) Passar tempo com amigos, conversar ou participar de atividades sociais
            C) Criar artes, escrever histórias, desenhar ou tocar instrumentos
            D) Fazer experimentos, observar a natureza ou ler sobre ciência e curiosidades

            Qual das atividades abaixo parece mais divertida para você?
            A) Resolver desafios de lógica ou montar estratégias em jogos
            B) Participar de um trabalho voluntário ou cuidar de alguém
            C) Pintar um quadro ou dirigir uma peça de teatro
            D) Investigar como funcionam as coisas ou fazer uma pesquisa

            Qual dessas frases te representa melhor?
            A) "Gosto de entender como tudo funciona."
            B) "Gosto de fazer a diferença na vida das pessoas."
            C) "Preciso expressar minhas ideias de forma criativa."
            D) "Tenho curiosidade sobre o mundo e quero explorar o desconhecido."

            Se você fosse organizar um evento, qual seria seu papel ideal?
            A) Cuidar da tecnologia e da parte prática
            B) Receber as pessoas e garantir que se sintam bem
            C) Criar o visual, a identidade e o conteúdo artístico
            D) Fazer pesquisas para garantir que tudo saia como o planejado

            Qual tipo de matéria você mais gostava na escola?
            A) Matemática ou Informática
            B) Sociologia ou Biologia
            C) Artes ou Literatura
            D) Física ou Química

            O que mais te motiva em uma profissão?
            A) Resolver problemas e usar raciocínio lógico
            B) Ajudar pessoas e promover o bem-estar
            C) Ter liberdade para criar e inovar
            D) Descobrir coisas novas e entender como o mundo funciona

            Você prefere trabalhar:
            A) Sozinho, com foco e concentração
            B) Com pessoas, em equipe
            C) De forma livre, com liberdade de expressão
            D) Investigando, testando e analisando hipóteses

            Como você reage diante de um desafio?
            A) Analiso a situação e tento encontrar uma solução lógica
            B) Busco apoio em outras pessoas e penso no impacto do problema
            C) Tento ver o desafio de forma criativa
            D) Pesquiso e estudo para entender melhor a situação

            Se você pudesse escolher um projeto para liderar, seria:
            A) Criar um aplicativo ou sistema inteligente
            B) Organizar uma campanha social
            C) Produzir um curta-metragem ou escrever um livro
            D) Fazer uma descoberta científica

            Em um grupo, você costuma ser:
            A) O que resolve problemas técnicos
            B) O que acolhe e motiva os outros
            C) O que tem ideias fora da caixa
            D) O que pesquisa e verifica as informações

            Instruções para análise:

            Conte quantas vezes cada letra (A, B, C, D) aparece nas respostas.

            Identifique o perfil predominante com base na letra mais frequente.

            Se houver empate entre dois perfis, utilize ambos.

            Recomende 3 cursos que combinem com o(s) perfil(is) identificado(s).

            Para cada curso, dê uma justificativa elaborada, conectando o interesse do usuário ao curso sugerido.

            Formato da resposta esperada:

            1. [Curso 1] - [Justificativa]
            2. [Curso 2] - [Justificativa]
            3. [Curso 3] - [Justificativa]
 
            NÃO EXIBA NADA ALÉM DA LISTA DE CURSOS NO FORMATO ACIMA
            
            """
                
            )
        )

        # Cria o chat uma única vez
        self.chat = self.model.start_chat(history=[])
    
    def generate(self, respostas_usuario: list) -> str:
        """
        Envia as respostas do usuário e retorna a recomendação de curso e o motivo.

        :para respostas_usuario: Lista com 10 respostas (strings).
        :return: Resposta da IA contendo o curso recomendado e o motivo.
        """

        if len(respostas_usuario) != 10:
            raise ValueError("É necessário fornecer exatamente 10 respostas.")

        # Monta o texto das respostas
        texto_respostas = "\n".join([f"{i + 1}. {respostas}" for i, respostas in enumerate(respostas_usuario)])
        # Envia para o chat
        resposta = self.chat.send_message(
            f"Respostas do usuário às 10 perguntas:\n{texto_respostas}"
        )

        return resposta.text.strip()