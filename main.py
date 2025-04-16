from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# Variáveis de ambiente
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Criação do cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Criação da aplicação FastAPI
app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pode substituir "*" pelo domínio do seu front-end
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de dados do Lead
class Lead(BaseModel):
    nome: str
    telefone: str
    carro: str
    vendedor: str
    classificacao: str

# Rota para criar um novo lead
@app.post("/leads")
def criar_lead(lead: Lead):
    data = lead.dict()
    resposta = supabase.table("leads1").insert(data).execute()
    return {"mensagem": f"Lead de {lead.nome} recebido com sucesso."}

# Rota para listar todos os leads
@app.get("/leads")
def listar_leads():
    resposta = supabase.table("leads1").select("*").execute()
    return resposta.data
