from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega as variáveis do .env (certifique-se de ter um arquivo .env na raiz do projeto)
load_dotenv()

# Variáveis de ambiente
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Verificação básica para evitar erro silencioso
if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("SUPABASE_URL ou SUPABASE_KEY não configurados corretamente.")

# Criação do cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Criação da aplicação FastAPI
app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Substitua por domínio específico se necessário
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
    try:
        data = lead.dict()
        resposta = supabase.table("leads1").insert(data).execute()
        return {"mensagem": f"Lead de {lead.nome} recebido com sucesso."}
    except Exception as e:
        return {"erro": str(e)}

# Rota para listar todos os leads
@app.get("/leads")
def listar_leads():
    try:
        resposta = supabase.table("leads1").select("*").execute()
        return resposta.data
    except Exception as e:
        return {"erro": str(e)}
