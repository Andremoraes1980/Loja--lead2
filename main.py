from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Configuração do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("SUPABASE_URL ou SUPABASE_KEY não configurados corretamente.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

# CORS para permitir requisições do seu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://leads-interface1.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de dados para a tabela do Supabase
class Lead(BaseModel):
    nome: str
    telefone: str
    veiculo: str
    temperatura: str
    origem: str

# Endpoint para criar um lead com logs de depuração
@app.post("/leads")
def criar_lead(lead: Lead):
    try:
        data = lead.dict()
        print(">>> Dados recebidos do frontend:", data)  # Log do que foi enviado

        resposta = supabase.table("leads").insert(data).execute()
        print(">>> Resposta do Supabase:", resposta)  # Log da resposta do Supabase

        return {
            "mensagem": "Lead criado com sucesso",
            "data": resposta.data
        }
    except Exception as e:
        print(">>> ERRO ao criar lead:", str(e))  # Log de erro
        return {"erro": str(e), "mensagem": "Erro ao criar lead"}

# Endpoint para listar todos os leads
@app.get("/leads")
def listar_leads():
    try:
        resposta = supabase.table("leads").select("*").execute()
        return resposta.data
    except Exception as e:
        print(">>> ERRO ao listar leads:", str(e))
        return {"erro": str(e)}
