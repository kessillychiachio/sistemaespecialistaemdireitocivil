🤖 Robô Especialista em Direito Civil

Este projeto implementa um Sistema Especialista na forma de um ChatterBot Web, especializado em Direito Civil brasileiro. Ele é capaz de responder a perguntas sobre conceitos jurídicos e fornecer artigos relevantes do Código Civil.

O sistema é dividido em um back-end de serviços (API) e um front-end web (interface de chat), com separação clara de responsabilidades.

🌟 Funcionalidades

Chatbot Interativo: Permite aos usuários fazerem perguntas em linguagem natural.
Base de Conhecimento: Responde a perguntas frequentes (FAQ) e comandos pré-definidos.
Busca de Artigos do Código Civil: Localiza e apresenta artigos relevantes com base em palavras-chave extraídas da pergunta do usuário.
Processamento de Linguagem Natural (PLN): Utiliza NLTK para tokenização, eliminação de stopwords e stemming, aprimorando a compreensão das perguntas e a extração de chaves.
Estrutura em Camadas: Back-end (serviços Flask) e Front-end (interface de chat Flask) separados.
Persistência de Dados: Armazena o treinamento do chatbot e os artigos do Código Civil em bancos de dados SQLite.

🛠️ Tecnologias Utilizadas

Python
Flask: Framework web para o back-end e front-end.
ChatterBot: Biblioteca para a inteligência conversacional do chatbot.
NLTK (Natural Language Toolkit): Para operações de PLN em português.
SQLite3: Banco de dados para persistência do treinamento do ChatterBot e dos artigos.

🚀 Como Configurar e Executar o Projeto
Siga os passos abaixo para colocar o Robô Especialista em Direito Civil em funcionamento em seu ambiente local.

1. Pré-requisitos

Certifique-se de ter o Python instalado em sua máquina.

2. Configurar o Ambiente Virtual

É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto.
python3 -m venv venv
source venv/bin/activate # No Windows, use `venv\Scripts\activate`

3. Instalar as Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias:
# Na raiz do projeto
pip install -r requirements.txt

4. Baixar Recursos NLTK

Os recursos do NLTK são essenciais para o PLN.
# Dentro da pasta 'backend/'
cd backend/
python inicializar_nltk.py

5. Preparar os Dados e Treinar o Robô
É fundamental seguir esta ordem para garantir que os bancos de dados sejam criados e o robô seja treinado corretamente.
# Ainda na pasta 'backend/'
# 5.1. Popular o Banco de Dados de Artigos (artigos.sqlite3)
python processar_artigos.py
# 5.2. Treinar o ChatterBot (chat.sqlite3)
python treinamento.py

6. Iniciar os Serviços
Agora você pode iniciar o back-end e o front-end em terminais separados.
6.1. Iniciar o Back-end (Serviço API)
Abra um novo terminal e navegue até a pasta backend/.
# Na pasta 'backend/'
python servico.py
Mantenha este terminal aberto e o serviço rodando. Ele estará disponível em http://127.0.0.1:5000.
6.2. Iniciar o Front-end (Interface Web)
Abra outro terminal e navegue até a pasta chat/.
# Na pasta 'chat/'
python chat.py
Mantenha este terminal aberto. A interface do chatbot estará disponível em http://127.0.0.1:5001.

7. Acessar o Chatbot
Abra seu navegador web e acesse o endereço:
http://127.0.0.1:5001/
Agora você pode interagir com o Robô Especialista em Direito Civil!

💡 Módulos Essenciais do Sistema Especialista
Este projeto foi desenvolvido com os seguintes módulos, conforme as diretrizes da disciplina para qual esse projeto foi desenvolvido:

Interface de Usuário: O front-end web (chat/chat.py e chat/templates/index.html) permite a interação intuitiva com o usuário.

Coleta de Dados: Os scripts de mineração e preparação (processar_artigos.py e gerar_chaves_json.py) são responsáveis por organizar e enriquecer a base de dados de artigos.

Base de Conhecimento: Composta pelos arquivos de conversas (backend/conversas/*.json), pelo banco de dados de artigos (backend/artigos.sqlite3) e pelo banco de dados de treinamento do ChatterBot (backend/chat.sqlite3).

Motor/Recurso de Inferência: Implementado pelo robo.py que utiliza a biblioteca ChatterBot para processar as perguntas e decidir as respostas.

Memória de Trabalho: Gerenciada pelas sessões do Flask no chat.py, permitindo a manutenção de dados como artigos selecionados durante a interação do usuário.