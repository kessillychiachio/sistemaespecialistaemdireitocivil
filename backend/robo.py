import os
import json
from chatterbot import ChatBot
from processar_artigos import get_artigos
from inicializar_nltk import extrair_assuntos, baixar_recursos

NOME_ROBO = "Robô Especialista em Direito Civil"
CONFIANCA_MINIMA = 0.3

DIRETORIO_ATUAL = os.path.dirname(__file__)
BD_ROBO = os.path.join(DIRETORIO_ATUAL, "chat.sqlite3")

robo = ChatBot(
    NOME_ROBO,
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri=f"sqlite:///{BD_ROBO}"
)

def pesquisar_artigos_por_chaves(chaves, artigos):
    encontrados = {}

    for artigo in artigos:
        todas_chaves_da_pergunta_encontradas = True

        for chave_pergunta in chaves:
            chave_pergunta = chave_pergunta.strip().lower()

            chave_pergunta_encontrada_no_artigo = False 

            for i in range(1, 8):
                nome_chave_artigo = f"chave{i}"
                if nome_chave_artigo in artigo.keys():
                    campo_chave_artigo = artigo[nome_chave_artigo]
                    if campo_chave_artigo and chave_pergunta in campo_chave_artigo.lower():
                        chave_pergunta_encontrada_no_artigo = True
                        break 

            if not chave_pergunta_encontrada_no_artigo:
                todas_chaves_da_pergunta_encontradas = False
                break 

        if todas_chaves_da_pergunta_encontradas:
            encontrados[artigo["id"]] = {
                "id": artigo["id"],
                "artigo": artigo["artigo"],
                "texto": artigo["texto"]
            }

    return len(encontrados) > 0, encontrados

def executar():
    baixar_recursos() 
    artigos = get_artigos(como_linhas=True)

    while True:
        mensagem = input("👤 Você: ")

        if mensagem.lower() in ["sair", "exit", "quit"]:
            print("👋 Encerrando o robô. Até logo!")
            break

        resposta = robo.get_response(mensagem)
        print(f"\n🤖 {resposta.text} [confiança = {resposta.confidence:.2f}]")

        if resposta.confidence >= CONFIANCA_MINIMA:
            chaves = extrair_assuntos(mensagem)
            
            if chaves:
                encontrou_artigos, artigos_relacionados = pesquisar_artigos_por_chaves(chaves, artigos)

                if encontrou_artigos:
                    print("\n📚 Artigos do Código Civil relacionados:")
                    for art in artigos_relacionados.values():
                        print(f"\n🖋️ {art['artigo']}")
                        print(f"{art['texto']}")
                else:
                    print("\n⚠️ Nenhum artigo relacionado encontrado para a sua pergunta.")
            else:
                pass 
        else:
            print("\n🚧 Não tenho certeza sobre isso. Consulte um especialista ou busque diretamente no Código Civil.")

if __name__ == "__main__":
    executar()