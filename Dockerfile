# Imagem base mínima, recomendada para reduzir a superfície de ataque
# (boa prática de DevSecOps a ser discutida no TCC).
FROM python:3.12-slim

WORKDIR /app

# Copia apenas o requirements.txt primeiro para aproveitar o cache de
# camadas do Docker: as dependências só são reinstaladas quando este
# arquivo muda, não a cada alteração de código.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Cria um usuário não-root e passa a executar a aplicação com ele.
# Evita que o processo da aplicação rode como root dentro do contêiner.
RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
