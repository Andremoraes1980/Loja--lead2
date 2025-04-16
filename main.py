from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from supabase import create_client, Client
import os

app = FastAPI()

# Conexão com o Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Modelo do lead
class Lead(BaseModel):
    nome: str
    telefone: str
    carro: str
    vendedor: str
    classificacao: str

# Recebe um novo lead e salva no Supabase
@app.post("/leads")
def receber_lead(lead: Lead):
    response = supabase.table("leads").insert(lead.dict()).execute()
    return {
        "mensagem": f"Olá {lead.nome}, recebi seu interesse em {lead.carro}. Em breve um vendedor entrará em contato!",
        "status": response.status_code
    }

# Retorna todos os leads armazenados no Supabase
@app.get("/leads")
def listar_leads():
    response = supabase.table("leads").select("*").execute()
    return response.data
