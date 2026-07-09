FROM python:3.13-slim

WORKDIR /app

# Instalar herramientas necesarias
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*


# Instalar uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"


# Copiar configuración del proyecto
COPY pyproject.toml README.md ./

# Instalar dependencias
RUN uv sync --no-install-project


# Copiar código
COPY . .


# Instalar proyecto
RUN uv sync


EXPOSE 8000


CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
