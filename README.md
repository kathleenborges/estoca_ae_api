# estoca_ae_api
Primeiro MVP para Pós PUC RIO - Engenharia de Software 

#!/bin/bash

# Cria o ambiente virtual
python3.10 -m venv venv-api

# Ativa o ambiente
source venv-api/bin/activate

# Instala as dependências
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup concluído! Para rodar, use: python app.py"