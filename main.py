from fastapi import FastAPI, HTTPException
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

# Modelo para criação de lead
class Lead(BaseModel):
    nome: str
    telefone: str
    veiculo: str
    temperatura: str
    origem: str

# Modelo para atualização de status
class StatusUpdate(BaseModel):
    status: str

# Criar novo lead
@app.post("/leads")
def criar_lead(lead: Lead):
    try:
        data = lead.dict()
        data["status"] = "nova-proposta"  # Status padrão ao criar
        print(">>> Dados recebidos:", data)

        resposta = supabase.table("leads").insert(data).execute()
        print(">>> Supabase resposta:", resposta)

        return {
            "mensagem": "Lead criado com sucesso",
            "data": resposta.data
        }
    except Exception as e:
        print(">>> ERRO ao criar lead:", str(e))
        return {"erro": str(e), "mensagem": "Erro ao criar lead"}

# Listar todos os leads
@app.get("/leads")
def listar_leads():
    try:
        resposta = supabase.table("leads").select("*").execute()
        return resposta.data
    except Exception as e:
        print(">>> ERRO ao listar leads:", str(e))
        return {"erro": str(e)}

# Atualizar status do lead
@app.put("/leads/{lead_id}/status")
def atualizar_status(lead_id: int, status_update: StatusUpdate):
    try:
        resposta = supabase.table("leads").update({"status": status_update.status}).eq("id", lead_id).execute()
        if not resposta.data:
            raise HTTPException(status_code=404, detail="Lead não encontrado")
        return {
            "mensagem": "Status atualizado com sucesso",
            "data": resposta.data
        }
    except Exception as e:
        print(">>> ERRO ao atualizar status:", str(e))
        return {"erro": str(e), "mensagem": "Erro ao atualizar status"}
