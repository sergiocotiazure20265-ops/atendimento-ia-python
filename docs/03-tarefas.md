# 03 — Tarefas de implementação

Use [01-especificacao.md](01-especificacao.md) como fonte das regras de negócio e [02-plano.md](02-plano.md) para as decisões técnicas. Implemente uma tarefa por vez. Marque o item apenas após verificar seu critério de conclusão.

## Etapa 1 — API e fluxo em modo simulado

- [x] **T01 — Criar a estrutura do projeto.** Inspecionar o workspace e criar ou adaptar a aplicação FastAPI, o ambiente de dependências e a rota `GET /health`. **Rastreio** RF-06, RNF-01. **Conclui quando** `/health` responde com o JSON previsto e `/docs` abre localmente.
- [ ] **T02 — Definir o contrato HTTP.** Criar os modelos Pydantic e a rota `POST /api/v1/atendimentos`. Validar mensagem e UUID. Declarar exemplos e respostas 200, 404, 422 e 503. **Depende de** T01. **Rastreio** RF-01, RF-03, RNF-01. **Conclui quando** o esquema OpenAPI descreve a rota e entradas inválidas recebem 422.
- [ ] **T03 — Implementar atendimento e memória em modo simulado.** Criar o serviço, o repositório e o provedor simulado. Entregar o fluxo completo, preservar o UUID nas continuações, isolar históricos e gravar apenas turnos concluídos. **Depende de** T02. **Rastreio** RF-01, RF-02, RF-04, RF-05, RNF-04. **Conclui quando** é possível iniciar e continuar uma conversa pelo Swagger e receber 404 com um UUID válido desconhecido.

## Etapa 2 — Provedor real e contêiner

- [ ] **T04 — Integrar a OpenAI.** Criar o provedor com Responses API, validar a configuração na inicialização e aplicar o tratamento de falhas. Preparar `.env.example` com valores vazios para chave e modelo e incluir as regras de exclusão para o `.env` real. **Depende de** T03. **Rastreio** RF-04, RF-05, RNF-03. **Conclui quando** um cliente SDK substituto comprova a montagem do contexto e o retorno 503 sem alterar o histórico em caso de falha.
- [ ] **T05 — Empacotar para Docker.** Criar `Dockerfile`, `compose.yaml` e `.dockerignore`. Publicar a porta local 8000, usar um worker e iniciar em modo simulado por padrão. **Depende de** T04. **Rastreio** RF-06, RNF-02, RNF-03. **Conclui quando** o Compose sobe sem `.env` e a API responde em `/health` e no Swagger.

## Etapa 3 — Testes e entrega

- [ ] **T06 — Automatizar a validação.** Cobrir saúde, esquema OpenAPI, criação e continuidade de conversa, isolamento por UUID, último conjunto de cinco pares em ordem, UUID desconhecido, limites da mensagem e falhas de geração sem gravação. Cobrir falha tanto na criação quanto na continuação e confirmar memória limpa ao criar outra instância da aplicação. **Depende de** T04. **Rastreio** RF-01 a RF-06, RNF-01, RNF-04. **Conclui quando** `python -m pytest -q` passa sem chave e sem rede.
- [ ] **T07 — Preparar e executar o roteiro de demonstração.** Documentar no README a execução local e com Docker, os endereços das rotas, como ativar a OpenAI e como reutilizar o UUID no Swagger. Registrar o resultado dos testes e da demonstração em Docker. **Depende de** T05 e T06. **Rastreio** RNF-01 a RNF-04. **Conclui quando** o roteiro reproduz o fluxo descrito na especificação em modo simulado.

## Primeiro prompt para o GitHub Copilot no VS Code

Abra a pasta do projeto com estes três arquivos na raiz. Adicione-os ao contexto do Copilot e use o modo Agente com este prompt.

```text
Leia por inteiro 01-especificacao.md, 02-plano.md e 03-tarefas.md.
Inspecione o projeto e implemente somente a tarefa T01, aproveitando a estrutura
existente quando ela atender ao plano. Execute as verificações previstas para
T01 e relate os arquivos alterados, os comandos executados e seus resultados.
Se encontrar uma contradição que bloqueie a tarefa, indique os trechos em questão.
Marque T01 em 03-tarefas.md apenas se o critério de conclusão for verificado.
Depois, pare para revisão.
```

Após revisar o resultado, use o mesmo prompt com o identificador da próxima tarefa. Se uma regra de negócio mudar, atualize primeiro a especificação e revise os itens afetados no plano e na lista de tarefas.
