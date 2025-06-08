from flask import Flask, Response, request
import json
import os
from chatterbot import ChatBot
from processar_artigos import get_artigos
from inicializar_nltk import baixar_recursos, extrair_assuntos
from robo import pesquisar_artigos_por_chaves

NOME_ROBO = "Robô Especialista em Direito Civil"
DIRETORIO_ATUAL = os.path.dirname(__file__)
BD_ROBO = os.path.join(DIRETORIO_ATUAL, "chat.sqlite3")
CONFIANCA_MINIMA = 0.6

try:
    baixar_recursos()
    robo = ChatBot(
        NOME_ROBO,
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        database_uri=f"sqlite:///{BD_ROBO}"
    )
    artigos = get_artigos(como_linhas=True)
    sucesso = True
    print("✅ Robô e artigos inicializados com sucesso.")
except Exception as e:
    sucesso = False
    robo = None
    artigos = []
    print(f"❌ Erro ao inicializar o robô ou carregar artigos: {e}")

servico = Flask("RoboDireitoCivil")

INFO = {
    "descricao": "Robô Especialista em Direito Civil. Responde perguntas e sugere artigos do Código Civil.",
    "versao": "1.0"
}

@servico.get("/")
def get_info():
    return Response(json.dumps(INFO), status=200, mimetype="application/json")

@servico.get("/alive")
def is_alive():
    return Response(json.dumps({"alive": "sim" if sucesso else "não"}), status=200, mimetype="application/json")

@servico.post("/responder")
def get_resposta():
    if not sucesso:
        return Response(status=503)

    conteudo = request.json
    pergunta = conteudo.get("pergunta", "").strip()

    if not pergunta:
        return Response(json.dumps({"erro": "Pergunta ausente ou vazia"}), status=400, mimetype="application/json")

    try:
        resposta = robo.get_response(pergunta.lower())

        resposta_json = {
            "resposta": resposta.text,
            "confianca": round(resposta.confidence, 4),
            "artigos_relacionados": []
        }

        respostas_de_comando_sem_busca = [
            "Você pode digitar uma palavra-chave ou uma pergunta que eu vou buscar artigos do Código Civil relacionados.",
            "Basta me enviar uma pergunta ou um termo e eu buscarei os artigos mais relacionados com base em palavras-chave."
        ]

        if resposta.confidence >= CONFIANCA_MINIMA and resposta.text not in respostas_de_comando_sem_busca:
            chaves = extrair_assuntos(pergunta)
            
            if chaves:
                encontrou_artigos, artigos_selecionados = pesquisar_artigos_por_chaves(chaves, artigos)
                
                if encontrou_artigos:
                    resposta_json["artigos_relacionados"] = list(artigos_selecionados.values())

        return Response(json.dumps(resposta_json, ensure_ascii=False), status=200, mimetype="application/json")
    except Exception as e:
        print(f"❌ Erro ao obter resposta do robô: {e}")
        return Response(json.dumps({"erro": f"Erro interno ao processar a pergunta: {str(e)}"}), status=500, mimetype="application/json")


@servico.post("/artigos")
def post_artigos():
    if not sucesso:
        return Response(status=503)

    conteudo = request.json
    entrada = conteudo.get("busca", "").strip().lower()

    if not entrada:
        return Response(json.dumps({"erro": "Busca por palavra-chave vazia"}), status=400, mimetype="application/json")

    chaves = [c.strip() for c in entrada.replace(",", " ").split()]
    chaves = [c for c in chaves if c]

    encontrou, artigos_selecionados = pesquisar_artigos_por_chaves(chaves, artigos)

    return Response(
        json.dumps({"artigos": list(artigos_selecionados.values())}, ensure_ascii=False),
        status=200 if encontrou else 204,
        mimetype="application/json"
    )

if __name__ == "__main__":
    servico.run(host="0.0.0.0", port=5000, debug=True)