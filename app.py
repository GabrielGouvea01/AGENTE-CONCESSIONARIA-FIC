# Importando as bibliotecas
from flask import Flask, jsonify, request
from flask_cors import CORS
from agno.models.openai import OpenAIChat
from agno.agent import Agent
from dotenv import load_dotenv
from supabase import create_client
import os

# Leitura da chave de API
load_dotenv()
# Usando o getenv para pegar o arquivo específico
supabase_url = os.getenv("SUPABASE_URL")
# Usando o getenv para pegar o arquivo específico
supabase_key = os.getenv("SUPABASE_KEY")
# Criando a conexão com o banco de dados, passando a URL e a KEY
supabase = create_client(supabase_url, supabase_key)

# Criar o nosso app
app = Flask(__name__)
# Habilitar o CORS
CORS(app)

# Criar o agente com a temática de Concessionária
agente = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    description=(
        "Você é o assistente virtual da Concessionária VeloCidade. "
        "Slogan: Aqui seu sonho corre mais rápido. "
        "Sua função é atender clientes e potenciais compradores, fornecendo informações sobre veículos, "
        "serviços, agendamentos de test drive e preços de forma clara, cordial e com um toque leve de humor "
        "e entusiasmo automobilístico, sempre alinhado à identidade ágil e moderna da concessionária. "
        
        "Catálogo de veículos disponíveis: "
        "- Categoria Tradicionais: Toyota Corolla (R$ 150.000) e Honda Civic (R$ 160.000). "
        "- Categoria Esportivos: Porsche 911 Carrera (R$ 900.000) e Chevrolet Corvette Stingray (R$ 850.000). "
        "- Categoria Luxo: Rolls-Royce Phantom (R$ 6.000.000). "
        
        "Serviços oferecidos pela concessionária: Test Drive Agendado, Financiamento com Taxas Especiais, "
        "Garantia Estendida, Oficina Especializada e Consultoria de Customização. "
        
        "Todos os veículos e serviços são de excelente qualidade e devem ser apresentados de forma empolgante. "
        
        "Diretrizes de atendimento: Responda sempre em português do Brasil. Seja educado, simpático e objetivo. "
        "Utilize humor leve e jargões do mundo do automobilismo quando apropriado, sem exageros. "
        "Ajude o cliente a escolher a máquina ideal para a garagem dele. Ao falar sobre preços, informe os valores de forma clara. "
        "Caso não saiba alguma informação técnica muito específica, informe isso de maneira transparente e sugira "
        "entrar em contato ou agendar uma conversa com um de nossos consultores na loja física. "
        "Não utilize formatação Markdown nas respostas, incluindo símbolos como #, ##, **, *, ou similares. "
        "Mantenha o foco em proporcionar uma experiência empolgante e transmitir a sensação de poder, conforto e a "
        "adrenalina que a Concessionária VeloCidade oferece aos seus clientes."
    ),
    markdown=True
)

@app.route("/", methods=['GET'])
def testar():
    return jsonify({'mensagem': "API da Concessionária VeloCidade funcionando"})

# Criar a rota e o método POST para o Chat
@app.route("/chat", methods=['POST'])
def pergunta():
    dados = request.get_json()
    pergunta = dados['pergunta']
    resposta = agente.run(pergunta)
    return jsonify({"resposta": resposta.content})

# Criar a rota para agendamento de interesse/test drive
@app.route("/agendar", methods=['POST'])
def agendar():
    dados = request.get_json()
    novo_agendamento = {
        "nome": dados["nome"],
        "email": dados["email"],
        "data_visita": dados["data_visita"],
        "modelo_carro": dados["modelo_carro"]
    }
    # Insere os dados na tabela 'agendamentos' do Supabase
    supabase.table("agendamentos").insert(novo_agendamento).execute()
    return jsonify({"mensagem": "Agendamento realizado com sucesso! Prepare-se para acelerar."})

# Rodar o nosso app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)


# Preciso que você crie o código do front-end para uma concessionária de carros chamada Concessionária VeloCidade (Slogan: "Aqui seu sonho corre mais rápido"). O design deve ser moderno, elegante, responsivo e com uma temática automobilística (sugiro um tema escuro com detalhes em vermelho ou laranja esportivo). Use HTML5 puro, Tailwind CSS (via CDN) e JavaScript vanilla concentrados em um único arquivo para facilitar a execução.

# O site deve ser uma SPA (Single Page Application) baseada em um sistema de 3 abas (abas navegáveis via botões no menu superior):

# 1. Aba "Início":

# Exiba o nome da concessionária em destaque e o slogan.

# Adicione um texto institucional sobre a paixão por velocidade e atendimento exclusivo.

# Liste os serviços oferecidos: Test Drive Agendado, Financiamento com Taxas Especiais, Garantia Estendida, Oficina Especializada e Consultoria de Customização.

# 2. Aba "Carros Disponíveis":

# Crie um Grid de cards para exibir os 5 carros do catálogo. Cada card deve ter uma foto (use links reais do Unsplash de carros semelhantes para ilustrar), nome do carro, categoria e o valor formatado em Reais.

# Os carros são:

# Toyota Corolla (Tradicional) - R$ 150.000

# Honda Civic (Tradicional) - R$ 160.000

# Porsche 911 Carrera (Esportivo) - R$ 900.000

# Chevrolet Corvette Stingray (Esportivo) - R$ 850.000

# Rolls-Royce Phantom (Luxo) - R$ 6.000.000

# 3. Aba "Agendar Visita":

# Um formulário de agendamento de Test Drive / Visita.

# O formulário deve conter exatamente os seguintes campos obrigatórios:

# Nome Completo (nome) -> Campo de texto.

# E-mail (email) -> Campo de e-mail.

# Data da Visita (data_visita) -> Input tipo date.

# Modelo do Carro (modelo_carro) -> Um campo select (dropdown) com as 5 opções de carros listadas acima.

# 4. NOVO REQUISITO: Assistente Virtual (Widget de Chat Flutuante):

# No canto inferior direito da tela, adicione um botão flutuante fixo (estilo um ícone de balão de conversa).

# Ao clicar nesse botão, deve abrir uma pequena janela de chat (e fechar se clicado novamente).

# A janela de chat deve ter:

# Um topo fixo dizendo "Assistente VeloCidade" com um botão para fechar.

# Uma área central de rolagem onde as mensagens enviadas e recebidas serão exibidas em formato de "balões" estilo WhatsApp.

# Um campo de texto na parte inferior com um botão "Enviar".

# Exiba uma mensagem inicial automática do assistente: "Olá! Sou o assistente da VeloCidade. Quer saber mais sobre nossos carros ou serviços? Pergunte-me qualquer coisa!"

# Regras de Integração e Comunicação (Obrigatório JSON):

# Para o Formulário de Agendamento: Ao enviar, o JavaScript deve coletar os dados e fazer um fetch via POST para https://agente-concessionaria-fic.onrender.com/agendar com o cabeçalho 'Content-Type': 'application/json' e o corpo em string JSON ({ "nome": "...", "email": "...", "data_visita": "...", "modelo_carro": "..." }).

# Para o Chat do Assistente: Ao enviar uma mensagem, exiba o balão do usuário na tela imediatamente. Em seguida, faça um fetch via POST para https://agente-concessionaria-fic.onrender.com/chat enviando o payload em JSON exatamente assim: { "pergunta": "texto da mensagem" }.

# Enquanto espera a resposta da API, mostre um indicador visual de "digitando..." ou "carregando...".

# Assim que a API responder, pegue o valor do campo resposta do JSON retornado e exiba-o como o balão do assistente na tela.