import os
import json
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

DIRETORIO_ATUAL = os.path.dirname(__file__)
CAMINHO_CONVERSAS = os.path.join(DIRETORIO_ATUAL, "conversas")

ARQUIVOS = ["saudacoes.json", "comandos.json", "faq.json"]

NOME_ROBO = "Robô Especialista em Direito Civil"
BD_ROBO = os.path.join(DIRETORIO_ATUAL, "chat.sqlite3")

def carregar_conversas():
    todas_conversas = []

    for nome in ARQUIVOS:
        caminho = os.path.join(CAMINHO_CONVERSAS, nome)
        if not os.path.exists(caminho):
            print(f"Arquivo não encontrado: {caminho}")
            continue

        with open(caminho, encoding="utf-8") as f:
            dados = json.load(f)

            for item in dados.get("conversas", []):
                mensagens = item.get("mensagens", [])
                resposta = item.get("resposta", "")
                if resposta:
                    for pergunta in mensagens:
                        if pergunta:
                            todas_conversas.append([pergunta, resposta])

    return todas_conversas

def treinar_robo():
    robo = ChatBot(
        NOME_ROBO,
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        database_uri=f"sqlite:///{BD_ROBO}"
    )

    treinador = ListTrainer(robo)
    conversas = carregar_conversas()

    for pergunta, resposta in conversas:
        print(f"Treinando: '{pergunta}' → '{resposta}'")
        treinador.train([pergunta, resposta])

    print("Treinamento finalizado com sucesso.")

if __name__ == "__main__":
    treinar_robo()