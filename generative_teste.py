import google.generativeai as genai
MAIN_PROMPT = "Você é um médico com anos de experiência especializado em pediatria"

class Gemini:
    def __init__(self, prompt, api_key):
        genai.configure(api_key=api_key)
        self.api_key = api_key
        self.prompt = prompt
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
        )
        self.chat = model.start_chat(
            history=[]
        )
    def generate(self):
        prompt = (f'{MAIN_PROMPT}\n {self.prompt}=')
        self.chat.send_message(prompt)
        # print(prompt)
        print(self.chat.last.text)
        return self.chat.last.text
    
    def containsHistory(self):
        return self.chat.history == []
    
gerador=Gemini('Escreve um pequeno texto sobre medicina','AIzaSyDeQXP7ZRCoyDGTXd6h9boFLJZGx0KXdb4')

gerador.generate()