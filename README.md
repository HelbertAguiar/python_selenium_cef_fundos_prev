# Scraping com Selenium para buscar cotas de fundos de previdencia da Caixa Seguradora

Realiza scraping da página de fundos previdenciários da CAIXA

## 🛠️ Como instalar

Baixe o código fonte, em seguida através de um terminal CLI (eg.: cmd) vá até a pasta baixada do projeto e execute o comando abaixo para instalação das bibliotecas do selenium e beatifulsoup nas versões utilizadas neste projeto:

>   pip install -r requirements.txt

Observação: é necessário ter instalado o PIP - Gerenciador de Pacotes

## 📦 Utilização

Insira as datas para pesquisa no arquivo `./data/input.txt` e execute o código abaixo:

>   python main.py

O resultado ficará salvo na pasta \
`./data/output*DatetimeHereOfExecution*.txt`\
O log de execução ficará salvo na pasta \
`./data/output*DatetimeHereOfExecution*.txt`

## 🔗 Link do Scraping

<https://www.caixavidaeprevidencia.com.br/previdencia/rendimento-dos-fundos>