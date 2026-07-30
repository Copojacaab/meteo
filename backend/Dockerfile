FROM python:3.12-slim                                      

WORKDIR /app            

COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt              
# separazione tra comando e copy per layerizzazione
COPY . .                                                    

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Sintassi comando uvicorn: 
# app.main:app: vai a app/main.py, prendi la variabile app e falla girare
# --host 0.0.0.0: ascolta connessioni da ovunque (0.0.0.0)
# --port 8000: porta su cui rispondere
# --reload: riavvia il server quando modifichi un file