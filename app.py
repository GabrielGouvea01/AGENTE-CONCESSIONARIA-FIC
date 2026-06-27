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