import re


def extractor(test):
    test_str = str(test)
    text = test_str.split("<TABLE")
    for i in text:
        if re.search('<span id="lblRetorno">', i):
            cut = i.replace('\t\t\t\t\t\t\t\t<span id="lblRetorno">', '')
            cut = cut.replace('</span>', '')
            cut = cut.replace('border="0" width="90%" align="center">', '')
            cut = cut.replace('\r\n\t\t\t\t\t<TR>', '')
            cut = cut.replace('\r\n\t\t\t\t\t\t<TD>', '')
            cut = cut.strip()
            initial_position = cut.find('<P align="justify">')
            final_position = cut.find('</P>')
            cut = cut[initial_position:final_position + 4]
            break
    return cut


def get_schema(identificacao, bloco, nome_campo1, nome_campo2, nome_campo3, campo1, campo2, campo3):
    sb = ['<?xml version="1.0" encoding="ISO-8859-1"?>\n', '<Site>\n', '\t<Identificacao>', identificacao,
          '</Identificacao>\n', '\t<Corpo>\n', '\t\t<L nome="' + bloco + '">\n', '\t\t\t<B>\n',
          '\t\t\t\t<C nome ="' + nome_campo1 + '">', campo1, '</C>\n', '\t\t\t\t<C nome ="' + nome_campo2 + '">',
          campo2, '</C>\n', '\t\t\t\t<C nome ="' + nome_campo3 + '">', campo3, '</C>\n', '\t\t\t</B>\n', '\t\t</L>\n',
          '\t</Corpo>\n', '</Site>']

    return ''.join(sb)


class BuilderXmlRet:

    def __init__(self, html):
        self.html = html
        self.builder_xml_ret(html)

    def builder_xml_ret(self, html):
        html = html
        info_reg = ''
        data_liberation = ''
        message = ''
        recorded = extractor(html)
        initial_position = recorded.find('<P align="justify">&nbsp;')
        final_position = recorded.find('</P>')
        recorded = recorded[initial_position + 25:final_position].strip()
        if re.search('Veículo não se encontra no pátio', recorded):
            recorded = '0222 - NÃO ENCONTRADO'
            print(recorded)
        else:
            array = recorded.split('<BR>')

            for i in array:
                if re.search('Veículo placa', i):
                    info_reg = i
                elif re.search('A liberação DO veículo', i) or re.search('A liberação DO veículo', i) or re.search(
                        'De segunda a sexta-feira', i) or re.search('    DETRAN', i) or re.search('2\)',
                                                                                                  i) or re.search(
                    'O proprietário deverá', i):
                    data_liberation += i
                elif re.search('O veículo será liberado', i):
                    message = i

            xml = get_schema('GUINCHADOSPREFEITURASP', 'Registro', 'inforRegistro', 'dadosLiberacao', 'message',
                             info_reg, data_liberation, message)
            print(xml)
