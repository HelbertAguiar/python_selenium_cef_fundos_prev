from selenium import webdriver
from bs4 import BeautifulSoup
import logging
from time import sleep
from datetime import datetime
import sys


class ScraperPrev():

    def __init__(self, url: str, sleep: int = 5, nivel_log=logging.INFO):
        self.now = datetime.now()
        self.date_current_str = self.now.strftime("%d-%m-%Y_%Hh%Mmin%Sseg")
        self.configura_log(self.date_current_str, nivel_log)
        self.lista_datas = self.busca_data()
        self.url = url
        self.sleep = sleep
        self.inicia_navegador()
        self.inicia_scraping()
        self.encerra_navegador()

    @staticmethod
    def configura_log():
        logging.basicConfig(
            filename='./log/log.txt',
            filemode='w',
            level=logging.INFO,
            format=('%(asctime)s.%(msecs)03d'
                    '%(levelname)8s %(module)s: %(message)s'),
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def busca_data(self):
        lista_datas = []
        with open('./data/input.txt', 'r') as reader:
            for line in reader.readlines():
                lista_datas.append(line.split())

        logging.info('Concluido busca das datas para pesquisa')
        return lista_datas

    def inicia_scraping(self):
        driver = self.driver
        driver.get(self.url)
        sleep(self.sleep)
        assert 'Caixa Vida e Previdência' in driver.title

        with open('data/output.txt', 'a', encoding='utf-8') as file:
            file.write('DATA;NOME FUNDO;TAXA ADM;COTA;CLASSE')
            file.write("\n")

        for data in self.lista_datas:
            data_string = str(data).replace('[', '')\
                                   .replace(']', '').replace('\'', '')
            self.insere_data(driver, data_string)
            sleep(self.sleep)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            table = soup.find_all('table', {'class':
                                            'tabela-fundo-investimento'})[0]
            table = table.tbody
            self.get_data(table, data_string)

    def insere_data(self, driver, dataInserir):
        sleep(self.sleep)
        input = driver.find_element_by_id(
            'formTabelaFundo.dataConsulta.input')
        input.clear()
        input.send_keys(dataInserir.replace('/', ''))

    def get_data(self, table, data):

        tags_tr = table.findChildren("tr", recursive=False)
        classe = ''

        for tr in tags_tr:
            if tr.has_attr('class'):
                classe = tr.text
            else:
                nome_fundo = tr.findAll('td')[0].text
                taxa_adm = tr.findAll('td')[2].text
                # data_cota = tr.findAll('td')[3].text
                cota = tr.findAll('td')[4].text
                self.save_to_file(data, nome_fundo,
                                  taxa_adm, cota, classe)
        logging.info(f'Consulta com sucesso referente a:{data}')

    def save_to_file(self, data_cota, nome_fundo, taxa_adm, cota, classe):
        with open('data/output.txt', 'a', encoding='utf-8') as file:
            file.write(f'{data_cota};{nome_fundo};{taxa_adm};{cota};{classe}')
            file.write("\n")

    def inicia_navegador(self):
        try:
            self.driver = webdriver.Firefox(
                            executable_path='./driver/geckodriver.exe',
                            service_log_path=os.devnull)
            logging.info('Navegador aberto com sucesso')
        except:
            logging.critical('Falha na carga do driver do navegador')
            sys.exit('Falha no carregamento do driver ou localizacao '
                     'do path firefox')

    def encerra_navegador(self):
        self.driver.close()
        logging.info('Navegador encerrado com sucesso')


URL = ('https://www.caixavidaeprevidencia.com.br/'
       'previdencia/rendimento-dos-fundos')
SLEEP = 12
scraper = ScraperPrev(URL, SLEEP)
