import re


def extractor(teste):
    teste = str(teste)
    texto = teste.split("<TABLE")
    for i in texto:
        if re.search('<span id="lblRetorno">', i):
            recorte = i.replace('\t\t\t\t\t\t\t\t<span id="lblRetorno">', '')
            recorte = recorte.replace('</span>', '')
            recorte = recorte.replace('border="0" width="90%" align="center">', '')
            recorte = recorte.replace('\r\n\t\t\t\t\t<TR>', '')
            recorte = recorte.replace('\r\n\t\t\t\t\t\t<TD>', '')
            recorte = recorte.strip()
            initial_position = recorte.find('<P align="justify">')
            final_position = recorte.find('</P>')
            recorte = recorte[initial_position:final_position + 4]
            break
    return recorte

def getSchema(identificacao, bloco, nome_campo1 , nome_campo2 , nome_campo3 , campo1, campo2, campo3):
    sb = []
    sb.append('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
    sb.append('<Site>\n')
    sb.append('\t<Identificacao>')
    sb.append(identificacao)
    sb.append('</Identificacao>\n')
    sb.append('\t<Corpo>\n')
    sb.append('\t\t<L nome="' + bloco + '">\n')
    sb.append('\t\t\t<B>\n')
    sb.append('\t\t\t\t<C nome ="' + nome_campo1 + '">')
    sb.append(campo1)
    sb.append('</C>\n')
    sb.append('\t\t\t\t<C nome ="' + nome_campo2 + '">')
    sb.append(campo2)
    sb.append('</C>\n')
    sb.append('\t\t\t\t<C nome ="' + nome_campo3 + '">')
    sb.append(campo3)
    sb.append('</C>\n')
    sb.append('\t\t\t</B>\n')
    sb.append('\t\t</L>\n')
    sb.append('\t</Corpo>\n')
    sb.append('</Site>')

    return ''.join(sb)

class BuilderXMLret:

    def builder_xml_ret(html):
        html = html
        infor_registro = ''
        dados_liberacao = ''
        mensagem = ''
        recorded = extractor(html)
        initial_position = recorded.find('<P align="justify">&nbsp;')
        final_position = recorded.find('</P>')
        recorded = recorded[initial_position + 25:final_position].strip()
        array = recorded.split('<BR>')

        for i in array:
            if re.search('Veículo placa', i):
                infor_registro = i
            elif re.search('A liberação DO veículo', i) or re.search('A liberação DO veículo', i) or re.search('De segunda a sexta-feira', i) or re.search('    DETRAN', i)  or re.search('2\)', i) or re.search('O proprietário deverá', i):
                dados_liberacao += i
            elif re.search('O veículo será liberado', i):
                mensagem = i

        xml = getSchema('GUINCHADOSPREFEITURASP', 'Registro', 'inforRegistro', 'dadosLiberacao', 'mensagem', infor_registro, dados_liberacao, mensagem)

        print(xml)
    # html = open('../texto.html', 'r')
    # teste = html.readlines()

    # print(recorte)
