from flask import Flask, render_template, Response, request, session, send_from_directory
import requests
import json
import os
import secrets

URL_ROBO = "http://localhost:5000"
URL_ROBO_ALIVE = f"{URL_ROBO}/alive"
URL_ROBO_RESPONDER = f"{URL_ROBO}/responder"
URL_ROBO_ARTIGOS = f"{URL_ROBO}/artigos"

CONFIANCA_MINIMA_FRONTEND = 0.60

DIRETORIO_ATUAL = os.path.dirname(__file__)
CAMINHO_ARQUIVOS = os.path.join(DIRETORIO_ATUAL, "static", "arquivos")

chat = Flask(__name__)
chat.secret_key = secrets.token_hex(16)

def acessar_robo(url, para_enviar=None):
    try:
        resposta = requests.post(url, json=para_enviar) if para_enviar else requests.get(url)
        resposta.raise_for_status()
        return True, resposta.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro acessando back-end: {str(e)}")
        return False, None
    except json.JSONDecodeError as e:
        print(f"❌ Erro decodificando JSON do back-end: {str(e)}")
        return False, None

def robo_alive():
    sucesso, resposta = acessar_robo(URL_ROBO_ALIVE)
    return sucesso and resposta.get("alive") == "sim"

def perguntar_robo(pergunta):
    sucesso, resposta_do_backend = acessar_robo(URL_ROBO_RESPONDER, {"pergunta": pergunta})

    mensagem_default_incerteza = "Não tenho certeza sobre isso. Consulte um especialista ou busque diretamente no Código Civil."
    
    mensagem = mensagem_default_incerteza
    artigos_para_exibir = []

    if sucesso:
        mensagem_robo_backend = resposta_do_backend.get("resposta")
        confianca = resposta_do_backend.get("confianca", 0)
        artigos_do_backend = resposta_do_backend.get("artigos_relacionados", []) 

        mensagem = mensagem_robo_backend

        if artigos_do_backend: 
            for ordem, artigo in enumerate(artigos_do_backend, start=1):
                artigos_para_exibir.append({
                    "id": artigo["id"],
                    "titulo": f"{ordem} - {artigo['artigo']}",
                    "texto": artigo["texto"]
                })
        
        if confianca < CONFIANCA_MINIMA_FRONTEND and not artigos_do_backend:
             mensagem = mensagem_default_incerteza


    return mensagem, artigos_para_exibir
    
def pesquisar_artigos(chaves):
    artigos_selecionados = []

    try:
        resposta = requests.post(URL_ROBO_ARTIGOS, json={"busca": " ".join(chaves)})
        if resposta.status_code == 200:
            dados = resposta.json()
            for ordem, artigo in enumerate(dados.get("artigos", []), start=1):
                artigos_selecionados.append({
                    "id": artigo["id"],
                    "titulo": f"{ordem} - {artigo['artigo']}",
                    "texto": artigo["texto"]
                })
        elif resposta.status_code == 204:
            print("ℹ️ Nenhuma chave encontrada para a busca de artigos.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro buscando artigos: {e}")

    return artigos_selecionados

@chat.get("/")
def index():
    return render_template("index.html")

@chat.post("/responder")
def get_resposta():
    conteudo = request.json
    pergunta = conteudo.get("pergunta", "").strip()

    if not pergunta:
        return Response(json.dumps({"erro": "Pergunta ausente"}), status=400, mimetype="application/json")

    resposta_texto, artigos = perguntar_robo(pergunta)

    session["artigos_selecionados"] = artigos

    return Response(json.dumps({
        "resposta": resposta_texto,
        "artigos": artigos,
        "artigos_pesquisados": bool(artigos)
    }, ensure_ascii=False), status=200, mimetype="application/json")

@chat.get("/artigos/<path:nome_arquivo>")
def download_artigo(nome_arquivo):
    return send_from_directory(CAMINHO_ARQUIVOS, nome_arquivo, as_attachment=True)

if __name__ == "__main__":
    chat.run(host="0.0.0.0", port=5001, debug=True)