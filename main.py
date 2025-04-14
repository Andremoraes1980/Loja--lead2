from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo do lead
class Lead(BaseModel):
    nome: str
    telefone: str
    carro: str
    vendedor: str
    classificacao: str

# Lista para armazenar os leads recebidos
leads_db: List[Lead] = []

# Recebe um novo lead
@app.post("/leads")
def receber_lead(lead: Lead):
    leads_db.append(lead)
    return {
        "mensagem": f"Olá {lead.nome}, recebi seu interesse em {lead.carro}. Em breve um vendedor entrará em contato!"
    }

# Retorna todos os leads armazenados
@app.get("/leads")
def listar_leads():
    return leads_db
