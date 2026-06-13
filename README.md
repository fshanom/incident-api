# Incident Management API

API REST para gerenciamento de incidentes operacionais, desenvolvida em **FastAPI**
como objeto de estudo do **TCC do MBA em Engenharia de Software (USP/ESALQ)**:

> **"Infraestrutura como Código e orquestração de contêineres em nuvem para entrega
> ágil de uma API REST"**

O projeto é utilizado para medir métricas de entrega inspiradas nos indicadores
**DORA** (frequência de deploy, lead time e MTTR) e para discutir, na prática,
testabilidade de IaC, segurança (DevSecOps) e governança de mudanças.

## Stack

- **Python 3.12**
- **FastAPI** + **Pydantic v2**
- **Uvicorn** (ASGI server)
- **Pytest** + **pytest-cov** + **httpx** (testes)
- **Docker**
- **Terraform** (AWS ECR + App Runner)
- **GitHub Actions** (CI/CD)

## Estrutura do projeto

```
incident-api/
├── app/
│   ├── main.py               # FastAPI app
│   ├── models/
│   │   └── incident.py       # Modelos Pydantic (IncidentCreate, IncidentUpdate, Incident)
│   └── routers/
│       └── incidents.py      # Endpoints e store em memória
├── tests/                     # Suíte de testes pytest
├── terraform/                 # IaC: ECR + App Runner
├── .github/workflows/ci.yml   # Pipeline CI (test + build/smoke test)
├── Dockerfile
├── pytest.ini
└── requirements.txt
```

## Como executar localmente

### 1. Criar e ativar um ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Rodar a aplicação

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A API ficará disponível em `http://localhost:8000`, com documentação interativa em:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Executando com Docker

```bash
docker build -t incident-api:latest .
docker run -d -p 8000:8000 --name incident-api incident-api:latest
curl http://localhost:8000/incidents/health/check
```

A imagem usa `python:3.12-slim`, instala as dependências antes de copiar o código
(cache de camadas) e executa a aplicação com um usuário não-root (`appuser`).

## Executando os testes

```bash
pytest -v
```

O `pytest.ini` já habilita relatório de cobertura (`--cov=app`), exibindo o resumo
no terminal e gerando `coverage.xml` (usado pela pipeline de CI).

## Endpoints

Base path: `/incidents`

| Método | Rota                       | Descrição                                              |
|--------|----------------------------|---------------------------------------------------------|
| POST   | `/incidents/`              | Cria um novo incidente                                  |
| GET    | `/incidents/`               | Lista todos os incidentes (mais recente primeiro)       |
| GET    | `/incidents/{id}`           | Busca um incidente pelo ID                              |
| PUT    | `/incidents/{id}`           | Atualiza um incidente (parcial)                         |
| DELETE | `/incidents/{id}`           | Remove um incidente                                     |
| GET    | `/incidents/health/check`   | Health check (status, nome do serviço, total de incidentes) |

### Modelo de incidente

```json
{
  "id": "uuid",
  "title": "string (3-200 chars)",
  "description": "string (mínimo 10 chars)",
  "severity": "low | medium | high | critical",
  "status": "open | investigating | resolved | closed",
  "reported_by": "string",
  "created_at": "datetime (UTC)",
  "updated_at": "datetime (UTC)",
  "resolved_at": "datetime (UTC) | null",
  "resolution_notes": "string | null"
}
```

### Exemplo: criar um incidente

```bash
curl -X POST http://localhost:8000/incidents/ \
  -H "Content-Type: application/json" \
  -d '{
        "title": "Falha no serviço de pagamentos",
        "description": "O serviço de pagamentos está retornando erro 500 para todas as transações.",
        "severity": "high",
        "reported_by": "ops-team"
      }'
```

### Exemplo: resolver um incidente

Ao atualizar `status` para `resolved`, o campo `resolved_at` é preenchido
automaticamente (se ainda estiver vazio):

```bash
curl -X PUT http://localhost:8000/incidents/{id} \
  -H "Content-Type: application/json" \
  -d '{
        "status": "resolved",
        "resolution_notes": "Causa raiz identificada e corrigida."
      }'
```

> **Observação:** o store de dados é em memória (dict Python), portanto os dados
> são perdidos a cada reinicialização da aplicação.

## CI/CD

A pipeline (`.github/workflows/ci.yml`) possui dois jobs:

1. **test**: checkout → setup Python 3.12 → instala dependências → roda `pytest`
   → publica `coverage.xml` como artifact.
2. **build** (depende de `test`): checkout → `docker build` → smoke test
   (sobe o container, aguarda alguns segundos e chama
   `/incidents/health/check` via `curl`).

## Infraestrutura como Código (Terraform)

Em `terraform/`:

- **Backend remoto S3** para o state (`tcc-tfstate-bucket`).
- `aws_ecr_repository` com `scan_on_push = true` (prática de DevSecOps: scan
  automático de vulnerabilidades a cada push de imagem).
- `aws_apprunner_service` com `auto_deployments_enabled = true` (simula um
  fluxo GitOps: novas imagens publicadas geram deploy automático).

Variáveis configuráveis (`terraform/variables.tf`): `aws_region` (default
`us-east-1`), `cpu` (default `0.25 vCPU`) e `memory` (default `0.5 GB`).

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

## Contexto do TCC

Este repositório é o objeto de estudo de um caso aplicado que investiga como a
combinação de IaC e orquestração de contêineres em nuvem apoia a entrega ágil
de uma API REST, medindo métricas inspiradas no DORA (frequência de deploy,
lead time for changes e MTTR) e documentando desafios práticos de
testabilidade de IaC, segurança (DevSecOps) e governança de mudanças.
