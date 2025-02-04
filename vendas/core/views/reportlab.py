import io
import locale
from django.shortcuts import get_object_or_404, redirect
from django.http import FileResponse
from django.contrib import messages
from datetime import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import cm, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from  vendas.users.models import User
from ..models import Venda, Cadastro,Setor 
from ..models import ItemVEN, Produto, CondPag
'''
Para chegar as cores RGB, neste caso, é necessário realizar a divisão 
do valor individual de cada um (vermelho, verde e branco) e dividí-lo
por 256. Com isso um número decimal é gerado, qual será utilizado como
parâmetro para a rotina setFillColorRGB.

'''

locale.setlocale(locale.LC_ALL, '')
def formataValor(valor):
    return "R$ {}".format(locale.format("%.2f",valor,grouping=True,monetary=True))

def controle_interno(request,pk):
    #logging.debug()
    venda = get_object_or_404(Venda,pk=pk)
    #logging.debug()
    cliente = get_object_or_404(Cadastro,pk=venda.cliente_ven.codigo_cad)
    #logging.debug()
    vendedor = get_object_or_404(User,pk=venda.usuario_ven.id)
    #logging.debug()
    empresaVenda = get_object_or_404(Setor,pk=vendedor.setor_usu.key_setor)
    #logging.debug()
    itens = ItemVEN.objects.filter(num_ven_ite=pk)
    #logging.debug()

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer,pagesize=A4,bottomup=1,pageCompression=0,verbosity=0,)
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    pdfmetrics.registerFont(TTFont('ArialBd', 'ArialBd.ttf'))
    p.setFont("Arial", 11)    
    p.setTitle(f'Venda_{venda.numero_ven}_{cliente.nome_cad}')
    def cabecalho_pdf(self): # altura 800 até 740
        p.drawImage('./vendas/core/static/img/Controle Interno.bmp', -60, 746, width=None,height=None,mask=None)
#        p.drawImage(f'media/{request.user.user_profile.setor_usu.Foto_Cabec_Tela_SET.cabec}', 10, 746, width=None,height=None,mask=None)
        p.drawString(510,815,'Folha ')
        p.drawRightString(584, 815, f'{str(p.getPageNumber())}')
        p.drawString(510,800,'Data ')
        p.drawRightString(584, 800, f'{datetime.today().strftime("%d/%m/%y")}')
        p.drawString(510,785,'Hora ')
        p.drawRightString(584, 785, f'{datetime.today().strftime("%H:%M")}')
# GERAL VENDA
        p.rect(9, 675, 190, 65, stroke=1, fill=0)
        p.drawString(12, 725, f'Número da venda: {str(venda.numero_ven)}')
        p.drawString(12, 710, f'Data da venda: {venda.get_data_ven()}') 
        p.drawString(147, 710, f'{venda.get_hora_ven()}')         
        p.drawString(12, 695, f'Vendedor: {vendedor.username}')
        p.drawString(12, 680, f'Veículo: {venda.placa_veic if venda.placa_veic != None else ""}')
# GERAL EMPRESA
        p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
        p.rect(190, 675, 395, 65, stroke=1, fill=1)
        p.setFillColor('black')
        p.setFont("ArialBd",24)
        p.drawCentredString(388/2+200, 718, f'{cliente.nome_cad}')
        p.setFont("Arial",11)
        p.drawString(203, 700, f'Endereço: {cliente.rua1_cad}')
        p.drawRightString(582, 700, f'Bairro: {cliente.bairro1_cad}')
        p.drawString(203, 685, f'CNPJ: {cliente.cgc_cpf_cad}')
        p.drawString(350, 685, f'Telefone: {cliente.telefone1_cad}')
        p.drawRightString(582, 685, f'CEP: {cliente.cep1_cad}')

    def cliente_pdf(self):
# GERAL CLIENTE        
        p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
        p.rect(9, 615, 576, 55, stroke=1, fill=1)
        p.setFillColor('black')
        p.drawString(12, 655, f'Cliente: {cliente.nome_cad}')
        p.drawString(288, 655, f'Código: {cliente.codigo_cad}')
        p.drawRightString(581, 655, f'Placa: {cliente.placa_vei_cad if cliente.placa_vei_cad != None else ""}')
        p.drawString(12, 640, f'Endereço: {cliente.rua1_cad}')
        p.drawString(288, 640, f'Bairro: {cliente.bairro1_cad}')
        p.drawString(434, 640, f'Cidade: {cliente.cidade1_cad}')
        p.drawRightString(581, 640, f'UF: {cliente.estado1_cad}')
        p.drawString(11, 625, f'CNPJ: {cliente.cgc_cpf_cad}')
        p.drawString(170, 625, f'RG: {cliente.ie_cad}')
        p.drawString(288, 625, f'Telefone: {cliente.telefone1_cad}')
        p.drawString(434, 625, f'{cliente.telefone2_cad if cliente.telefone2_cad != None else ""}')
        p.drawRightString(581, 625, f'CEP: {cliente.cep1_cad}')

    def produto_cabec_pdf(self):
        p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
        p.rect(9, 590, 43, 20, stroke=1, fill=1) # codigo
        p.rect(52, 590, 60, 20, stroke=1, fill=1) # sigla
        p.rect(112, 590, 255, 20, stroke=1, fill=1) # nome
        p.rect(367, 590, 25, 20, stroke=1, fill=1) # un
        p.rect(392, 590, 42, 20, stroke=1, fill=1) # quant
        p.rect(434, 590, 74, 20, stroke=1, fill=1) # unit
        p.rect(508, 590, 77, 20, stroke=1, fill=1) # total
        p.setFillColor('blue')
        p.setFont("ArialBd",11)
        p.drawString(11, 597, "Código")
        p.drawString(56, 597, "Sigla Fáb.")
        p.drawString(186, 597, "Nome Produto / Serviço")
        p.drawString(371, 597, "UN")
        p.drawString(396, 597, "Quant.")
        p.drawString(444, 597, "Valor Unit.")
        p.drawString(519, 597, "Valor Total")
        p.setFont("Arial",11)
        p.setFillColor('black') # voltar cor preta

    def rodape_pdf(self, alt_ini):
        valorTotal = 0
        for i in range(itens.count()):
            valorTotal += itens[i].quantidade_ite * itens[i].unitario_ite
        p.rect(9, alt_ini-60, 425, 60, stroke=1, fill=0) # executores
        p.drawString(12, alt_ini-13, f'{venda.obs_ven if venda.obs_ven != None else ""}')
# TOTAL GERAL
        p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
        p.rect(434, alt_ini-20, 74, 20, stroke=1, fill=1) # total geral
        p.rect(508, alt_ini-20, 77, 20, stroke=1, fill=1) # total geral valor
        p.setFillColor('black')
        p.setFont("ArialBd",11)
        p.drawString(443, alt_ini-13, "Total Geral")
        p.drawRightString(582,alt_ini-13,f'{formataValor(valorTotal)}')
# DESCONTO
        p.rect(434, alt_ini-40, 74, 20, stroke=1, fill=0) # desconto
        p.rect(508, alt_ini-40, 77, 20, stroke=1, fill=0) # desconto valor
        p.setFont("Arial",11)
        p.drawString(448, alt_ini-34, "Desconto")
        p.drawRightString(582,alt_ini-34,f'{formataValor(venda.desconto_ven)}') 
# TOTAL FINAL
        p.setFillColorRGB(0.390625, 0.8984375, 0.99609375)
        p.rect(434, alt_ini-60, 74, 20, stroke=1, fill=1) # total final
        p.rect(508, alt_ini-60, 77, 20, stroke=1, fill=1) # total final valor
        p.setFillColor('black')
        p.setFont("ArialBd",11)
        p.drawString(444, alt_ini-54, "Total Final")
        p.drawRightString(582,alt_ini-54,f'{formataValor(valorTotal - venda.desconto_ven)}')
# EXECUTORES
        p.setFont("Arial",11)
        alt_ini -= 65
        alt_fim = alt_ini-85
        p.rect(9, alt_fim, 576, alt_ini-alt_fim, stroke=1, fill=0)
        p.drawString(12, alt_ini-15, f'')
        p.drawString(12, alt_ini-30, f'')
        p.drawString(12, alt_ini-45, f'')
        p.drawString(12, alt_ini-60, f'')
        p.drawString(12, alt_ini-75, f'')
# TOTAL PRODUTO / SERVIÇO
        p.setFillColorRGB(0.90625, 0.9375, 0.9453125)
        p.rect(390, alt_ini-50, 174, 40, stroke=1, fill=1)
        p.setFillColor('black')
        p.drawString(395, alt_ini-25, f'Total de produtos:')
        p.drawRightString(561,alt_ini-25,f'{formataValor(venda.tot_pecas) if venda.tot_pecas != None else ""}')
        p.drawString(395, alt_ini-40, f'Total de serviços:')
        p.drawRightString(561,alt_ini-40,f'{formataValor(venda.tot_servicos) if venda.tot_servicos != None else ""}')
# CONDIÇÃO
        p.setFillColorRGB(0.90625, 0.9375, 0.9453125)
        p.rect(390, alt_ini-75, 174, 20, stroke=1, fill=1)
        p.setFillColor('black')
        p.drawString(395, alt_ini-68, f'Cond. {venda.condicao_ven if venda.condicao_ven != None else ""}')
# RODAPÉ
        alt_ini = alt_ini - 190
        p.drawImage('./vendas/core/static/img/Rodape QuickReport.bmp', 0, alt_ini, width=None,height=None,mask=None)
        p.drawImage('./vendas/core/static/img/Rodapé Relatorios Cecotein novo.bmp', 9, alt_ini+20, width=None,height=None,mask=None)
        p.drawString(510, alt_ini+80, f'Sistema ')
        p.drawRightString(584, alt_ini+80, f'0180')
        p.drawString(510,alt_ini+60,f'Tela ')
        p.drawRightString(584,alt_ini+60,f'000-1')
        p.drawString(510,alt_ini+40,'Versão ')
        p.drawRightString(584,alt_ini+40,'1.0')

    def gera_produtos_pdf(self):
        alt_ini = 590
        alt_fim = alt_ini - 20
        for i in range(itens.count()):
            # Responsável pelo desenho da grade dos produtos
            p.rect(9, alt_fim, 43, alt_ini-alt_fim, stroke=1, fill=0) # código
            p.rect(52, alt_fim, 60, alt_ini-alt_fim, stroke=1, fill=0) # sigla
            p.rect(112, alt_fim, 255, alt_ini-alt_fim, stroke=1, fill=0) # nome
            p.rect(367, alt_fim, 25, alt_ini-alt_fim, stroke=1, fill=0) # un
            p.rect(392, alt_fim, 42, alt_ini-alt_fim, stroke=1, fill=0) # quant
            p.rect(434, alt_fim, 74, alt_ini-alt_fim, stroke=1, fill=0) # valor unit
            p.rect(508, alt_fim, 77, alt_ini-alt_fim, stroke=1, fill=0) # valor total

            # Responsável pelo desenho das informações dos produtos
            produto = Produto.objects.get(produto_pro=itens[i].produto_ite_id)
            p.drawString(12, (alt_ini-13), f'{produto.produto_pro}')
            p.drawString(56, alt_ini-13, f'{produto.sigla_fab_pro if produto.sigla_fab_pro != None else ""}')
            p.drawString(116, alt_ini-13, f'{produto.descricao_pro[0:35]}')
            p.drawString(371, alt_ini-13, f'{produto.unidade_pro}')
            p.drawString(398, alt_ini-13, f'{itens[i].quantidade_ite}')
            p.drawRightString(505, alt_ini-13, f'{formataValor(itens[i].unitario_ite)}')
            p.drawRightString(582, alt_ini-13, f'{formataValor(itens[i].quantidade_ite * itens[i].unitario_ite)}')
            alt_ini -= 20

            '''
            Ajuste para finalização e início de nova página, quando quantidade de produtos ultrapassa o tamanho
            o tamanho máximo de linhas permitidas. O reinício da folha se dá com a inclusão de cabeçalho, novamente,
            e continuação da sequência de itens.

            '''
            if alt_ini < 60:
                p.showPage()
                cabecalho_pdf(self)
                produto_cabec_pdf(self)
                alt_ini = 673

        '''
        A última fileira da grade não estava aparecendo, portanto, para que essa fosse desenhada corretamente 
        no documento foi necessário adicionar as linhas abaixo para realização do ajuste. É apenas uma cópia
        simples das linhas acima com o ajuste correto de altura.

        '''
        p.rect(9, alt_fim, 43, alt_ini-alt_fim, stroke=1, fill=0)
        p.rect(52, alt_fim, 60, alt_ini-alt_fim, stroke=1, fill=0)
        p.rect(112, alt_fim, 255, alt_ini-alt_fim, stroke=1, fill=0)
        p.rect(367, alt_fim, 25, alt_ini-alt_fim, stroke=1, fill=0)
        p.rect(392, alt_fim, 42, alt_ini-alt_fim, stroke=1, fill=0)
        p.rect(434, alt_fim, 74, alt_ini-alt_fim, stroke=1, fill=0)
        p.rect(508, alt_fim, 77, alt_ini-alt_fim, stroke=1, fill=0)

        rodape_pdf(self, alt_ini)        

    cabecalho_pdf(p)
    cliente_pdf(p)
    produto_cabec_pdf(p)
    gera_produtos_pdf(p)

    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename=f'Venda_{venda.numero_ven}_{cliente.nome_cad}.pdf')


def cupom_fiscal(request,pk):
    # Variáveis
    alt_ini = 55
    tf = 7 # Tamanho da fonte
    pl = 8 # Pulo de linha

    # Consultas ao banco de dados
    venda = get_object_or_404(Venda,pk=pk)
    cliente = get_object_or_404(Cadastro,pk=venda.cliente_ven.codigo_cad)
    vendedor = get_object_or_404(User,pk=venda.usuario_ven.id)
    print(vendedor.setor_usu.cod_emp_para_nfe_setor)
    empresaVenda = get_object_or_404(Cadastro,pk=vendedor.setor_usu.cod_emp_para_nfe_setor)
    itens = ItemVEN.objects.filter(num_ven_ite=pk)
    condicao = CondPag.objects.get(pk=venda.formapag_ven_id) if venda.formapag_ven != None else "Dinheiro"

    # Verifica se é Cupom Fiscal de Consumidor Eletrônica (65) ou Nota Fiscal Eletrônica
    if request.method == 'GET' and int(venda.modelo_nf_ven) != 65:
        messages.warning(request,'Nota Fiscal de Consumidor Eletrônica só pode ser emitida para Modelo NF igual a 65. (Escolha um modelo válido: 55 - NFe, 65 - NFCe)')
        return redirect('core:detalhe_venda',pk)

    # Definições da página
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer,pagesize=(7.9*cm,0*cm),bottomup=0,pageCompression=0,verbosity=0,)
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    pdfmetrics.registerFont(TTFont('ArialBd', 'ArialBd.ttf'))
    p.setFont("Arial",tf)    
    p.setTitle(f'Venda_{venda.numero_ven}_{cliente.nome_cad}')
    print("1"  + cliente.nome_cad)
    p.drawImage('./vendas/core/static/img/logo_cabecalho.bmp',62.5,5,width=100,height=50,preserveAspectRatio=True,mask=None)

    def cabecalho_cupom(self,alt_ini):
        p.drawCentredString(224/2, alt_ini+pl, f'{empresaVenda.razao_cad} - Fone: {empresaVenda.telefone1_cad}')
        p.drawCentredString(224/2, alt_ini+pl*2, f'CNPJ: {empresaVenda.cgc_cpf_cad} - EI: {empresaVenda.ie_cad}')
        p.drawCentredString(224/2, alt_ini+pl*3, f'{empresaVenda.rua1_cad} - {empresaVenda.bairro1_cad}')
        p.drawCentredString(224/2, alt_ini+pl*4, f'{empresaVenda.cidade1_cad} - {empresaVenda.estado1_cad}')
        p.line(0,alt_ini+pl*4.5,224,alt_ini+pl*4.5)
        p.setFont('ArialBd',tf)
        p.drawCentredString(224/2, alt_ini+pl*5.5, f'DANFE NFC-e Documento Auxiliar')
        p.drawCentredString(224/2, alt_ini+pl*6.5, f'da Nota Fiscal de Consumidor Eletrônica')
        p.setFont('Arial',tf)
        p.drawCentredString(224/2, alt_ini+pl*7.5, f'Não permite aproveitamento de crédito do ICMS')
        p.line(0,alt_ini+pl*8,224,alt_ini+pl*8)
        p.drawString(9,alt_ini+pl*9,'CÓDIGO')
        p.drawString(79,alt_ini+pl*9,'DESCRIÇÃO')
        p.drawString(45,alt_ini+pl*10,'QTD UN')
        p.drawString(93,alt_ini+pl*10,'VL. UNIT')
        p.drawRightString(215,alt_ini+pl*10,'VL. TOTAL')
        p.line(0,alt_ini+pl*10.5,224,alt_ini+pl*10.5)
        return alt_ini+pl*11.5

    def itens_cupom(self,alt_ini):
        qtd_total_itens = 0
        valor_produtos = 0
        for i in range(itens.count()):
            produto = Produto.objects.get(produto_pro=itens[i].produto_ite_id)
            qtd_total_itens += itens[i].quantidade_ite
            valor_produtos += itens[i].quantidade_ite * itens[i].unitario_ite
            p.drawString(9,alt_ini,f'{produto.produto_pro}')
            p.drawString(79,alt_ini,f'{produto.descricao_pro[0:28]}')            
            p.drawString(45,alt_ini+pl,f'{itens[i].quantidade_ite} {produto.unidade_pro}')
            p.drawString(93,alt_ini+pl,f'{formataValor(itens[i].unitario_ite)}')
            p.drawRightString(215,alt_ini+pl,f'{formataValor(itens[i].quantidade_ite * itens[i].unitario_ite)}')
            alt_ini += pl*2
        p.line(0,alt_ini-pl*0.5,224,alt_ini-pl*0.5)
        p.drawString(9,alt_ini+pl*0.5,f'QTD. TOTAL DE ITENS')
        p.drawRightString(215,alt_ini+pl*0.5,f'{qtd_total_itens}')
        return alt_ini + pl*2

    def resumo_venda_cupom(self,alt_ini):
        valor_produtos = 0
        for i in range(itens.count()):
            produto = Produto.objects.get(produto_pro=itens[i].produto_ite_id)
            valor_produtos += itens[i].quantidade_ite * itens[i].unitario_ite
        p.drawString(9,alt_ini,'Valor Produtos')
        p.drawRightString(215,alt_ini,f'{formataValor(valor_produtos)}')
        p.drawString(9,alt_ini+pl,'Descontos')
        p.drawRightString(215,alt_ini+pl,f'{formataValor(venda.desconto_ven)}')
        p.drawString(9,alt_ini+pl*2,'Acréscimos')
        p.drawRightString(215,alt_ini+pl*2,f'{formataValor(venda.acrescimo_ven)}')
        p.drawString(9,alt_ini+pl*3,'VALOR A PAGAR')
        p.drawRightString(215,alt_ini+pl*3,f'{formataValor((valor_produtos - venda.desconto_ven + venda.acrescimo_ven))}')
        alt_ini += pl*4.5
        p.drawString(9,alt_ini,'FORMA DE PAGAMENTO')
        p.drawRightString(215,alt_ini,'VALOR')
        p.drawString(9,alt_ini+pl,f'{condicao.descricao if venda.condicao_ven != None else "Dinheiro"}')
        p.drawRightString(215,alt_ini+pl,f'valor')
        p.drawString(9,alt_ini+pl*2,f'Troco')
        p.drawRightString(215,alt_ini+pl*2,f'valor')
        p.line(0,alt_ini+pl*2.5,224,alt_ini+pl*2.5)
        return alt_ini + pl*3.5

    def detalhe_venda_cupom(self,alt_ini):
        p.drawString(9,alt_ini,f'Número da venda {venda.numero_ven} Código do cliente {venda.cliente_ven.codigo_cad}')
        p.drawString(9,alt_ini+pl,f'*Trib aprox R$: {venda.irrf_ven + venda.pis_ven + venda.cofins_ven + venda.csll_ven} Federal {0.0} Estadual* Fonte: IBPT')
        p.line(0,alt_ini+pl*2,224,alt_ini+pl*2)
        return alt_ini + pl*3

    def mensagem_fiscal_cupom(self,alt_ini):
        p.setFont('ArialBd',tf)
        p.drawCentredString(224/2,alt_ini,'ÁREA DE MENSAGEM FISCAL')
        p.setFont('Arial',tf)
        p.drawCentredString(224/2,alt_ini+pl*1.5,f'Número: {venda.nf_ven:09} - Série: {venda.serie_nf_ven:03}')
        p.drawCentredString(224/2,alt_ini+pl*2.5,f'Emissão {venda.datanfsai_ven.strftime("%d/%m/%Y")} {venda.horanfsai_ven.strftime("%H:%M:%S")} - Via Estabelecimento')
        p.line(0,alt_ini+pl*3,224,alt_ini+pl*3)
        return alt_ini + pl*4

    def chave_acesso_cupom(self,alt_ini):
        p.drawCentredString(224/2,alt_ini,'Consulte pela chave de acesso em:')
        p.drawCentredString(224/2,alt_ini+pl,'http://nfce.fazenda.mg.gov.br/portalnfce')
        p.setFont('ArialBd',tf)
        p.drawCentredString(224/2,alt_ini+pl*2.5,'CHAVE DE ACESSO')
        p.setFont('Arial',tf)
        p.drawCentredString(224/2,alt_ini+pl*4,f'{venda.chave_acesso_nfe_ven}')
        p.line(0,alt_ini+pl*4.5,224,alt_ini+pl*4.5)
        return alt_ini + pl*5.5

    def consumidor_cupom(self,alt_ini):
        p.setFont('ArialBd',tf)
        p.drawCentredString(224/2,alt_ini,'CONSUMIDOR')
        p.setFont('Arial',tf)

        if venda.cliente_ven != 538:
            p.drawCentredString(224/2,alt_ini+pl*1.5,f'CONSUMIDOR CNPJ:{venda.cliente_ven.cgc_cpf_cad} {venda.cliente_ven.razao_cad}')
            p.drawCentredString(224/2,alt_ini+pl*2.5,f'{venda.cliente_ven.rua1_cad}')
            p.drawCentredString(224/2,alt_ini+pl*3.5,f'{venda.cliente_ven.bairro1_cad} - {venda.cliente_ven.cidade1_cad}/{venda.cliente_ven.estado1_cad}')
            p.line(0,alt_ini+pl*4,224,alt_ini+pl*4)
            return alt_ini + pl*5
        else:    
            p.drawCentredString(224/2,alt_ini+pl*1.5,f'{venda.cliente_ven if venda.cliente_ven != None else "CONSUMIDOR NÃO IDENTIFICADO"}')
            p.line(0,alt_ini+pl*2,224,alt_ini+pl*2)
            return alt_ini + pl*3


    def protocolo_cupom(self,alt_ini):
        p.drawCentredString(224/2,alt_ini,'Consulta via leitor de QR Code')
        p.drawCentredString(224/2,alt_ini+pl*1.5,'Protocolo de Autorização')
        p.drawCentredString(224/2,alt_ini+pl*3,f'{venda.protocolo_nfe_ven} {venda.datanfsai_ven.strftime("%d/%m/%Y")} {venda.horanfsai_ven.strftime("%H:%M:%S")}')
        p.line(0,alt_ini+pl*3.5,224,alt_ini+pl*3.5)
        return alt_ini + pl*4.5

    alt_ini = cabecalho_cupom(p,alt_ini)
    alt_ini = itens_cupom(p,alt_ini)
    alt_ini = resumo_venda_cupom(p,alt_ini)
    alt_ini = detalhe_venda_cupom(p,alt_ini)
    alt_ini = mensagem_fiscal_cupom(p,alt_ini)
    alt_ini = chave_acesso_cupom(p,alt_ini)
    alt_ini = consumidor_cupom(p,alt_ini)
    alt_ini = protocolo_cupom(p,alt_ini)

    p.setPageSize((7.9*cm,(alt_ini/28)*cm)) # Utilizado para alterar o tamanho da página antes da impressão
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer,as_attachment=False,filename=f'Cupom_{venda.numero_ven}_{cliente.nome_cad}.pdf')

def cupom(request, pk):
    # Variáveis
    alt_ini = 30
    tf = 8 # Tamanho da fonte
    pl = 10 # Pulo de linha
    vendas  = Venda.objects.all().order_by('pk')
    # Consultas ao banco de dados
    venda = get_object_or_404(Venda,pk=pk)
  
    print(venda.usuario_ven.setor_usu.cod_emp_para_nfe_setor)
    print(venda.formapag_ven_id)
    cliente = get_object_or_404( Cadastro,pk=venda.cliente_ven.codigo_cad)
    vendedor = get_object_or_404(User,pk=venda.usuario_ven.id)
    empresaVenda = get_object_or_404( Cadastro,pk=venda.cliente_ven.codigo_cad)#vendedor.setor_usu.cod_emp_para_nfe_setor)
    itens = ItemVEN.objects.filter(num_ven_ite=pk)
    condicao = CondPag.objects.get(pk=venda.formapag_ven_id) if venda.formapag_ven != None else "Dinheiro"

    # Definições da página
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer,pagesize=(7.9*cm,0*cm),bottomup=0,pageCompression=0,verbosity=0,)
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    pdfmetrics.registerFont(TTFont('ArialBd', 'ArialBd.ttf'))
    p.setFont("Arial",tf)    
    p.setTitle(f'Venda_{venda.numero_ven}_{cliente.nome_cad}')
    print("2"+cliente.nome_cad)
    def cabecalho_cupom(self,alt_ini):
        p.line(0,alt_ini,224,alt_ini)
        p.line(0,alt_ini+1.1,224,alt_ini+1.1)
        p.drawString(7,alt_ini+pl,f'{cliente.nome_cad}')
        p.drawRightString(217,alt_ini+pl,f'Setor: {venda.setor_ven}')
        p.drawString(7,alt_ini+pl*2,f'{empresaVenda.rua1_cad}')
        p.drawString(7,alt_ini+pl*3,f'{empresaVenda.bairro1_cad}')
        p.drawString(90,alt_ini+pl*3,f'{empresaVenda.cidade1_cad}-{empresaVenda.estado1_cad}')
        p.drawString(7,alt_ini+pl*4,f'CNPJ {empresaVenda.cgc_cpf_cad} EI {empresaVenda.ie_cad}')
        p.drawString(7,alt_ini+pl*5,f'{datetime.today().strftime("%d/%m/%Y")}          {datetime.today().strftime("%H:%M:%S")}         Num: {venda.numero_ven}')
        p.line(0,alt_ini+pl*5.5,224,alt_ini+pl*5.5)
        return alt_ini+pl*6.5

    def itens_cupom(self,alt_ini):
        produto = ''
        cont = 1
        p.drawString(7,alt_ini,'ITEM')
        p.drawString(35,alt_ini,'CODIGO')
        p.drawString(115,alt_ini,'DESCRICAO')
        p.drawString(45,alt_ini+pl,'UN.')
        p.drawString(70,alt_ini+pl,'PR.UNIT.')
        p.drawRightString(210,alt_ini+pl,'PRECO TOTAL')
        for i in range(itens.count()):
            produto = Produto.objects.get(produto_pro=itens[i].produto_ite_id)
            cont += 1
            p.drawString(7,alt_ini+(pl*cont),f'{i+1}')
            p.drawString(40,alt_ini+(pl*cont),f'{produto.produto_pro}')
            p.drawString(70,alt_ini+(pl*cont),f'{produto.descricao_pro[0:40]}')
            cont += 1
            p.drawString(21,alt_ini+(pl*cont),f'{itens[i].quantidade_ite}')
            p.drawString(45,alt_ini+(pl*cont),f'{produto.unidade_pro}')
            p.drawString(70,alt_ini+(pl*cont),f'{formataValor(itens[i].unitario_ite)}')
            p.drawString(115,alt_ini+(pl*cont),f'TOTAL:')
            p.drawRightString(210,alt_ini+(pl*cont),f'{formataValor(itens[i].quantidade_ite * itens[i].unitario_ite)}')
        cont += 1
        p.drawString(7,alt_ini+(pl*cont),f'---Localiz.:{123} Sigla:{132}')
        return alt_ini+pl*(cont+2)

    def consumidor_cupom(self,alt_ini):
        p.drawString(7,alt_ini,f'MINAS LEGAL 039134040803202296')
        p.drawString(7,alt_ini+pl,f'{cliente.nome_cad}')
        p.drawString(7,alt_ini+pl*2,f'{cliente.rua1_cad}')
        p.drawString(7,alt_ini+pl*3,f'BRASIL')
        p.drawString(100,alt_ini+pl*3,f'{cliente.cidade1_cad}-{cliente.estado1_cad}')
        p.line(0,alt_ini+pl*3.5,224,alt_ini+pl*3.5)
        return alt_ini+pl*4.5
        
    def subtotal_cupom(self,alt_ini):
        valor_produtos = 0
        for i in range(itens.count()):
            valor_produtos += itens[i].quantidade_ite * itens[i].unitario_ite
        p.drawString(7,alt_ini,'SUB-TOTAL')
        p.drawRightString(210,alt_ini,f'{formataValor(valor_produtos)}')
        p.drawString(7,alt_ini+pl*1,'DESCONTO')
        #modificado (retirada de venda.desconto) Davi Oliveira Tito 03/05/2022
        #teste para se realizar no dia 04/05/2022, modificação feita 03/05/2022 Davi Oliveira Tito
        #colocação de um if para ver se funciona e resolve o problema principal
        if (venda.desconto_ven == None):
           p.drawRightString(210,alt_ini+pl*1,f'{formataValor(0.00)}')#venda.desconto_ven)}')
        else:
           p.drawRightString(210,alt_ini+pl*1,f'{formataValor(venda.desconto_ven)}')
        #p.drawRightString(210,alt_ini+pl*1,f'{formataValor(0.00)}')#venda.desconto_ven)}')
        p.drawString(7,alt_ini+pl*2,f'VALOR RECEBIDO')
        p.drawRightString(210,alt_ini+pl*2,f'{formataValor(valor_produtos)}')
        p.drawString(7,alt_ini+pl*3,f'TROCO')
        p.drawRightString(210,alt_ini+pl*3,f'{formataValor( - valor_produtos + venda.desconto_ven + valor_produtos)}')
        p.drawString(7,alt_ini+pl*4,f'TOTAL GERAL')
        #Modificado (retirado + venda.acrescimo_ven) Rennan 03/05/2022
        #modificado(retirado venda.desconto) Davi O 03/05/2022
        p.drawRightString(210,alt_ini+pl*4,f'{formataValor((valor_produtos)   - venda.desconto_ven )}')#venda.desconto_ven)}')
        p.line(0,alt_ini+pl*4.5,224,alt_ini+pl*4.5)
        p.drawString(7,alt_ini+pl*5.5,'Data do Vencimento')
        p.drawRightString(210,alt_ini+pl*5.5,'Valor do Pagamento')
        p.drawString(7,alt_ini+pl*6.5,f'{venda.get_data_ven()}')
        #Modificado (retirado + venda.acrescimo_ven) Rennan 03/05/2022
        # modificado(retirado venda.desconto) Davi O 03/05/2022
        p.drawRightString(210,alt_ini+pl*6.5,f'{formataValor((valor_produtos) - venda.desconto_ven )}')
        p.line(0,alt_ini+pl*7,224,alt_ini+pl*7)
        return alt_ini+pl*8        

    def observacoes_cupom(self,alt_ini):
        p.drawString(7,alt_ini,'OBSERVAÇÕES:')
        count = len(venda.obs_ven) / 40 if venda.obs_ven != None else 0
        if count > 1:
            parada = 0
            i = 0
            while i < count:
                if i > 5:
                    break
                p.drawString(7,alt_ini+(pl*(i+1)),f'{venda.obs_ven[parada:parada+40]}')
                i += 1
                parada += 40
        else:            
           p.drawString(7,alt_ini+pl,f'{venda.obs_ven if venda.obs_ven != None else ""}')
        p.drawString(152,alt_ini+pl*7,'Versão:1.0')
        p.line(0,alt_ini+pl*6.7,150,alt_ini+pl*6.7)
        p.line(0,alt_ini+pl*6.8,150,alt_ini+pl*6.8)
        p.line(193,alt_ini+pl*6.7,224,alt_ini+pl*6.7)
        p.line(193,alt_ini+pl*6.8,224,alt_ini+pl*6.8)
        return alt_ini+pl*8

    def rodape_cupom(self,alt_ini):
        p.drawCentredString(224/2,alt_ini,'Não é Documento Fiscal')
        p.drawCentredString(224/2,alt_ini+pl,'Não é válido como garantia de mercadoria')
        p.drawString(78,alt_ini+pl*2,f'{datetime.today().strftime("%d/%m/%Y")} {datetime.today().strftime("%H:%M:%S")}')
        return alt_ini+pl*7

    alt_ini = cabecalho_cupom(p,alt_ini)
    alt_ini = itens_cupom(p,alt_ini)
    alt_ini = consumidor_cupom(p,alt_ini)
    alt_ini = subtotal_cupom(p,alt_ini)
    alt_ini = observacoes_cupom(p,alt_ini)
    alt_ini = rodape_cupom(p,alt_ini)

    p.setPageSize((7.9*cm,(alt_ini/28)*cm)) # Utilizado para alterar o tamanho da página antes da impressão
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer,as_attachment=False,filename=f'Cupom_{venda.numero_ven}_{cliente.nome_cad}.pdf')
