# 01 — Especificação do atendente educacional

## Objetivo

Construir uma API REST em Python que receba perguntas de um aluno, gere respostas em português e mantenha o contexto das mensagens recentes da mesma conversa. O aluno poderá experimentar o fluxo completo pelo Swagger UI, com a aplicação executando em Docker.

## Escopo da primeira entrega

- Atendimento de dúvidas educacionais por API REST.
- Continuidade de conversa por identificador, com memória temporária.
- Modo simulado para a aula e integração configurável com a OpenAI.
- Swagger UI, OpenAPI e execução local em Docker.

RAG para consultar material de cursos e MCP para acessar serviços institucionais ficam para especificações futuras. A primeira entrega é um laboratório local, com perguntas fictícias e sem dados pessoais. O identificador da conversa serve para recuperar o contexto no laboratório. Um ambiente compartilhado exigirá autenticação e autorização por usuário.

## Requisitos e critérios de aceitação

| ID | Requisito | Critério de aceitação |
| --- | --- | --- |
| RF-01 | Iniciar conversa | Dada uma mensagem válida sem identificador, a API retorna HTTP 200 com um novo UUID e uma resposta em português. |
| RF-02 | Continuar conversa | Dado o UUID de uma conversa existente, a API retorna o mesmo UUID e fornece ao provedor até cinco pares anteriores de pergunta e resposta dessa conversa, do mais antigo ao mais recente, seguidos pela nova pergunta. Duas conversas têm históricos independentes. Um UUID válido desconhecido retorna 404. |
| RF-03 | Validar a entrada | A mensagem é obrigatória, deve ser uma string e deve conter de 1 a 2.000 caracteres após remover espaços das extremidades. Mensagem ausente, vazia, fora do limite, com tipo incorreto ou UUID inválido retorna 422. |
| RF-04 | Gerar resposta | O modo `simulado` responde de forma determinística e identifica a simulação. O modo `openai` usa a pergunta e o histórico recente e responde em português. Dúvidas sobre informações institucionais específicas, como preços ou datas de turmas, devem receber orientação para confirmação com a instituição. |
| RF-05 | Tratar falha de geração | Se o provedor falhar, exceder o tempo limite ou devolver texto vazio, a API retorna 503 com mensagem genérica. O histórico anterior permanece íntegro. Uma nova conversa só é registrada após a primeira resposta bem-sucedida. |
| RF-06 | Verificar serviço | `GET /health` retorna 200 e `{"status":"ok"}` quando a aplicação está de pé. Essa rota responde sem consultar o provedor. |
| RNF-01 | Documentar API | Swagger UI em `/docs` permite executar o atendimento. O contrato gerado em `/openapi.json` descreve exemplos, esquemas e respostas de sucesso e erro. |
| RNF-02 | Executar em Docker | `docker compose up --build` inicia a aplicação em modo simulado. O Swagger fica disponível em `http://localhost:8000/docs`. |
| RNF-03 | Proteger configuração | Credenciais são lidas do ambiente e ficam fora do repositório, das respostas HTTP e dos logs. Os logs também omitem o conteúdo das conversas. |
| RNF-04 | Delimitar persistência | A memória guarda até cinco pares completos por conversa no processo da API. Reiniciar o processo apaga as conversas. |

## Contrato HTTP

| Método | Rota | Sucesso | Erros previstos |
| --- | --- | --- | --- |
| GET | `/health` | 200 | — |
| POST | `/api/v1/atendimentos` | 200 | 404, 422, 503 |

**Abrir conversa**

```json
{
  "mensagem": "O que é uma API REST?"
}
```

**Resposta ilustrativa do modo simulado**

```json
{
  "conversa_id": "5ac95013-8f19-4384-8356-bc9318df1ca0",
  "resposta": "[Simulação] Sua pergunta sobre API REST foi recebida.",
  "modo": "simulado"
}
```

**Continuar conversa**

```json
{
  "conversa_id": "5ac95013-8f19-4384-8356-bc9318df1ca0",
  "mensagem": "Pode dar um exemplo em Python?"
}
```

Use o UUID da resposta real ao testar a continuação. O campo `conversa_id` também aceita `null` para abrir uma nova conversa. Na resposta, `modo` é `simulado` ou `openai`. Os erros de negócio usam o formato `{"detail":"Conversa não encontrada."}` para 404 e `{"detail":"Serviço de atendimento temporariamente indisponível."}` para 503. O 422 segue o formato de validação do FastAPI, com uma lista em `detail`.
