import io
import locale
from django.shortcuts import get_object_or_404, redirect
from django.http import FileResponse
from django.contrib import messages
from datetime import datetime
from reportlab.pdfgen import canvas
from datetime import timedelta

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import cm, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime

from   vendas.users.models import User
from ..models import Mov_caixa,Setor
from ..forms import Mov_caixaForm
from ..mixins import CounterMixin 
from  vendas.users.models import User
from ..models import Venda, Cadastro,Setor 
from ..models import ItemVEN, Produto, CondPag, Titulos,Mov_caixa

locale.setlocale(locale.LC_ALL, '')
def formataValor(valor):
    return "R$ {}".format(locale.format("%.2f",valor,grouping=True,monetary=True))

def formataPorcent(valor):
    return "{}%".format(locale.format("%.2f",valor,grouping=True,monetary=True))
def mov_caixaM(request):
    alt_ini = 700
    data = datetime.today().strftime("%d/%m/%y") 
    troco = float(0.00)
    mov_caixa = Mov_caixa.objects.all().order_by('pk')
    #setor= mov_caixa.objects.filter(pk= object_list.cod_seto_mov_c).order_by(pk)
    buffer = io.BytesIO()
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer,pagesize=A4,bottomup=1,pageCompression=0,verbosity=0,)
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    pdfmetrics.registerFont(TTFont('ArialBd', 'ArialBd.ttf'))
    p.setFont("Arial", 11)    
    p.setTitle(f'Movimento de caixa ')
    def cabecalho_pdf(self): # altura 800 até 740
        p.drawImage('./vendas/core/static/img/mov_caixa.png', -360, 716, width=None,height=None,mask=None)
     #   p.drawImage(f'./{request.user.foto_emp.url}', 10, 766, 70,70,mask=None)
        p.drawString(510,815,'Folha ')
        p.drawRightString(584, 815, f'{str(p.getPageNumber())}')
        p.drawString(510,800,'Data ')
        p.drawRightString(584, 800, f'{datetime.today().strftime("%d/%m/%y")}')
        p.drawString(510,785,'Hora ')
        p.drawRightString(584, 785, f'{datetime.today().strftime("%H:%M")}')
# GERAL VENDA
     #   p.rect(9, 675, 190, 65, stroke=1, fill=0)
     #   p.drawString(12, 725, f'')
     #   p.drawString(12, 710, f'') 
     #   p.drawString(147, 710, f'')         
      #  p.drawString(12, 695, f'')
     #   p.drawString(12, 680, f'')
# GERAL EMPRESA
    #    p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
    #    p.rect(190, 675, 395, 65, stroke=1, fill=1)
    #    p.setFillColor('black')
    #    p.setFont("ArialBd",24)
    #    p.drawCentredString(388/2+200, 718, f'')
    #    p.setFont("Arial",11)
    #    p.drawString(203, 700, f': ')
    #    p.drawRightString(582, 700, f'Bairro: ')
    #    p.drawString(203, 685, f'CNPJ: ')
    #    p.drawString(350, 685, f'Telefone: ')
    #    p.drawRightString(582, 685, f'CEP: ')

    def cliente_pdf(self,alt_ini):
# GERAL CLIENTE        
        p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
        
        p.rect(9, alt_ini-46, 576, 80, stroke=1, fill=1)
        p.setFillColor('black')
        troco = 0
        for i in range(mov_caixa.count()): 
            soma = float(mov_caixa[i].Troco_inicial)
            troco = soma +troco    
        print("teste20")
        soma_tudo = 0 
        p.setFont('Arial',10)
        p.drawString(35, alt_ini+20, f'emitidos: ') 
        p.drawString(12, alt_ini+10, f'A - vista: ')
        p.drawRightString(225, alt_ini+10, f'{formataValor(0)}')
        p.drawString(12, alt_ini, f'B - boleto Bancario:')
        p.drawRightString(225, alt_ini, f'{formataValor(0)}')
        p.drawString(12, alt_ini-10, f'C - Contra Apres: ')
        p.drawRightString(225, alt_ini-10, f'{formataValor(0)}')
        p.drawString(12, alt_ini-20, f'D - cheque pré: ')
        p.drawRightString(225, alt_ini-20, f'{formataValor(0)}')
        p.drawString(12, alt_ini-30, f'E - Carteira: ')
        p.drawRightString(225, alt_ini-30, f'{formataValor(0)}')
        p.drawString(12, alt_ini-40, f'F - duplicada: ')
        p.drawRightString(225, alt_ini-40, f'{formataValor(0)}')
        p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
        p.rect(240, alt_ini+10 , 120, 20, stroke=1, fill=1)
        p.rect(240, alt_ini-17 , 120, 25, stroke=1, fill=1)
        p.rect(240, alt_ini-37 , 120, 25, stroke=1, fill=1)
        p.drawString(412, alt_ini+20, f'emitidos: ') 
        p.drawString(412, alt_ini+10, f'A - vista: ')
        #p.drawRightString(225, alt_ini+10, f'{formataValor(0)}')
        p.setFillColor('black')
        p.drawString(260, alt_ini+17, f'Titulos baixados')
        
        p.drawString(280, alt_ini, f'Saidas')
        p.drawString(280, alt_ini-10, f'{formataValor(0)}')
        p.drawString(280, alt_ini-22,f'Entradas' )
        p.drawString(280, alt_ini-32, f'{formataValor(0)}') 
        p.setFillColor('black') 
        p.drawString(380, alt_ini+20, f'emitidos')
        p.drawString(365, alt_ini+10, f'G - Nota Fiscal:')
        p.drawString(540, alt_ini+10, f'{formataValor(0)}')
        #p.drawRightString(225, alt_ini, f'{formataValor(0)}')
        p.drawString(365, alt_ini, f'H - Nota Promissoria: ')
        p.drawString(540, alt_ini, f'{formataValor(0)}')
        #p.drawRightString(225, alt_ini-10, f'{formataValor(0)}')
        p.drawString(365, alt_ini-10, f'I - Vale:  ')
        p.drawString(540, alt_ini-10, f'{formataValor(0)}')
       # p.drawRightString(225, alt_ini-20, f'{formataValor(0)}')
        p.drawString(365, alt_ini-20, f'j - Cartão ')
        p.drawString(540, alt_ini-20, f'{formataValor(0)}')
        #p.drawRightString(225, alt_ini-30, f'{formataValor(0)}')
    
        p.drawString(365, alt_ini-30, f'k - Convenio ')
        p.drawString(540, alt_ini-30, f'{formataValor(0)}')
        p.drawString(365, alt_ini-40, f'L - Outros (Rp, XX,CX)  ')
       # p.drawRightString(225, alt_ini-40, f'{formataValor(0)}')
        p.drawString(540, alt_ini-40, f'{formataValor(0)}')
        p.setFillColor('black') 
        # sigla 
        #p.drawRightString(155, alt_ini-10, f'G- nota Fiscal: ')
       # p.drawRightString(155, alt_ini-20, f'H-Nota Promissoria: ')
       # p.drawRightString(155, alt_ini-30, f'I - Vale: ')
       # p.drawRightString(155, alt_ini-40, f' j - cartão')
       # p.drawRightString(155, alt_ini-50, f'k - convenio ')
       # p.drawRightString(155, alt_ini-60, f'L=Outros (Rp, XX,CX) ')
        return alt_ini  - 60 
    def produto_cabec_pdf(self):
        p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
        p.rect(9, 700, 100, 15, stroke=1, fill=1) # codigo
        p.rect(52, 700, 100, 15, stroke=1, fill=1) # sigla
        p.rect(112, 700, 140, 15, stroke=1, fill=1) # nome
        p.rect(240, 700, 140, 15, stroke=1, fill=1)
        p.rect(367, 700, 140, 15, stroke=1, fill=1)
        p.rect(434, 700, 100, 15, stroke=1, fill=1)
        p.rect(508, 700, 76, 15, stroke=1, fill=1)
        p.setFillColor('blue')
        p.setFont("ArialBd",11)
        p.drawString(11, 705, "titulos ")
        p.drawString(56, 705, "Setor")
        p.drawString(116, 705, "nome")
        p.drawString(250, 705, "documento")
        p.drawString(380, 705, "esp")
        p.drawString(440, 705, "entradas")
        p.drawString(514, 705, "saidas")
        p.setFont("Arial",11)
        p.setFillColor('black') # voltar cor preta
        return alt_ini - 46
    def caixa_valores_pdf(self,alt_ini):
        p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
        p.rect(9, alt_ini-160, 576, 170, stroke=1, fill=1)
        p.setFillColor('black')
        p.drawString(12, alt_ini, f'Cheque pre datado ') 
        p.drawRightString(225, alt_ini, f'{formataValor(0)}')        
        p.drawString(12, alt_ini-10, f'Convenio ')
        p.drawRightString(225, alt_ini-10, f'{formataValor(0)}')
        p.drawString(12, alt_ini-20, f'Cartão')
        p.drawRightString(225, alt_ini-20, f'{formataValor(0)}')
        p.drawString(12, alt_ini-30, f'Troco inicial')
        p.drawRightString(225, alt_ini-30, f'{formataValor(0)}')
        p.drawString(12, alt_ini-40, f'Vendas a vista ')
        p.drawRightString(225, alt_ini-40, f'{formataValor(0)}')
        p.drawString(12, alt_ini-50, 'DV + TR clientes')
        p.drawRightString(225, alt_ini-50, f'{formataValor(0)}')
        p.drawString(12, alt_ini-60,'NP +CA + CT ')
        p.drawRightString(225, alt_ini-60, f'{formataValor(0)}')
        p.drawString(12, alt_ini-70,'Saidas (-) (-DV + TR)')
        p.drawRightString(225, alt_ini-70, f'{formataValor(0)}')
        p.drawString(12, alt_ini-80,'NP +CA + CT ')
        p.drawRightString(225, alt_ini-80, f'{formataValor(0)}')
        p.drawString(12, alt_ini-90,'Suprimentos - Cheques')
        p.drawRightString(225, alt_ini-90, f'{formataValor(0)}') 
        p.drawString(12, alt_ini-100,'Suprimento Dinheiro')
        p.drawRightString(225, alt_ini-100, f'{formataValor(0)}')
        p.drawString(12, alt_ini-110,' Sabngria/Retirada')
        p.drawRightString(225, alt_ini-110, f'{formataValor(0)}')       
        p.drawString(12, alt_ini-120,'Trans-entradas ')
        p.drawRightString(225, alt_ini-120, f'{formataValor(0)}')       
        p.drawString(12, alt_ini-130,' Trans-saidas')
        p.drawRightString(225, alt_ini-130, f'{formataValor(0)}')
        p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
        p.rect(240, alt_ini-115, 120, 120, stroke=1, fill=1)       
        p.setFillColor('black')
        p.drawString(280, alt_ini-20,'numero ')
        p.drawString(290, alt_ini-40,' de')
        p.drawString(280, alt_ini-60,' Vendas')
        p.drawString(295, alt_ini-80, f'0')
        p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
        p.setFont('Arial',12)
        p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
        p.rect(365, alt_ini-115, 215, 120, stroke=1, fill=1)
        p.rect(365, alt_ini-115, 215, 25, stroke=1, fill=1)
        p.setFillColor('black')
        p.setFont('Arial',10)
        p.drawString(370,alt_ini-20,'Produtos a vista ')
        p.drawString(500,alt_ini-20,f'{formataPorcent(0)}')
        p.drawString(540,alt_ini-20,f'{formataValor(0)}')
        p.drawString(370,alt_ini-30,'Produtos a vista ')
        p.drawString(500,alt_ini-30,f'{formataPorcent(0)}')
        p.drawString(540,alt_ini-30,f'{formataValor(0)}')        
        p.drawString(370,alt_ini-40,'Servicos a vista ')
        p.drawString(500,alt_ini-40,f'{formataPorcent(0)}')
        p.drawString(540,alt_ini-40,f'{formataValor(0)}')
        p.drawString(370,alt_ini-50,'Produtos a praso ') 
        p.drawString(500,alt_ini-50,f'{formataPorcent(0)}')
        p.drawString(540,alt_ini-50,f'{formataValor(0)}')
        p.drawString(370,alt_ini-60,'servicos a praso ') 
        p.drawString(500,alt_ini-60,f'{formataPorcent(0)}')
        p.drawString(540,alt_ini-60,f'{formataValor(0)}')
        p.drawString(370,alt_ini-105,'Total fatur,no dia  ') 
        p.drawString(500,alt_ini-105,f'{formataPorcent(100)}')
        p.drawString(540,alt_ini-105,f'{formataValor(0)}')
        p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
        p.rect(9, alt_ini-160,576,20, stroke=1, fill=1)
        p.setFillColor('black')
        p.setFont('Arial',12)
        p.drawString(9,alt_ini-155,'Caixa Final') 
        p.drawString(225,alt_ini-155,f'{formataValor(0)}')
        p.drawString(370,alt_ini-155,'Diferença de caixa ')
        p.drawString(540,alt_ini-155,f'{formataValor(0)}')
        return alt_ini - 185
    def rodape_pdf(self, alt_ini):
        alt_ini -= 65
        alt_fim = alt_ini-85
        valorTotal = 0
        troco = 0
        p.drawString(12,alt_ini+40,"Totais de Entradas e de Saidas ")
        p.drawString(440,alt_ini+40,f'{formataValor(0)}')
        p.drawString(540,alt_ini+40,f'{formataValor(0)}')
        for i in range(mov_caixa.count()): 
            troco = float(mov_caixa[i].Troco_inicial)
            troco = valorTotal +troco    
        print("teste20")
        soma_tudo = 0
      #  p.drawRightString(582,alt_ini-54,f'{formataValor(valorTotal - venda.desconto_ven)}')
# EXECUTORES
      #  p.setFont("Arial",11)
      #  alt_ini -= 65
      #  alt_fim = alt_ini-85
       # p.rect(9, alt_fim, 576, alt_ini-alt_fim, stroke=1, fill=0)
       # p.drawString(12, alt_ini-15, f'')
       # p.drawString(12, alt_ini-30, f'')
       # p.drawString(12, alt_ini-45, f'')
       # p.drawString(12, alt_ini-60, f'')
       # p.drawString(12, alt_ini-75, f'')
# TOTAL PRODUTO / SERVIÇO # executores
       # p.drawString(12, alt_ini-13 "SEM OBSERVAÇÔES ")# f'{mov_caixa. if venda.obs_ven != None else ""}') 
        p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
        p.rect(12, alt_ini-60, 174, 60, stroke=1, fill=1)
        p.setFillColor('black')
        p.setFont("Arial",11)
        p.drawString(12,alt_ini-15,"Observações/caixa")
        p.setFillColorRGB(0.90625, 0.9375, 0.9453125)
        p.rect(190, alt_ini-60, 194, 60, stroke=1, fill=1)
        p.setFillColor('black')
        p.drawString(210, alt_ini-15, f'Observações/visto :')
        p.setFillColorRGB(0.90625, 0.9375, 0.9453125)
        p.rect(390, alt_ini-60, 174, 60, stroke=1, fill=1)
        p.setFillColor('black')
        p.drawString(395, alt_ini-25, f'Total Geral:')
        p.drawRightString(561,alt_ini-25,f'{formataValor(0)}')
        p.drawString(395, alt_ini-40, f'Saldo Anterior')
        p.drawRightString(561,alt_ini-40,f'{formataValor(0)}')
        p.drawString(395, alt_ini-55, f'Saldo Atual')
        p.drawRightString(561,alt_ini-55,f'{formataValor(0)}')
# CONDIÇÃO
        p.setFillColorRGB(0.90625, 0.9375, 0.9453125)
        p.rect(390, alt_ini-85, 174, 20, stroke=1, fill=1)
        p.setFillColor('black')
    #

      #  p.drawString(395, alt_ini-68, f'Cond. {venda.condicao_ven if venda.condicao_ven != None else ""}')
# RODAPÉ
        alt_ini = alt_ini - 190
        p.drawImage('./vendas/core/static/img/Rodape QuickReport.bmp', 0, alt_ini, width=None,height=None,mask=None)
        p.drawImage('./vendas/core/static/img/Rodapé Relatorios Cecotein novo.bmp', 9, alt_ini+20, width=None,height=None,mask=None)
        p.setFillColorRGB(0.90625, 0.9375, 0.9453125)
        #p.rect(180, alt_ini+40, 280, 40, stroke=1, fill=1)
        #p.setFillColorRGB(30,144,255)
        #p.rect(185, alt_ini+60, 90, 15, stroke=1, fill=1)
       # p.rect(280, alt_ini+60, 175, 15, stroke=1, fill=1)
        #p.rect(280, alt_ini+43, 175, 15, stroke=1, fill=1)
        p.setFillColor('black')
        #p.drawString(190 , alt_ini +65, "Processador por ")
        #p.drawCentredString(370,alt_ini+65,"Nome emp (00)0000-0000")
        #p.drawString(285,alt_ini+47,"CECOTEIN- shopping informatica")
        p.drawString(510, alt_ini+80, f'Sistema ')
        p.drawRightString(584, alt_ini+80, f'0180')
        p.drawString(510,alt_ini+60,f'Tela ')
        p.drawRightString(584,alt_ini+60,f'000-1')
        p.drawString(510,alt_ini+40,'Versão ')
        p.drawRightString(584,alt_ini+40,'1.0')

    def gera_produtos_pdf(self,alt_ini):
        alt_fim = alt_ini - 20
        titulos = Titulos.objects.all().order_by('pk')
        for i in range(titulos.count()):
            p.rect(9, alt_fim, 43, alt_ini-alt_fim, stroke=1, fill=0) # código
            p.rect(52, alt_fim, 60, alt_ini-alt_fim, stroke=1, fill=0) # sigla
            p.rect(112, alt_fim, 128, alt_ini-alt_fim, stroke=1, fill=0) # nome
            p.rect(240, alt_fim, 127, alt_ini-alt_fim, stroke=1, fill=0) # un
            #p.rect(392, alt_fim, 82, alt_ini-alt_fim, stroke=1, fill=0) # quant
            p.rect(367, alt_fim, 68, alt_ini-alt_fim, stroke=1, fill=0)
            p.rect(434, alt_fim, 74, alt_ini-alt_fim, stroke=1, fill=0) # valor unit
            p.rect(508, alt_fim, 77, alt_ini-alt_fim, stroke=1, fill=0) # valor total
            
            # Responsável pelo desenho das informações dos produtos
           # produto = Produto.objects.get(produto_pro=itens[i].produto_ite_id)
            if titulos[i].tipo_tit == "E"  or titulos[i].tipo_tit == 'e':
                setor = Setor.objects.get(pk=titulos[i].setor_baixa_tit.key_setor)
                p.drawString(12, alt_ini-13, f'{titulos[i].numero_tit}')
                p.drawString(56,alt_ini-13, f'{setor.key_setor}')
                p.drawString(116, (alt_ini-13), f'nome')
                p.drawString(250, (alt_ini-13), f'Docum')
                
                p.drawString(380,(alt_ini -13), f'{titulos[i].tipo_mov_tit}')
                if titulos[i].tipo_baixa_tit != None:  
                    p.drawRightString(505, alt_ini-13, f'{formataValor(titulos[i].tipo_baixa_tit)}')
                    p.drawRightString(582, alt_ini-13, f'{formataValor(0)}')
                else :
                    p.drawRightString(505, alt_ini-13, f'{formataValor(0)}')
                    p.drawRightString(582, alt_ini-13, f'{formataValor(0)}')
                alt_ini -= 20
            else :
                if titulos[i].tipo_tit == 'S' or titulos[i].tipo_tit == 's' :
                    setor = Setor.objects.get(pk=titulos[i].setor_baixa_tit.key_setor)
                    p.drawString(12, alt_ini-13, f'{titulos[i].numero_tit}')
                    p.drawString(56,alt_ini-13, f'{setor.key_setor}')
                    p.drawString(116, (alt_ini-13), f'nome')
                    p.drawString(250, (alt_ini-13), f'Docum')
                    p.drawString(380,(alt_ini -13), f'{titulos[i].tipo_mov_tit}')
                if titulos[i].tipo_baixa_tit != None:  
                    p.drawRightString(505, alt_ini-13, f'{formataValor(0)}')
                    p.drawRightString(582, alt_ini-13, f'{formataValor(titulos[i].tipo_baixa_tit)}')
                else :
                    p.drawRightString(505, alt_ini-13, f'{formataValor(0)}')
                    p.drawRightString(582, alt_ini-13, f'{formataValor(0)}')
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
        p.rect(240, alt_fim, 195, alt_ini-alt_fim, stroke=1, fill=0)
        #p.rect(367, alt_fim, 42, alt_ini-alt_fim, stroke=1, fill=0)
        #p.rect(392, alt_fim, 82, alt_ini-alt_fim, stroke=1, fill=0)
        p.rect(434, alt_fim, 74, alt_ini-alt_fim, stroke=1, fill=0)
        p.rect(508, alt_fim, 77, alt_ini-alt_fim, stroke=1, fill=0)
        return alt_ini - 40
        rodape_pdf(self, alt_ini)        

    cabecalho_pdf(p)
    #cliente_pdf(p)
    produto_cabec_pdf(p)
    alt_ini = gera_produtos_pdf(p,alt_ini)
    alt_ini = cliente_pdf(p,alt_ini)
    alt_ini = caixa_valores_pdf(p,alt_ini)
    rodape_pdf(p,alt_ini)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename=f'movimento_de_caixa{data}.pdf')
#/-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
#/-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
#/-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
def mov_caixaM_filtro(request,pk):
    alt_ini = 700
    mov_caixa = get_object_or_404(Mov_caixa,pk=pk)
    total_ent = 0
    total_sai = 0
    troco = float(0.00)
    user = get_object_or_404(User,pk=mov_caixa.usu_alt.id)
    print(mov_caixa.data_mov)
    #setor= mov_caixa.objects.filter(pk= object_list.cod_seto_mov_c).order_by(pk)
    buffer = io.BytesIO()
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer,pagesize=A4,bottomup=1,pageCompression=0,verbosity=0,)
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    pdfmetrics.registerFont(TTFont('ArialBd', 'ArialBd.ttf'))
    p.setFont("Arial", 11)    
    p.setTitle(f'Movimento de caixa ')

    def cabecalho_pdf(self): # altura 800 até 740
        string = user.foto_emp.url
        p.drawImage('./vendas/core/static/img/mov_caixa.png', -70, 720,width=700,height=None,mask=None)
     #  p.drawImage(string, -10, 716, width=100,height=100,mask=None)
        p.drawImage(f'./{request.user.foto_emp.url}', 10, 766, 70,70,mask=None)
        p.drawString(510,800,'Folha ')
        p.drawRightString(584, 800, f'{str(p.getPageNumber())}')
        p.drawString(510,785,'Data ')
        p.drawRightString(584, 785, f'{datetime.today().strftime("%d/%m/%y")}')
        p.drawString(510,770,'Hora ')
        p.drawRightString(584, 770, f'{datetime.today().strftime("%H:%M")}')
# GERAL VENDA
     #   p.rect(9, 675, 190, 65, stroke=1, fill=0)
     #   p.drawString(12, 725, f'')
     #   p.drawString(12, 710, f'') 
     #   p.drawString(147, 710, f'')         
      #  p.drawString(12, 695, f'')
     #   p.drawString(12, 680, f'')
# GERAL EMPRESA
    #    p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
    #    p.rect(190, 675, 395, 65, stroke=1, fill=1)
    #    p.setFillColor('black')
    #    p.setFont("ArialBd",24)
    #    p.drawCentredString(388/2+200, 718, f'')
    #    p.setFont("Arial",11)
    #    p.drawString(203, 700, f': ')
    #    p.drawRightString(582, 700, f'Bairro: ')
    #    p.drawString(203, 685, f'CNPJ: ')
    #    p.drawString(350, 685, f'Telefone: ')
    #    p.drawRightString(582, 685, f'CEP: ')

    def cliente_pdf(self,alt_ini,total_ent,total_sai):
# GERAL CLIENTE        
        print(total_ent)
        print(total_sai)  
        p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
        
        p.rect(9, alt_ini-46, 576, 80, stroke=1, fill=1)
        p.setFillColor('black')
        troco = 0
       # for i in range(mov_caixa.count()): 
       #     soma = float(mov_caixa[i].Troco_inicial)
       #     troco = soma +troco    
       # print("teste20")
      #  soma_tudo = 0 
        p.setFont('Arial',10)
         p.drawString(120, alt_ini+20, f'EMITIDOS: ') 
        p.drawString(12, alt_ini+10, f'A - vista: ')
        p.drawRightString(225, alt_ini+10, f'{formataValor(0)}')
        p.drawString(12, alt_ini, f'B - boleto Bancario:')
        p.drawRightString(225, alt_ini, f'{formataValor(0)}')
        p.drawString(12, alt_ini-10, f'C - Contra Apres: ')
        p.drawRightString(225, alt_ini-10, f'{formataValor(0)}')
        p.drawString(12, alt_ini-20, f'D - cheque pré: ')
        p.drawRightString(225, alt_ini-20, f'{formataValor(0)}')
        p.drawString(12, alt_ini-30, f'E - Carteira: ')
        p.drawRightString(225, alt_ini-30, f'{formataValor(0)}')
        p.drawString(12, alt_ini-40, f'F - duplicada: ')
        p.drawRightString(225, alt_ini-40, f'{formataValor(0)}')
        p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
        p.rect(240, alt_ini+10 , 120, 20, stroke=1, fill=1)
        p.rect(240, alt_ini-17 , 120, 25, stroke=1, fill=1)
        p.rect(240, alt_ini-37 , 120, 25, stroke=1, fill=1)
 
        p.drawString(412, alt_ini+10, f'A - vista: ')
        #p.drawRightString(225, alt_ini+10, f'{formataValor(0)}')
        p.setFillColor('black')
        p.drawString(260, alt_ini+17, f'Titulos baixados')
        
        p.drawString(280, alt_ini, f'Saidas')
        p.drawString(280, alt_ini-10, f'{formataValor(total_sai)}')
        p.drawString(280, alt_ini-22,f'Entradas' )
        p.drawString(280, alt_ini-32, f'{formataValor(total_ent)}') 
        p.setFillColor('black') 
        p.drawString(380, alt_ini+20, f'emitidos')
        p.drawString(365, alt_ini+10, f'G - Nota Fiscal:')
        p.drawString(540, alt_ini+10, f'{formataValor(0)}')
        #p.drawRightString(225, alt_ini, f'{formataValor(0)}')
        p.drawString(365, alt_ini, f'H - Nota Promissoria: ')
        p.drawString(540, alt_ini, f'{formataValor(0)}')
        #p.drawRightString(225, alt_ini-10, f'{formataValor(0)}')
        p.drawString(365, alt_ini-10, f'I - Vale:  ')
        p.drawString(540, alt_ini-10, f'{formataValor(0)}')
       # p.drawRightString(225, alt_ini-20, f'{formataValor(0)}')
        p.drawString(365, alt_ini-20, f'j - Cartão ')
        p.drawString(540, alt_ini-20, f'{formataValor(0)}')
        #p.drawRightString(225, alt_ini-30, f'{formataValor(0)}')
    
        p.drawString(365, alt_ini-30, f'k - Convenio ')
        p.drawString(540, alt_ini-30, f'{formataValor(0)}')
        p.drawString(365, alt_ini-40, f'L - Outros (Rp, XX,CX)  ')
       # p.drawRightString(225, alt_ini-40, f'{formataValor(0)}')
        p.drawString(540, alt_ini-40, f'{formataValor(0)}')
        p.setFillColor('black') 
        # sigla 
        #p.drawRightString(155, alt_ini-10, f'G- nota Fiscal: ')
       # p.drawRightString(155, alt_ini-20, f'H-Nota Promissoria: ')
       # p.drawRightString(155, alt_ini-30, f'I - Vale: ')
       # p.drawRightString(155, alt_ini-40, f' j - cartão')
       # p.drawRightString(155, alt_ini-50, f'k - convenio ')
       # p.drawRightString(155, alt_ini-60, f'L=Outros (Rp, XX,CX) ')
        alt_ini = alt_ini -60
        alt_ini = caixa_valores_pdf(p,alt_ini,total_ent,total_sai)
        rodape_pdf(p,alt_ini,total_ent,total_sai)
        return alt_ini
    def produto_cabec_pdf(self):
        p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
        p.rect(9, 700, 100, 15, stroke=1, fill=1) # codigo
        p.rect(52, 700, 100, 15, stroke=1, fill=1) # sigla
        p.rect(112, 700, 140, 15, stroke=1, fill=1) # nome
        p.rect(240, 700, 140, 15, stroke=1, fill=1)
        p.rect(367, 700, 140, 15, stroke=1, fill=1)
        p.rect(434, 700, 100, 15, stroke=1, fill=1)
        p.rect(508, 700, 76, 15, stroke=1, fill=1)
        p.setFillColor('blue')
        p.setFont("ArialBd",11)
        p.drawString(11, 705, "titulos ")
        p.drawString(56, 705, "Setor")
        p.drawString(116, 705, "nome")
        p.drawString(250, 705, "documento")
        p.drawString(380, 705, "esp")
        p.drawString(440, 705, "entradas")
        p.drawString(514, 705, "saidas")
        p.setFont("Arial",11)
        p.setFillColor('black') # voltar cor preta
        return alt_ini - 46
    def caixa_valores_pdf(self,alt_ini,total_ent,total_sai):
        p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
        p.rect(9, alt_ini-160, 576, 170, stroke=1, fill=1)
        p.setFillColor('black')
        p.drawString(12, alt_ini, f'Cheque pre datado ') 
        p.drawRightString(225, alt_ini, f'{formataValor(0)}')        
        p.drawString(12, alt_ini-10, f'Convenio ')
        p.drawRightString(225, alt_ini-10, f'{formataValor(0)}')
        p.drawString(12, alt_ini-20, f'Cartão')
        p.drawRightString(225, alt_ini-20, f'{formataValor(0)}')
        p.drawString(12, alt_ini-30, f'Troco inicial')
        p.drawRightString(225, alt_ini-30, f'{formataValor(mov_caixa.Troco_inicial)}')
        p.drawString(12, alt_ini-40, f'Vendas a vista ')
        p.drawRightString(225, alt_ini-40, f'{formataValor(0)}')
        p.drawString(12, alt_ini-50, 'DV + TR clientes')
        p.drawRightString(225, alt_ini-50, f'{formataValor(0)}')
        p.drawString(12, alt_ini-60,'NP +CA + CT ')
        p.drawRightString(225, alt_ini-60, f'{formataValor(0)}')
        p.drawString(12, alt_ini-70,'Saidas (-) (-DV + TR)')
        p.drawRightString(225, alt_ini-70, f'{formataValor(total_sai)}')
        p.drawString(12, alt_ini-80,'NP +CA + CT ')
        p.drawRightString(225, alt_ini-80, f'{formataValor(total_ent)}')
        p.drawString(12, alt_ini-90,'Suprimentos - Cheques')
        p.drawRightString(225, alt_ini-90, f'{formataValor(0)}') 
        p.drawString(12, alt_ini-100,'Suprimento Dinheiro')
        p.drawRightString(225, alt_ini-100, f'{formataValor(0)}')
        p.drawString(12, alt_ini-110,' Sabngria/Retirada')
        p.drawRightString(225, alt_ini-110, f'{formataValor(0)}')       
        p.drawString(12, alt_ini-120,'Trans-entradas ')
        p.drawRightString(225, alt_ini-120, f'{formataValor(0)}')       
        p.drawString(12, alt_ini-130,' Trans-saidas')
        p.drawRightString(225, alt_ini-130, f'{formataValor(0)}')
        p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
        p.rect(240, alt_ini-115, 120, 120, stroke=1, fill=1)       
        p.setFillColor('black')
        p.drawString(280, alt_ini-20,'numero ')
        p.drawString(290, alt_ini-40,' de')
        p.drawString(280, alt_ini-60,' Vendas')
        p.drawString(295, alt_ini-80, f'0')
        p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
        p.setFont('Arial',12)
        p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
        p.rect(365, alt_ini-115, 215, 120, stroke=1, fill=1)
        p.rect(365, alt_ini-115, 215, 25, stroke=1, fill=1)
        p.setFillColor('black')
        p.setFont('Arial',10)
        p.drawString(370,alt_ini-20,'Produtos a vista ')
        p.drawString(500,alt_ini-20,f'{formataPorcent(0)}')
        p.drawString(540,alt_ini-20,f'{formataValor(0)}')
        p.drawString(370,alt_ini-30,'Produtos a vista ')
        p.drawString(500,alt_ini-30,f'{formataPorcent(0)}')
        p.drawString(540,alt_ini-30,f'{formataValor(0)}')        
        p.drawString(370,alt_ini-40,'Servicos a vista ')
        p.drawString(500,alt_ini-40,f'{formataPorcent(0)}')
        p.drawString(540,alt_ini-40,f'{formataValor(0)}')
        p.drawString(370,alt_ini-50,'Produtos a praso ') 
        p.drawString(500,alt_ini-50,f'{formataPorcent(0)}')
        p.drawString(540,alt_ini-50,f'{formataValor(0)}')
        p.drawString(370,alt_ini-60,'servicos a praso ') 
        p.drawString(500,alt_ini-60,f'{formataPorcent(0)}')
        p.drawString(540,alt_ini-60,f'{formataValor(0)}')
        p.drawString(370,alt_ini-105,'Total fatur,no dia  ') 
        p.drawString(500,alt_ini-105,f'{formataPorcent(100)}')
        p.drawString(540,alt_ini-105,f'{formataValor(0)}')
        p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
        p.rect(9, alt_ini-160,576,20, stroke=1, fill=1)
        p.setFillColor('black')
        p.setFont('Arial',12)
        p.drawString(9,alt_ini-155,'Caixa Final') 
        p.drawString(225,alt_ini-155,f'{formataValor(0)}')
        p.drawString(370,alt_ini-155,'Diferença de caixa ')
        p.drawString(540,alt_ini-155,f'{formataValor(0)}')
        return alt_ini - 185
    def rodape_pdf(self, alt_ini,total_ent,total_sai):
        alt_ini -= 65
        alt_fim = alt_ini-85
        valorTotal = 0
        troco = 0
        p.drawString(12,alt_ini+40,"Totais de Entradas e de Saidas ")
        p.drawString(440,alt_ini+40,f'{formataValor(total_ent)}')
        p.drawString(530,alt_ini+40,f'{formataValor(total_sai)}') 
        troco = float(mov_caixa.Troco_inicial)
        troco = valorTotal +troco    
        print("teste20")
        soma_tudo = 0
      #  p.drawRightString(582,alt_ini-54,f'{formataValor(valorTotal - venda.desconto_ven)}')
# EXECUTORES
      #  p.setFont("Arial",11)
      #  alt_ini -= 65
      #  alt_fim = alt_ini-85
       # p.rect(9, alt_fim, 576, alt_ini-alt_fim, stroke=1, fill=0)
       # p.drawString(12, alt_ini-15, f'')
       # p.drawString(12, alt_ini-30, f'')
       # p.drawString(12, alt_ini-45, f'')
       # p.drawString(12, alt_ini-60, f'')
       # p.drawString(12, alt_ini-75, f'')
# TOTAL PRODUTO / SERVIÇO # executores
       # p.drawString(12, alt_ini-13 "SEM OBSERVAÇÔES ")# f'{mov_caixa. if venda.obs_ven != None else ""}') 
        total = total_ent - total_sai 
        p.setFillColorRGB(0.7421875, 0.85546875, 0.99609375)
        p.rect(12, alt_ini-60, 174, 60, stroke=1, fill=1)
        p.setFillColor('black')
        p.setFont("Arial",11)
        p.drawString(12,alt_ini-15,"Observações/caixa")
        p.setFillColorRGB(0.90625, 0.9375, 0.9453125)
        p.rect(190, alt_ini-60, 194, 60, stroke=1, fill=1)
        p.setFillColor('black')
        p.drawString(210, alt_ini-15, f'Observações/visto :')
        p.setFillColorRGB(0.90625, 0.9375, 0.9453125)
        p.rect(390, alt_ini-60, 174, 60, stroke=1, fill=1)
        p.setFillColor('black')
        p.drawString(395, alt_ini-25, f'Total Geral:')
        p.drawRightString(561,alt_ini-25,f'{formataValor(total)}')
        p.drawString(395, alt_ini-40, f'Saldo Anterior')
        p.drawRightString(561,alt_ini-40,f'{formataValor(mov_caixa.saldo_ant)}')
        p.drawString(395, alt_ini-55, f'Saldo Atual')
        p.drawRightString(561,alt_ini-55,f'{formataValor(0)}')
# CONDIÇÃO
        p.setFillColorRGB(0.90625, 0.9375, 0.9453125)
        p.rect(390, alt_ini-85, 174, 20, stroke=1, fill=1)
        p.setFillColor('black')
    #

      #  p.drawString(395, alt_ini-68, f'Cond. {venda.condicao_ven if venda.condicao_ven != None else ""}')
# RODAPÉ
        alt_ini = alt_ini - 190
        p.drawImage('./vendas/core/static/img/Rodape QuickReport.bmp', 0, alt_ini, width=None,height=None,mask=None)
        p.drawImage('./vendas/core/static/img/Rodapé Relatorios Cecotein novo.bmp', 9, alt_ini+20, width=None,height=None,mask=None)
        p.setFillColorRGB(0.90625, 0.9375, 0.9453125)
        #p.rect(180, alt_ini+40, 280, 40, stroke=1, fill=1)
        #p.setFillColorRGB(30,144,255)
        #p.rect(185, alt_ini+60, 90, 15, stroke=1, fill=1)
       # p.rect(280, alt_ini+60, 175, 15, stroke=1, fill=1)
        #p.rect(280, alt_ini+43, 175, 15, stroke=1, fill=1)
        p.setFillColor('black')
        #p.drawString(190 , alt_ini +65, "Processador por ")
        #p.drawCentredString(370,alt_ini+65,"Nome emp (00)0000-0000")
        #p.drawString(285,alt_ini+47,"CECOTEIN- shopping informatica")
        p.drawString(510, alt_ini+80, f'Sistema ')
        p.drawRightString(584, alt_ini+80, f'0180')
        p.drawString(510,alt_ini+60,f'Tela ')
        p.drawRightString(584,alt_ini+60,f'000-1')
        p.drawString(510,alt_ini+40,'Versão ')
        p.drawRightString(584,alt_ini+40,'1.0')

    def gera_produtos_pdf(self,alt_ini,total_ent,total_sai):
        alt_fim = alt_ini - 20
        data1 =  mov_caixa.data_mov
        date = mov_caixa.data_emiss - timedelta(1)
        print(date)
        titulos = Titulos.objects.filter(data_emissao_tit__range=[data1,date])
        print(titulos)
        for i in range(titulos.count()):
            p.rect(9, alt_fim, 43, alt_ini-alt_fim, stroke=1, fill=0) # código
            p.rect(52, alt_fim, 60, alt_ini-alt_fim, stroke=1, fill=0) # sigla
            p.rect(112, alt_fim, 128, alt_ini-alt_fim, stroke=1, fill=0) # nome
            p.rect(240, alt_fim, 127, alt_ini-alt_fim, stroke=1, fill=0) # un
            #p.rect(392, alt_fim, 82, alt_ini-alt_fim, stroke=1, fill=0) # quant
            p.rect(367, alt_fim, 68, alt_ini-alt_fim, stroke=1, fill=0)
            p.rect(434, alt_fim, 74, alt_ini-alt_fim, stroke=1, fill=0) # valor unit
            p.rect(508, alt_fim, 77, alt_ini-alt_fim, stroke=1, fill=0) # valor total
            
            # Responsável pelo desenho das informações dos produtos
           # produto = Produto.objects.get(produto_pro=itens[i].produto_ite_id)
            if titulos[i].tipo_tit == "E"  or titulos[i].tipo_tit == 'e':
                setor = Setor.objects.get(pk=titulos[i].setor_baixa_tit.key_setor)
                p.drawString(12, alt_ini-13, f'{titulos[i].numero_tit}')
                p.drawString(56,alt_ini-13, f'{setor.key_setor}')
                p.drawString(116, (alt_ini-13), f'nome')
                p.drawString(250, (alt_ini-13), f'Docum')
                
                p.drawString(380,(alt_ini -13), f'{titulos[i].tipo_mov_tit}')
                if titulos[i].tipo_baixa_tit != None:  
                    p.drawRightString(505, alt_ini-13, f'{formataValor(titulos[i].tipo_baixa_tit)}')
                    p.drawRightString(582, alt_ini-13, f'{formataValor(0)}')
                    total_ent = total_ent + titulos[i].tipo_baixa_tit
                else :
                    p.drawRightString(505, alt_ini-13, f'{formataValor(0)}')
                    p.drawRightString(582, alt_ini-13, f'{formataValor(0)}')
                alt_ini -= 20
            else :
                if titulos[i].tipo_tit == 'S' or titulos[i].tipo_tit == 's' :
                    setor = Setor.objects.get(pk=titulos[i].setor_baixa_tit.key_setor)
                    p.drawString(12, alt_ini-13, f'{titulos[i].numero_tit}')
                    p.drawString(56,alt_ini-13, f'{setor.key_setor}')
                    p.drawString(116, (alt_ini-13), f'nome')
                    p.drawString(250, (alt_ini-13), f'Docum')
                    p.drawString(380,(alt_ini -13), f'{titulos[i].tipo_mov_tit}')
                if titulos[i].tipo_baixa_tit != None:  
                    p.drawRightString(505, alt_ini-13, f'{formataValor(0)}')
                    p.drawRightString(582, alt_ini-13, f'{formataValor(titulos[i].tipo_baixa_tit)}')
                    total_sai = total_sai + titulos[i].tipo_baixa_tit
                else :
                    p.drawRightString(505, alt_ini-13, f'{formataValor(0)}')
                    p.drawRightString(582, alt_ini-13, f'{formataValor(0)}')
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
        p.rect(240, alt_fim, 195, alt_ini-alt_fim, stroke=1, fill=0)
        #p.rect(367, alt_fim, 42, alt_ini-alt_fim, stroke=1, fill=0)
        #p.rect(392, alt_fim, 82, alt_ini-alt_fim, stroke=1, fill=0)
        p.rect(434, alt_fim, 74, alt_ini-alt_fim, stroke=1, fill=0)
        p.rect(508, alt_fim, 77, alt_ini-alt_fim, stroke=1, fill=0)
        alt_ini = alt_ini - 40
        alt_ini = cliente_pdf(p,alt_ini,total_ent,total_sai)
        return alt_ini
       
        rodape_pdf(self, alt_ini)        

    cabecalho_pdf(p)
    #cliente_pdf(p)
    produto_cabec_pdf(p)
    alt_ini = gera_produtos_pdf(p,alt_ini,total_ent,total_sai)
    #alt_ini = cliente_pdf(p,alt_ini,total_ent,total_sai)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename=f'movimento_de_caixa{mov_caixa.pk}.pdf')


