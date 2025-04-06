from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Lead(BaseModel):
    nome: str
    interesse: str

@app.post("/lead")
def receber_lead(lead: Lead):
    return {"mensagem": f"Olá {lead.nome}, recebemos seu interesse em {lead.interesse}. Em breve um vendedor entrará em contato!"}
