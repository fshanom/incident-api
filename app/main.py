"""FastAPI application entry point.

Study object for the MBA capstone project (TCC) - MBA em Engenharia de
Software, USP/ESALQ. Theme: "Infraestrutura como Código e orquestração de
contêineres em nuvem para entrega ágil de uma API REST".

This Incident Management REST API is the application under test used to
measure DORA-inspired delivery metrics (deployment frequency, lead time for
changes and MTTR) and to discuss IaC testability, DevSecOps practices and
change governance.
"""

from fastapi import FastAPI

from app.routers import incidents

app = FastAPI(
    title="Incident Management API",
    description=(
        "API REST para gerenciamento de incidentes operacionais, utilizada "
        "como objeto de estudo do TCC de MBA em Engenharia de Software "
        "(USP/ESALQ) sobre Infraestrutura como Código e orquestração de "
        "contêineres em nuvem para entrega ágil de uma API REST."
    ),
    version="1.0.0",
)

app.include_router(incidents.router)


@app.get("/", tags=["root"])
def root() -> dict:
    """Simple landing endpoint pointing to the interactive API docs."""

    return {"message": "Incident Management API", "docs": "/docs"}
