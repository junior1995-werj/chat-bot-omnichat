# chat-bot-omnichat

## Requisitos: 

- Ter o poetry instalado.
```shell
pip install poetry
```
- Versão mínima requerida do python: v3.11.0

## Instação

- Necessário clonar o projeto localmente:

```shell
git git@github.com:junior1995-werj/chat-bot-omnichat.git
```

- Para instalar as dependências:

```shell
poetry install
```

- Para ativar a virtual env:

```shell
poetry shell
```

- Atualizar as env vars:

```shell
cp local.env .env
```

## Requisitos: 
#### Tarefas:
1. Coleta de Dados:
- O chatbot deve consumir dados de uma API de filmes que está na seção de referências abaixo.
```shell
https://api.themoviedb.org/3/
```
2. Funcionalidades do Chatbot:
    - O chatbot deve ser capaz de responder às seguintes perguntas:
        - “Qual é o elenco do filme ‘Nome do Filme’?”
        - “Qual é a sinopse do filme ‘Nome do Filme’?”
        - “Qual é a avaliação do filme ‘Nome do Filme’?”
        - “Quais são os filmes populares no momento?”
        - “Dê-me uma recomendação de filme com base no meu gostopor ‘Gênero’.”
        - “Quero um filme similar ao 'Nome do FIlme'"

3. Conceitos a serem Abordados:
- Agentes: Implemente um agente que gerencie as interações do chatbot com os usuários.
- Guardrails: Defina limites para as respostas geradas pelo chatbot para evitar resultados inadequados.
- Consumo de API: Use a API de filmes para obter informações relevantes.

## Executar 
- renomear arquivo "variable.py" para ".env"
  
```shell
python bot.py
```
