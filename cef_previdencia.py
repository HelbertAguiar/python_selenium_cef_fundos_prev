from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import sys


def inicia_driver(website, temp):

    try:
        options = Options()
        options.binary_location = 'C:/Program Files/Mozilla Firefox/firefox.exe'
        browser = webdriver.Firefox(
            options=options, executable_path='geckodriver.exe')
    except:
        sys.exit('Falha no carregamento do driver ou localizacao do path firefox')

    browser.implicitly_wait(temp)
    browser.get(website)

    if browser.title == '502 Bad Gateway':
        browser.quit()
        sys.exit('Falha no carregamento da pagina, error: 502 BAD GATEWAY')

    return browser


def insere_data(browser, temp, dataInserir):
    time.sleep(1)
    inputElement = browser.find_element_by_id(
        "formTabelaFundo.dataConsulta.input")
    inputElement.clear()
    inputElement.send_keys(dataInserir)


def print_table(table):

    tags_tr = table.findChildren("tr", recursive=False)
    classe = ''

    for tr in tags_tr:
        if tr.has_attr('class'):
            classe = tr.text
        else:
            nome_fundo = tr.findAll('td')[0].text
            taxa_adm = tr.findAll('td')[2].text
            dataInserir = tr.findAll('td')[3].text
            cota = tr.findAll('td')[4].text
            print('{};{};{};{};{}'.format(dataInserir, nome_fundo, taxa_adm, cota, classe))


def print_linha_inicial_csv():
    print('{};{};{};{};{}'.format( 'DATA', 'NOME FUNDO', 'TAXA ADM', 'COTA' , 'CLASSE') )


def leitura_arquivo_data():
    
    lista_datas = []
    with open('input_datas', 'r') as reader:
        for line in reader.readlines():
            lista_datas.append(line.split())

    return lista_datas

temp = 6  # segundos
browser = inicia_driver(
    'https://www.caixavidaeprevidencia.com.br/previdencia/rendimento-dos-fundos', temp)

print_linha_inicial_csv()
lista_datas = leitura_arquivo_data()

for data in lista_datas:

    insere_data(browser, temp, data)
    time.sleep(temp)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    table = soup.find_all("table", {
                        "class": "tabela-fundo-investimento text-center text-body-sm table table-bordered table-hover"})[0]
    table = table.tbody
    print_table(table)

browser.quit()
