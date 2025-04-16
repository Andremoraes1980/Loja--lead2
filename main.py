from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from supabase import create_client, Client

# Variáveis de ambiente
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou substitua pelo domínio da sua interface, ex: ["https://leads-interface1.onrender.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo do lead
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
