from kivy.app import App
from kivy.lang import Builder
from telas import *
from botoes import *
from datetime import date
from banner_vendas import BannerVendas
from banner_vendedor import BannerVendedor
from functools import partial
from myfirebase import Myfarebase
import requests
import os


GUI = Builder.load_file("main.kv")
class MainApp(App):

    cliente = None
    produto = None
    unidade = None

    def build(self):
        self.firebase = Myfarebase()
        return GUI

    def on_start(self):
        # lista de arquivos de fotos do usuario
        arquivo = os.listdir("icones/fotos_perfil")
        pagina_fotoperfil = self.root.ids["fotoperfilpage"]
        lista_fotos = pagina_fotoperfil.ids["lista_fotos_perfil"]

        # atualizacao de foto perfil
        for foto in arquivo:
            imagem = ImageButton(source=f"icones/fotos_perfil/{foto}", on_release=partial(self.mudar_foto, foto))
            lista_fotos.add_widget(imagem)

        # carregar foto dos clientes
        arquivos = os.listdir("icones/fotos_clientes")
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"]
        lista_clientes = pagina_adicionarvendas.ids["lista_clientes"]

        for foto_cliente in arquivos:
            imagem = ImageButton(source=f"icones/fotos_clientes/{foto_cliente}", on_release=partial(self.selecinar_cliente, foto_cliente))
            label = LabelButton(text=foto_cliente.replace(".png", "").capitalize(), on_release=partial(self.selecinar_cliente, foto_cliente))

            lista_clientes.add_widget(imagem)
            lista_clientes.add_widget(label)

        # carregar fotos dos produtos
        arquivos = os.listdir("icones/fotos_produtos")
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"]
        lista_produtos = pagina_adicionarvendas.ids["lista_produtos"]

        for foto_produto in arquivos:
            imagem = ImageButton(source=f"icones/fotos_produtos/{foto_produto}", on_release=partial(self.selecinar_produto, foto_produto))
            label = LabelButton(text=foto_produto.replace(".png", "").capitalize(), on_release=partial(self.selecinar_produto, foto_produto))

            lista_produtos.add_widget(imagem)
            lista_produtos.add_widget(label)

        #carregar a data atual para a pagina
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"]
        label_data = pagina_adicionarvendas.ids["label_data"]
        label_data.text = f"Data: {date.today().strftime('%d/%m/%Y')}"


        # carregar usuarios
        self.carregar_informacaoes_usuario()

    def mudar_foto(self, foto, *args):
        foto_perfil = self.root.ids['foto_perfil']
        foto_perfil.source = f"icones/fotos_perfil/{foto}"

        # atualizar banco de dado
        info = f'{{"avatar": "{foto}"}}'

        requisicao = requests.patch(f"https://aplicativo-e340d-default-rtdb.firebaseio.com/{self.local_id}.json",
                                   data=info)

        self.mudar_tela("ajustespage")

    def adicionar_vendedor(self, id_vendedor_adicionado):
        link = f'https://aplicativo-e340d-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_vendedor_adicionado}"'
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()

        pagina_adicionarvendedor = self.root.ids["adicionarvendedorpage"]
        mensagem_texto = pagina_adicionarvendedor.ids["mensagem_outrovendedor"]

        if requisicao_dic == {}:
            mensagem_texto.text = "usuário não existe"
        else:
            equipe = self.equipe.split(",")
            if id_vendedor_adicionado in equipe:
                mensagem_texto.text = ("Vendedor ja faz parte da equipe")
            else:
                self.equipe = self.equipe + f",{id_vendedor_adicionado}"
                info = f'{{"equipe": "{self.equipe}"}}'
                requests.patch(f"https://aplicativo-e340d-default-rtdb.firebaseio.com/{self.local_id}.json",
                                data=info)
                mensagem_texto.text = "Vendedor adicionado com sucesso"
                self.mudar_tela('listarvendedorespage')
                # adicionar outro banner a lista vendedores
                pagina_listavendedores = self.root.ids["listarvendedorespage"]
                lista_vendedores = pagina_listavendedores.ids["lista_vendedores"]
                banner_vendedor = BannerVendedor(id_vendedor=id_vendedor_adicionado)
                lista_vendedores.add_widget(banner_vendedor)




    def carregar_informacaoes_usuario(self):
        try:
            # pegar informações do usuarios
            requisicao = requests.get(f"https://aplicativo-e340d-default-rtdb.firebaseio.com/{self.local_id}.json")
            requisicao_dic = requisicao.json()

            # preencher a foto de perfil
            avatar = requisicao_dic["avatar"]
            self.avatar = avatar
            foto_perfil = self.root.ids['foto_perfil']
            foto_perfil.source = f"icones/fotos_perfil/{avatar}"

            # preencher o total de vendas

            total_vendas = requisicao_dic["total_vendas"]
            self.total_vendas = total_vendas
            homepage = self.root.ids["homepage"]
            homepage.ids["label_total_vendas"].text = f"[color=#000000]Total de Vendas: [/color] [b]R${total_vendas}[/b]"

            # preencher o ID unico

            id_vendedor = requisicao_dic['id_vendedor']
            self.id_vendedor =id_vendedor
            pagina_ajustes = self.root.ids["ajustespage"]
            pagina_ajustes.ids["id_vendedor"].text = f"Seu ID Único: {id_vendedor}"
            # preencher equipe
            self.equipe = requisicao_dic["equipe"]

            # preencher lista de vendas


            # preencher lista de vendas
            try:
                vendas = requisicao_dic['vendas']
                self.vendas = vendas
                pagina_homepage = self.root.ids["homepage"]
                lista_vendas = pagina_homepage.ids["lista_vendas"]
                for id_venda in vendas:
                    venda = vendas[id_venda]
                    banner = BannerVendas(cliente=venda["cliente"], foto_cliente=venda["foto_cliente"],
                                          produto=venda["produto"], foto_produto=venda["foto_produto"],
                                          data=venda["data"], preco=venda["preco"],
                                          unidade=venda["unidade"], quantidade=venda["quantidade"])

                    lista_vendas.add_widget(banner)
            except:
                pass

            # preencher equipe
            equipe = requisicao_dic["equipe"]
            lista_equipe = equipe.split(",")
            pagina_listavendedores = self.root.ids["listarvendedorespage"]
            lista_vendedores = pagina_listavendedores.ids["lista_vendedores"]

            # criando a lista na página Listarvendedor
            for id_vendedor_equipe in lista_equipe:
                if id_vendedor_equipe != "":
                    banner_vendedor = BannerVendedor(id_vendedor=id_vendedor_equipe)
                    lista_vendedores.add_widget(banner_vendedor)



            self.mudar_tela('homepage')

        except:
            pass

    def mudar_tela(self, id_tela):
        gerenciador_telas = self.root.ids["screen_manager"]
        gerenciador_telas.current = id_tela

    def selecinar_cliente(self, foto, *args):
        self.cliente = foto.replace(".png", "")
        # pintar de branco todas a outras letras
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"]
        lista_clientes = pagina_adicionarvendas.ids["lista_clientes"]

        for item in list(lista_clientes.children):
            item.color = (1, 1, 1, 1)

        #pintar de azul a letra do item selecionado
            try:
                texto = item.text
                texto = texto.lower() + ".png"
                if foto == texto:
                    item.color = (0, 207/255, 219/255, 1)

            except:
                pass

    def selecinar_produto(self, foto, *args):
        # pintar de branco todas a outras letras
        self.produto = foto.replace(".png", "")
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"]
        lista_produtos = pagina_adicionarvendas.ids["lista_produtos"]

        for item in list(lista_produtos.children):
            item.color = (1, 1, 1, 1)

        #pintar de azul a letra do item selecionado
            try:
                texto = item.text
                texto = texto.lower() + ".png"
                if foto == texto:
                    item.color = (0, 207/255, 219/255, 1)

            except:
                pass

    def selecionar_unidade(self, id_label, *args):
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"]
        self.unidade = id_label.replace("unidades_", "")
        # pintar de branco todas a outras letras
        pagina_adicionarvendas.ids["unidades_litros"].color = (1, 1, 1, 1)
        pagina_adicionarvendas.ids["unidades_kg"].color = (1, 1, 1, 1)
        pagina_adicionarvendas.ids["unidades_unidades"].color = (1, 1, 1, 1)
        # pintar de azul a letra do item selecionado
        pagina_adicionarvendas.ids[id_label].color = (0, 207/255, 219/255, 1)

    def adicionar_venda(self):
        cliente = self.cliente
        produto = self.produto
        unidade = self.unidade
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"]
        data = pagina_adicionarvendas.ids["label_data"].text.replace("Data: ", "")
        preco = pagina_adicionarvendas.ids["preco_total"].text
        quantidade = pagina_adicionarvendas.ids["quantidade"].text

        if not cliente:
            pagina_adicionarvendas.ids["label_selecione_cliente"].color = (1, 0, 0, 1)

        if not produto:
            pagina_adicionarvendas.ids["label_selecione_cliente"].color = (1, 0, 0, 1)

        if not unidade:
            pagina_adicionarvendas.ids["unidades_litros"].color = (1, 0, 0, 1)
            pagina_adicionarvendas.ids["unidades_unidades"].color = (1, 0, 0, 1)
            pagina_adicionarvendas.ids["unidades_kg"].color = (1, 0, 0, 1)

        if not preco:
            pagina_adicionarvendas.ids["label_preco"].color = (1, 0, 0, 1)
        else:
                try:
                    preco = float(preco)
                except:
                    pagina_adicionarvendas.ids["label_preco"].color = (1, 0, 0, 1)


        if not quantidade:
            pagina_adicionarvendas.ids["label_quantidade"].color = (1, 0, 0, 1)
        else:
                try:
                    quantidade = float(quantidade)
                except:
                    pagina_adicionarvendas.ids["label_quantidade"].color = (1, 0, 0, 1)

        # dado que o cliente preencheu todos os campos, vamos executar o codigo Adicionar vendas

        if cliente and produto and unidade and preco and quantidade and (type(preco) == float) and (type(quantidade) == float):
            foto_produto = produto + ".png"
            foto_cliente = cliente + ".png"

            info = f'{{"cliente": "{cliente}", "produto": "{produto}", "foto_cliente": "{foto_cliente}","foto_produto": "{foto_produto}", "data": "{data}", "unidade": "{unidade}", "preco": "{preco}", "quantidade": "{quantidade}"}}'

            requests.post(f"https://aplicativo-e340d-default-rtdb.firebaseio.com/{self.local_id}/vendas.json", data=info)

            banner = BannerVendas(cliente=cliente, produto=produto, foto_cliente=foto_cliente, foto_produto=foto_produto, data=data, preco=preco, quantidade=quantidade, unidade=unidade)
            pagina_homepage = self.root.ids["homepage"]
            lista_vendas = pagina_homepage.ids["lista_vendas"]
            lista_vendas.add_widget(banner)

            requisicao = requests.get(f"https://aplicativo-e340d-default-rtdb.firebaseio.com/{self.local_id}/total_vendas.json")
            total_vendas = float(requisicao.json())
            total_vendas += preco

            info = f'{{"total_vendas": "{total_vendas}"}}'
            requests.patch(f"https://aplicativo-e340d-default-rtdb.firebaseio.com/{self.local_id}.json", data=info)
            # atualizar o label de total de vendas na homepage
            homepage = self.root.ids["homepage"]
            homepage.ids["label_total_vendas"].text = f"[color=#000000]Total de Vendas: [/color] [b]R${total_vendas}[/b]"

            self.mudar_tela("homepage")


        self.cliente = None
        self.produto = None
        self.unidade = None
    def carregar_todas_vendas(self):
        # banner na pagina
        pagina_todasvendas = self.root.ids["todasvendaspage"]
        lista_vendas = pagina_todasvendas.ids["lista_vendas"]

        # excluir duplicatas da pagina de carregar vendas
        for item in list(lista_vendas.children):
            lista_vendas.remove_widget(item)


        # preencher com foto de vendas da empresa
        foto_perfil = self.root.ids['foto_perfil']
        foto_perfil.source = f"icones/fotos_perfil/hash.png"



        # pegar informações
        requisicao = requests.get(f'https://aplicativo-e340d-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"')
        requisicao_dic = requisicao.json()


        total_vendas = 0
        for local_id_usuario in requisicao_dic:
            try:
                vendas = requisicao_dic[local_id_usuario]["vendas"]
                for id_venda in vendas:
                    venda = vendas[id_venda]
                    total_vendas += float(venda["preco"])
                    banner = BannerVendas(cliente=venda["cliente"], foto_cliente=venda["foto_cliente"],
                                          produto=venda["produto"], foto_produto=venda["foto_produto"],
                                          data=venda["data"], preco=venda["preco"],
                                          unidade=venda["unidade"], quantidade=venda["quantidade"])
                    lista_vendas.add_widget(banner)
            except Exception as execao:
                 print(execao)
    #
            pagina_todasvendas.ids["label_total_vendas"].text = f"[color=#000000]Total de Vendas: [/color] [b]R${total_vendas}[/b]"
            self.mudar_tela('todasvendaspage')
    def sair_todas_vendas(self):
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{self.avatar}"
        self.mudar_tela('ajustespage')



MainApp().run()

