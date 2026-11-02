from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from app.database import engine
from pydantic import BaseModel #Pydantic é usado para validar e estruturar os dados que chegam na API.

app = FastAPI() #cria a nossa aplicação

class ClienteCreate(BaseModel):  #define o formato que a API espera receber.
    nome: str
    email: str
    cidade: str | None = None 


@app.get("/") #cria endpoint 
def home():
    return {"mensagem": "API funcionando!"}

@app.get("/clientes")
def listar_clientes():
    with engine.connect() as connection:   # abre uma conexão com o SQL Server.
        resultado = connection.execute(     #manda o SQL para o banco.
            text("SELECT id, nome, email, cidade FROM clientes")
        )

        clientes = resultado.mappings().all() #transforma o resultado em uma lista de registros que o FastAPI consegue devolver como JSON.
    return clientes 

@app.get("/clientes/{id}")
def buscar_cliente(id: int):
    with engine.connect() as connection:
        resultado = connection.execute(
            text("""
                SELECT id, nome, email, cidade 
                FROM clientes 
                WHERE id = :id """), #é um parameto da consulta
                {"id": id} #O :id do SQL recebe o valor do id que veio da URL.

        )

        cliente_id = resultado.mappings().first() #pega o primeiro registro encontrado.

    if cliente_id is None:      #verifica se o banco não encontrou nenhum registro.
        raise HTTPException(    #interrompe a função e devolve um erro HTTP
            status_code=404,    #recurso não encontrado
            detail="Cliente não encontrado"
        )

    return cliente_id

 
@app.post("/clientes", status_code=201)
def criar_cliente(cliente: ClienteCreate): #O corpo recebido dessa requisição deve seguir o modelo ClienteCreate.
    with engine.begin() as connection:
        resultado = connection.execute(   #OUTPUT INSERTED.id pede: "SQL Server, me devolva o ID que acabou de ser criado."
            text("""
                INSERT INTO clientes (nome, email, cidade)
                OUTPUT INSERTED.id      
                VALUES (:nome, :email, :cidade)
            """),
            cliente.model_dump()
        )

        cliente_id = resultado.scalar_one() #Aqui pegamos esse ID que o banco devolveu.

    return {
        "id": cliente_id,
        **cliente.model_dump() #model dump fornece os valores nesse formato de dicionário.
    } 

@app.put("/clientes/{id}")
def atualizar_cliente(id: int, cliente: ClienteCreate):
    with engine.begin() as connection:  #engine.begin(): executa a alteração dentro de uma transação.
        resultado = connection.execute(
            text("""
                UPDATE clientes    
                SET nome = :nome,
                    email = :email,
                    cidade = :cidade
                WHERE id = :id
            """), #WHERE id = :id: limita a alteração ao cliente solicitado. Sem esse filtro, poderíamos atualizar todos os clientes.
            {
                "id": id,
                **cliente.model_dump()
            }
        )

        if resultado.rowcount == 0: #informa quantas linhas foram afetadas; se nenhuma foi alterada, retornamos 404.
            raise HTTPException(
                status_code=404,
                detail="Cliente não encontrado"
            )

    return {
        "mensagem": "Cliente atualizado com sucesso",
        "id": id,
        **cliente.model_dump()
    }


@app.delete("/clientes/{id}")
def excluir_cliente(id: int):
    try:
        with engine.begin() as connection:
            # Verifica se o cliente existe
            cliente = connection.execute(
                text("""
                    SELECT id
                    FROM clientes
                    WHERE id = :id
                """),
                {"id": id}
            ).first()

            if cliente is None:
                raise HTTPException(
                    status_code=404,
                    detail="Cliente não encontrado"
                )

            # Verifica se o cliente possui pedidos
            pedidos = connection.execute(
                text("""
                    SELECT TOP 1 id
                    FROM pedido
                    WHERE cliente_id = :id
                """),
                {"id": id}
            ).first()

            if pedidos is not None:
                raise HTTPException(
                    status_code=409,
                    detail="Não é possível excluir um cliente que possui pedidos"
                )

            # Exclui somente se não houver pedidos
            connection.execute(
                text("""
                    DELETE FROM clientes
                    WHERE id = :id
                """),
                {"id": id}
            )

    except HTTPException:
        raise

    return {
        "mensagem": "Cliente excluído com sucesso",
        "id": id
    }

