# Usa a imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copia os arquivos de requisitos para o container
COPY requirements.txt requirements.txt

# Instala as dependências
RUN pip install -r requirements.txt

# Copia todo o código da aplicação para o container
COPY . .

# Define a variável de ambiente para desabilitar o modo de depuração
ENV FLASK_ENV=production

# Expõe a porta onde o Flask vai rodar
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["flask", "run", "--host=0.0.0.0"]