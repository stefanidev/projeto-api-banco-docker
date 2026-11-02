from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app) #cria um cliente para enviar requisições à API durante os testes, sem precisar iniciar o Uvicorn.

def test_home():
    response = client.get("/") #simula uma requisição GET para a rota inicial.

    assert response.status_code == 200 #assert: é uma afirmação. Se a condição for falsa, o teste falha.
    assert response.json() == {
        "mensagem": "API funcionando!"
    }

    #um teste automatizado compara o resultado real com o resultado esperado. 
    # Quando eles são diferentes, o teste falha — mesmo que a diferença seja apenas uma letra ou um ponto de exclamação.