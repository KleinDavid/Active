FROM python:3.9

WORKDIR /app

# Kopiere die requirements.txt und installiere Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den gesamten actionParser-Inhalt in das Arbeitsverzeichnis im Container
COPY . .

# Befehl zum Ausführen der Anwendung
CMD ["python", "main.py"]