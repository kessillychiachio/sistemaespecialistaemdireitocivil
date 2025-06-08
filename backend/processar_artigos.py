import sqlite3
import os
import json

CAMINHO = os.path.dirname(__file__)
CAMINHO_JSON = os.path.join(CAMINHO, "data", "codigo_civil_estruturado.json")
BD_ARTIGOS = os.path.join(CAMINHO, "artigos.sqlite3")

def iniciar_banco_artigos():
    if not os.path.exists(CAMINHO_JSON):
        print("Arquivo JSON com os artigos não encontrado.")
        return

    with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
        artigos = json.load(f)

    if os.path.exists(BD_ARTIGOS):
        os.remove(BD_ARTIGOS)

    conexao = sqlite3.connect(BD_ARTIGOS)
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artigos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artigo TEXT,
            texto TEXT,
            chave1 TEXT, chave2 TEXT, chave3 TEXT, chave4 TEXT,
            chave5 TEXT, chave6 TEXT, chave7 TEXT
        )
    """)

    for art in artigos:
        cursor.execute("""
            INSERT INTO artigos (artigo, texto, chave1, chave2, chave3, chave4, chave5, chave6, chave7)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            art.get("artigo"),
            art.get("texto"),
            art.get("chave1"),
            art.get("chave2"),
            art.get("chave3"),
            art.get("chave4"),
            art.get("chave5"),
            art.get("chave6"),
            art.get("chave7")
        ))

    conexao.commit()
    conexao.close()
    print("✅ Banco de artigos criado e populado com sucesso.")

def get_artigos(como_linhas=False):
    conexao = sqlite3.connect(BD_ARTIGOS)
    conexao.row_factory = sqlite3.Row if como_linhas else None
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM artigos")
    artigos = cursor.fetchall()

    conexao.close()
    return artigos

if __name__ == "__main__":
    iniciar_banco_artigos()