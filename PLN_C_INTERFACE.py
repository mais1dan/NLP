import nltk
from nltk.chat.util import Chat, reflections
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import ttk

# Configuração inicial do NLTK
def configurar_nltk():
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('punkt')
        nltk.download('stopwords')

configurar_nltk()

class AplicativoNLP:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de NLP com Tkinter")
        self.root.geometry("800x600")
        
        # Configuração do Chatbot
        self.pares = [
            ['Oi|Olá|E aí', ['Olá!', 'Oi, como posso ajudar?']],
            ['Qual é seu nome?', ['Me chamo ChatNLP!']],
            ['Como você está?', ['Estou bem, obrigado!']],
            ['O que é NLP?', ['É Processamento de Linguagem Natural!']],
            ['Tchau|Xau|Até mais', ['Até logo!']]
        ]
        self.chatbot = Chat(self.pares, reflections)
        
        self.criar_interface()
    
    def criar_interface(self):
        # Notebook (abas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        
        # Aba do Chatbot
        self.aba_chat = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_chat, text='Chatbot')
        
        # Aba de Análise de Texto
        self.aba_analise = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_analise, text='Análise de Texto')
        
        # Widgets do Chatbot
        self.criar_aba_chat()
        
        # Widgets de Análise de Texto
        self.criar_aba_analise()
    
    def criar_aba_chat(self):
        # Área de conversa
        self.conversa = scrolledtext.ScrolledText(
            self.aba_chat, wrap=tk.WORD, width=70, height=20, state='disabled'
        )
        self.conversa.pack(pady=10, padx=10)
        
        # Entrada do usuário
        frame_entrada = tk.Frame(self.aba_chat)
        frame_entrada.pack(fill='x', padx=10, pady=5)
        
        self.entrada = tk.Entry(frame_entrada, font=('Arial', 12))
        self.entrada.pack(side='left', fill='x', expand=True)
        self.entrada.bind('<Return>', self.enviar_mensagem)
        
        btn_enviar = tk.Button(
            frame_entrada, text="Enviar", command=self.enviar_mensagem
        )
        btn_enviar.pack(side='right', padx=5)
        
        # Mensagem inicial
        self.adicionar_mensagem("Chatbot", "Olá! Como posso ajudar? Digite 'sair' para encerrar.")
    
    def criar_aba_analise(self):
        # Área de texto para análise
        tk.Label(
            self.aba_analise, text="Digite o texto para análise:", 
            font=('Arial', 10, 'bold')
        ).pack(pady=5)
        
        self.texto_analise = scrolledtext.ScrolledText(
            self.aba_analise, wrap=tk.WORD, width=70, height=10
        )
        self.texto_analise.pack(pady=5, padx=10)
        self.texto_analise.insert('1.0', "O Processamento de Linguagem Natural (NLP) é uma área fascinante da Inteligência Artificial.")
        
        # Botão de análise
        btn_analisar = tk.Button(
            self.aba_analise, text="Analisar Texto", 
            command=self.analisar_texto
        )
        btn_analisar.pack(pady=5)
        
        # Resultados
        self.resultados = scrolledtext.ScrolledText(
            self.aba_analise, wrap=tk.WORD, width=70, height=15, state='disabled'
        )
        self.resultados.pack(pady=10, padx=10)
    
    def enviar_mensagem(self, event=None):
        mensagem = self.entrada.get().strip()
        if not mensagem:
            return
        
        self.adicionar_mensagem("Você", mensagem)
        self.entrada.delete(0, 'end')
        
        if mensagem.lower() == 'sair':
            self.adicionar_mensagem("Chatbot", "Até logo!")
            return
        
        resposta = self.chatbot.respond(mensagem)
        resposta = resposta if resposta else "Não entendi. Pode reformular?"
        self.adicionar_mensagem("Chatbot", resposta)
    
    def adicionar_mensagem(self, remetente, mensagem):
        self.conversa.config(state='normal')
        self.conversa.insert('end', f"{remetente}: {mensagem}\n")
        self.conversa.config(state='disabled')
        self.conversa.see('end')
    
    def analisar_texto(self):
        texto = self.texto_analise.get('1.0', 'end-1c').strip()
        if not texto:
            messagebox.showwarning("Aviso", "Digite um texto para análise!")
            return
        
        try:
            # Tokenização
            tokenizer = RegexpTokenizer(r'\w+')
            tokens = tokenizer.tokenize(texto.lower())
            
            # Remoção de stopwords
            stop_words = set(stopwords.words('portuguese'))
            tokens_filtrados = [word for word in tokens if word not in stop_words]
            
            # Análise de frequência
            freq_dist = FreqDist(tokens_filtrados)
            
            # Exibir resultados
            self.resultados.config(state='normal')
            self.resultados.delete('1.0', 'end')
            
            self.resultados.insert('end', "=== TOKENS ===\n")
            self.resultados.insert('end', f"{tokens}\n\n")
            
            self.resultados.insert('end', "=== TOKENS SEM STOPWORDS ===\n")
            self.resultados.insert('end', f"{tokens_filtrados}\n\n")
            
            self.resultados.insert('end', "=== PALAVRAS MAIS FREQUENTES ===\n")
            for palavra, freq in freq_dist.most_common(5):
                self.resultados.insert('end', f"{palavra}: {freq}\n")
            
            self.resultados.config(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro na análise:\n{str(e)}")

# Execução do aplicativo
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicativoNLP(root)
    root.mainloop()
