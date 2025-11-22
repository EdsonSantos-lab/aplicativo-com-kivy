from kivy.app import App
import requests

class Myfarebase ():
    API_KEY = "AIzaSyAI5vRGCsvwRT8EJsrYX41VkrLgL7QZwOU"

    def criar_conta(self, email, senha):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}"
        info = {"email": email,
                "password": senha,
                "returnSecureToken": True}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
        if requisicao.ok:

            id_token = requisicao_dic["idToken"] # autenticação
            local_id = requisicao_dic["localId"] # id do usuario
            refresh_token = requisicao_dic["refreshToken"] # token que mantem o usuario logado

            meu_aplicativo = App.get_running_app()
            meu_aplicativo.local_id = local_id
            meu_aplicativo.id_token = id_token

            with open("refreshToken.txt", "w") as arquivo:
                arquivo.write(refresh_token)

            req_id = requests.get("https://aplicativo-e340d-default-rtdb.firebaseio.com/proximo_id_vendedor.json")
            req_id_vendedor = req_id.json()
            link_id = f"https://aplicativo-e340d-default-rtdb.firebaseio.com/{local_id}.json"
            info_usuario = f'{{"avatar": "foto1.png", "equipe": "", "total_vendas": "0", "vendas": "", "id_vendedor": "{req_id_vendedor}"}}'
            requisicao_usuario = requests.patch(link_id, data=info_usuario)

            # atualizar o proximo valor do id vendedor
            proximo_id_vendedor = int(req_id_vendedor) +1
            info_id_vendedor = f'{{"proximo_id_vendedor": "{proximo_id_vendedor}"}}'
            requests.patch("https://aplicativo-e340d-default-rtdb.firebaseio.com/.json", data=info_id_vendedor)

            meu_aplicativo.carregar_informacaoes_usuario()
            meu_aplicativo.mudar_tela("homepage")

        else:
            messagem_erro = requisicao_dic["error"]["message"]
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["loginpage"]
            pagina_login.ids["mensagem_login"].text = messagem_erro
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)



    def faser_login(self, email, senha):

        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}"
        info = {"email": email,
                "password": senha,
                "returnSecureToken": True}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()

        if requisicao.ok:
            id_token = requisicao_dic["idToken"]  # autenticação
            local_id = requisicao_dic["localId"]  # id do usuario
            refresh_token = requisicao_dic["refreshToken"]  # token que mantem o usuario logado

            meu_aplicativo = App.get_running_app()
            meu_aplicativo.local_id = local_id
            meu_aplicativo.id_token = id_token

            with open("refreshToken.txt", "w") as arquivo:
                arquivo.write(refresh_token)

            meu_aplicativo.carregar_informacaoes_usuario()
            meu_aplicativo.mudar_tela("homepage")

        else:
            messagem_erro = requisicao_dic["error"]["message"]
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["loginpage"]
            pagina_login.ids["mensagem_login"].text = messagem_erro
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)

