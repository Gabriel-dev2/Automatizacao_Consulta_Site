import requests
import re
import importlib

from builder.builderXMLret import BuilderXmlRet


# importlib.import_module('builder.builderXMLret.BuilderXmlRet')


def making_request(request_type, url, headers, params):
    if request_type == 'GET' and url == '' and headers == '' and params == '':
        response = requests.request('GET', url)
    else:
        response = requests.post(url=url, headers=headers,
                                 data=params)
    return response


class Site:

    def __init__(self, url, placa):
        self.url = url
        self.placa = placa
        self.submit_site(url, placa)

    def submit_site(self, url, placa):
        html = making_request('GET', url, '', '')
        view_state = ''
        view_state_generator = ''
        # placa = 'DRG3560'  # LLY9200
        cookie = html.cookies
        cookie_str = ''
        if re.search('<RequestsCookieJar', str(cookie)):
            cookie_str = str(cookie)
            cookie_str = cookie_str.replace('<RequestsCookieJar[<Cookie ', '')
            cookie_str = cookie_str.replace(' for www3.prefeitura.sp.gov.br/>]>', '')

        if html.text.find('<input type="hidden" name="__VIEWSTATE"'):
            array = html.text.split('<input')
            for i in array:
                if re.search('__VIEWSTATE"', i):
                    retorno = i.replace('type="hidden" name="__VIEWSTATE" value="', '')

        if html.text.find('<input type="hidden" name="__VIEWSTATE"'):
            array2 = html.text.split('<input')
            for a in array2:
                if re.search('__VIEWSTATEGENERATOR"', a):
                    retorno2 = a.replace('type="hidden" name="__VIEWSTATEGENERATOR" value="', '')
                    retorno2 = retorno2[:13]

        view_state = retorno.replace('" />', '')
        view_state = view_state.replace('\r\n\r\n', '')

        view_state_generator = retorno2.replace('" />', '')
        view_state_generator = view_state_generator.replace('\r\n\t', '')

        headers = {'Host': 'www3.prefeitura.sp.gov.br',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
                   'Accept-Encoding': 'gzip, deflate',
                   'Referer': 'http://www3.prefeitura.sp.gov.br/smt/pesqveic/Pesquisa.aspx',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Connection': 'close',
                   'Cookie': cookie_str,
                   'Upgrade-Insecure-Requests': '1'}

        params = {'PageProdamSPOnChange': '',
                  'PageProdamSPPosicao': 'Form=0;0/',
                  'PageProdamSPFocado': 'btnPesquisar',
                  '__VIEWSTATE': view_state,
                  '__VIEWSTATEGENERATOR': view_state_generator,
                  'txtPlaca': placa,
                  'btnPesquisar': 'Pesquisar'}

        response = making_request('POST', url, headers, params)

        # arquivo = open('texto.html', 'w')

        # arquivo.write(response.text)
        html = response.text
        BuilderXmlRet.__init__(html)
        print('passou')

        if __name__ == '__main__':
            Site.__init__(self, 'http://www3.prefeitura.sp.gov.br/smt/pesqveic/Pesquisa.aspx', 'DRG3560')
