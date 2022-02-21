from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
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
    def configura_log(date_current_str: str, nivel_log):
        logging.basicConfig(
            filename=f'./log/log_execution_{date_current_str}.txt',
            filemode='w',
            level=nivel_log,
            format=('%(asctime)s.%(msecs)02d | '
                    '%(levelname)8s (%(module)s => %(funcName)s) | '
                    '%(message)s'),
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def busca_data(self):
        lista_datas = []
        try:
            with open('./data/input.txt', 'r') as reader:
                for line in reader.readlines():
                    lista_datas.append(line.split())

            logging.info('Concluido busca das datas para pesquisa')
            return lista_datas
        except FileNotFoundError as e:
            logging.critical(f'Falha: {e}')
            sys.exit("Falha critica, consulte o log na pasta de mesmo nome")

    def inicia_scraping(self):
        driver = self.driver
        driver.get(self.url)
        sleep(self.sleep)
        assert 'Caixa Vida e Previdência' in driver.title
        self.salva_dados_csv(somenteCabecalho=True)

        for data in self.lista_datas:
            if data != '\n':
                self.insere_data(driver, data)
                sleep(self.sleep)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                table = soup.find_all(
                            'table', {'class': 'tabela-fundo-investimento'}
                        )[0]
                table = table.tbody
                self.captura_dados(table)
                driver.refresh()

    def insere_data(self, driver, dataInserir):
        try:
            driver.execute_script("window.scrollTo(0, 1000)")
            sleep(.1)
            input = driver.find_element(By.ID,
                                        'formTabelaFundo.dataConsulta.input')
            dataInserir = str(dataInserir).replace('[', '')\
                                          .replace(']', '')\
                                          .replace('\'', '')\
                                          .replace('/', '')
            input.send_keys(dataInserir)
            sleep(self.sleep)
        except Exception as e:
            logging.critical(f'Falha: {e}')
            sys.exit("Falha critica, consulte o log")

    def captura_dados(self, table):
        tags_tr = table.findChildren("tr", recursive=False)
        classe = ''

        for tr in tags_tr:
            if tr.has_attr('class'):
                classe = tr.text
            else:
                nome_fundo = tr.findAll('td')[0].text
                dt_inicio_fundo = tr.findAll('td')[1].text
                taxa_adm = tr.findAll('td')[2].text
                data_cota = tr.findAll('td')[3].text
                cota = tr.findAll('td')[4].text
                self.salva_dados_csv(data_cota, nome_fundo, dt_inicio_fundo,
                                     taxa_adm, cota, classe)
        logging.info(f'Consulta com sucesso referente a:{data_cota}')

    def salva_dados_csv(self, data=None, nome_fundo=None,
                        dt_inicio_fundo=None, taxa_adm=None,
                        cota=None, classe=None, somenteCabecalho=False):
        if somenteCabecalho is False:
            with open(f'./data/output_{self.date_current_str}.csv',
                      'a', encoding='utf-8') as file:
                file.write(f'{data};{nome_fundo};{dt_inicio_fundo};' +
                           f'{taxa_adm};{cota};{classe}')
                file.write("\n")
        else:
            with open(f'./data/output_{self.date_current_str}.csv',
                      'a', encoding='utf-8') as file:
                # include char BOM / Excell entende que é UTF8 ao abrir
                file.write('\ufeff')

                file.write('dataCota;nomeFundo;dtInicio;taxaAdm;cota;classe\n')

    def inicia_navegador(self):
        try:
            svc = Service(executable_path='./driver/geckodriver.exe', log_path='')
            self.driver = webdriver.Firefox(service=svc)
            logging.info('Navegador aberto com sucesso')
        except WebDriverException as e:
            logging.critical(f'Falha: {e}')
            sys.exit("Falha critica, consulte o log")

    def encerra_navegador(self):
        try:
            self.driver.close()
            logging.info('Navegador encerrado com sucesso')
        except Exception as e:
            logging.critical(f'Falha: {e}')
            sys.exit("Falha critica, consulte o log")


URL = ('https://www.caixavidaeprevidencia.com.br/'
       'previdencia/rendimento-dos-fundos')
SLEEP = 6
NIVEL_LOG = logging.INFO

scraper = ScraperPrev(URL, SLEEP, NIVEL_LOG)
