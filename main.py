from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import logging
import sys


class ScraperPrev():

    def __init__(self, url: str, sleep: int = 5):
        self.configura_log()
        self.lista_datas = self.busca_data()
        self.url = url
        self.sleep = sleep
        self.browser = None
        self.inicia_navegador()
        self.encerra_navegador()

    @staticmethod
    def configura_log():
        logging.basicConfig(
            filename='./log/log.txt',
            filemode='w',
            level=logging.DEBUG,
            format=('%(asctime)s.%(msecs)03d'
                    '%(levelname)8s %(module)s: %(message)s'),
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def busca_data(self):
        lista_datas = []
        with open('./data/input', 'r') as reader:
            for line in reader.readlines():
                lista_datas.append(line.split())

        logging.info('Processo de buscar datas concluido')
        return lista_datas

    def inicia_navegador(self):
        try:
            options = Options()
            options.binary_location = ('C:/Program Files/'
                                       'Mozilla Firefox/firefox.exe')
            self.browser = webdriver.Firefox(
                options=options, executable_path='./driver/geckodriver.exe')
        except:
            logging.critical('Falha na carga do driver do navegador')
            sys.exit('Falha no carregamento do driver ou localizacao '
                     'do path firefox')

        logging.info('Driver do navegador iniciado')
        self.browser.implicitly_wait(self.sleep)
        self.browser.get(self.url)

        if self.browser.title == '502 Bad Gateway':
            self.browser.quit()
            logging.critical('Falha no carga da pagina, error: 502 BADGATEWAY')
            sys.exit('Falha no carregamento da pagina, error: 502 BAD GATEWAY')

        logging.info('Pagina aberta com sucesso')
        return

    def encerra_navegador(self):
        self.browser.quit()
        logging.info('Navegador encerrado com sucesso')


URL = 'https://www.caixavidaeprevidencia.com.br/ \
        previdencia/rendimento-dos-fundos'
SLEEP = 6

scraper = ScraperPrev(URL, SLEEP)
