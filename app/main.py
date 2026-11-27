from fastapi import FastAPI


app = FastAPI(
    title="Atendente educacional",
    description="API REST para atendimento educacional com IA.",
)


@app.get("/health", summary="Verificar disponibilidade da API")
def health() -> dict[str, str]:
    return {"status": "ok"}
