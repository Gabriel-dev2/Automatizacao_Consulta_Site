import requests
import re
import builder.builderXMLret

class Site:

    html = requests.request('GET', 'http://www3.prefeitura.sp.gov.br/smt/pesqveic/Pesquisa.aspx')
    viewstate = ''
    viewstategenerator = ''
    placa = 'DRG3560'  # LLY9200
    cookie = html.cookies
    temp = ''
    if re.search('<RequestsCookieJar', str(cookie)):
        temp = str(cookie)
        temp = temp.replace('<RequestsCookieJar[<Cookie ', '')
        temp = temp.replace(' for www3.prefeitura.sp.gov.br/>]>', '')

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

    viewstate = retorno.replace('" />', '')
    viewstate = viewstate.replace('\r\n\r\n', '')

    viewstategenerator = retorno2.replace('" />', '')
    viewstategenerator = viewstategenerator.replace('\r\n\t', '')

    HEADERS = {'Host': 'www3.prefeitura.sp.gov.br',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
               'Accept-Encoding': 'gzip, deflate',
               'Referer': 'http://www3.prefeitura.sp.gov.br/smt/pesqveic/Pesquisa.aspx',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Connection': 'close',
               'Cookie': temp,
               'Upgrade-Insecure-Requests': '1'}

    PARAMS = {'PageProdamSPOnChange': '',
              'PageProdamSPPosicao': 'Form=0;0/',
              'PageProdamSPFocado': 'btnPesquisar',
              '__VIEWSTATE': viewstate,
              '__VIEWSTATEGENERATOR': viewstategenerator,
              'txtPlaca': placa,
              'btnPesquisar': 'Pesquisar'}

    response = requests.post(url='http://www3.prefeitura.sp.gov.br/smt/pesqveic/Pesquisa.aspx', headers=HEADERS,
                             data=PARAMS)

   # arquivo = open('texto.html', 'w')

    #arquivo.write(response.text)
    html = response.text
    builder.builderXMLret.BuilderXMLret.builder_xml_ret(html)

