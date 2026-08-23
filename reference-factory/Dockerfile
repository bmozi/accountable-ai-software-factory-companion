# © 2026 John Briggs — MIT licensed; see ../LICENSE-CODE.
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
WORKDIR /companion
COPY . .
ENV PYTHONPATH=/companion
CMD ["python", "-m", "accountable_factory.cli", "journey"]
