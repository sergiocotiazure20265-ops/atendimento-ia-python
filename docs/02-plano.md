# 02 — Plano técnico

Implemente o contrato de [01-especificacao.md](01-especificacao.md) na ordem definida em [03-tarefas.md](03-tarefas.md).

## Tecnologias

| Componente | Escolha |
| --- | --- |
| Aplicação | Python 3.12, FastAPI, Pydantic e Uvicorn |
| Documentação HTTP | OpenAPI e Swagger UI do FastAPI |
| IA | Provedor simulado e SDK oficial da OpenAI com Responses API |
| Memória | Dicionário em memória, indexado pelo UUID da conversa |
| Execução | Docker e Docker Compose |
| Testes | pytest e FastAPI TestClient com HTTPX |

## Organização do código

| Caminho | Responsabilidade |
| --- | --- |
| `app/main.py` | Criar a aplicação, registrar rotas e configurar dependências por instância. |
| `app/api/rotas.py` | Expor rotas e converter resultados e falhas esperadas em respostas HTTP. |
| `app/api/schemas.py` | Definir entrada, saída, erros documentados e exemplos OpenAPI. |
| `app/services/atendimento.py` | Coordenar validação da conversa, memória e geração de respostas. |
| `app/services/provedores.py` | Definir o contrato de geração de texto e implementar os modos simulado e OpenAI. |
| `app/repositories/conversas.py` | Guardar pares de pergunta e resposta por UUID e aplicar o limite do histórico. |
| `tests/` | Verificar o contrato HTTP, o histórico e as falhas com provedores controlados. |
| `requirements.txt` e `requirements-dev.txt` | Registrar versões testadas das dependências de execução e teste. |
| `Dockerfile`, `compose.yaml` e `.dockerignore` | Construir e iniciar o contêiner local. |
| `.env.example`, `.gitignore` e `README.md` | Documentar configuração, comandos e roteiro de teste. |

## Fluxo do atendimento

1. A rota valida o JSON. O serviço consulta o UUID recebido ou gera um novo UUID para a interação.
2. Para uma conversa existente, o serviço carrega até cinco pares anteriores em ordem cronológica. Para uma nova conversa, inicia com histórico vazio.
3. O provedor recebe os turnos anteriores e a mensagem atual. No modo OpenAI, utilize `AsyncOpenAI` e `responses.create`, com as instruções do atendente em `instructions` e as mensagens de usuário e assistente em `input`. Leia o texto em `output_text`. Aplique um tempo limite de 30 segundos à chamada do SDK e desabilite suas novas tentativas automáticas para manter o tempo previsível na aula.
4. Depois de obter texto válido, o serviço grava pergunta e resposta juntas e mantém os cinco pares mais recentes. Em caso de falha, a rota retorna 503.
5. Use um único worker Uvicorn e serialize o processamento de duas solicitações que atinjam a mesma conversa existente. Mantenha a memória por instância da aplicação para que os testes possam montar aplicações independentes.

As instruções do atendente orientam respostas curtas em português e encaminhamento à instituição quando a pergunta exigir confirmação de dados institucionais. O simulado deve fornecer uma confirmação previsível, em português, que indique se recebeu contexto anterior. Para testar os argumentos enviados ao provedor, injete um substituto que registre as chamadas.

## Configuração

| Variável | Padrão | Uso |
| --- | --- | --- |
| `IA_MODO` | `simulado` | Aceita `simulado` ou `openai`. |
| `OPENAI_API_KEY` | Vazio | Obrigatória no modo `openai`. |
| `OPENAI_MODELO` | Vazio | Obrigatória no modo `openai`. Informe um modelo compatível com a Responses API e disponível na conta. |

Valide a configuração na inicialização. O modo simulado deve iniciar mesmo sem arquivo `.env`. O Compose pode repassar as três variáveis usando interpolação com valores padrão. Exclua o arquivo `.env` do Git e da imagem.

## Execução e verificação

- No contêiner, execute Uvicorn em `0.0.0.0:8000`. No host, publique a porta apenas em loopback com `127.0.0.1:8000:8000`.
- Execute `python -m pip install -r requirements-dev.txt` e `python -m pytest -q` em um ambiente virtual local. Os testes devem funcionar sem chamadas externas.
- Execute `docker compose up --build` e confira `http://localhost:8000/health`, `http://localhost:8000/docs` e `http://localhost:8000/openapi.json`.
- No Swagger, abra uma conversa, reutilize o UUID em uma segunda pergunta e execute os casos 404 e 422. Valide 503 com o provedor substituto nos testes. A demonstração com a OpenAI depende da configuração da conta usada na aula.

## Referências técnicas

- [FastAPI — URLs da documentação e do esquema OpenAPI](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls)
- [OpenAI — Geração de texto com Responses API](https://developers.openai.com/api/docs/guides/text)
