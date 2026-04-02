FROM python:3.11-slim

# Crear usuario no-root
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copiar requisitos e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY . .

# Cambiar permisos
RUN chown -R appuser:appuser /app
USER appuser

# Exponer puerto
EXPOSE 7860

# Comando para ejecutar
CMD ["python", "main.py"]
