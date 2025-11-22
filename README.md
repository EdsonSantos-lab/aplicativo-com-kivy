# Criação de Aplicativo para Celular com Kivy

Este projeto demonstra a criação de um aplicativo mobile utilizando Kivy, um framework Python multiplataforma capaz de gerar apps para Android, Windows, Linux e mais.
O foco deste projeto é ensinar a estrutura, funcionamento e boas práticas para desenvolvimento de aplicativos completos.

🚀 Sobre o Projeto

O aplicativo foi desenvolvido utilizando:

Python 3

Kivy (interface e interação)

Firebase (autenticação e banco de dados)

Buildozer (para gerar APK Android)

O projeto possui várias telas, integração com banco de dados, lógica de autenticação, carregamento de dados e funcionalidades completas.

📚 Conteúdo do Curso / Aulas

Leia antes de começar — 00:15

Apresentação do Aplicativo — 06:52

Telas e Funcionalidades do Aplicativo — 9:43

Configurando nosso sistema — 05:33

Como iniciar qualquer Aplicativo Kivy — 06:36

Funcionamento básico dos arquivos KV — 9:21

Criando uma tela no aplicativo — 04:37

Criar um gerenciador de telas — 07:40

Criando uma nova página (Ajustes) — 04:13

Criando função para navegar entre telas — 15:25

Funcionamento do FloatLayout — 15:42

Aplicação do FloatLayout — 17:01

Imagem como Fundo de Tela e Canvas — 10:42

Botões Personalizados — 9:02

Ajustando Layout da Página Ajustes — 22:45

Ajustando Layout da Home — 13:59

Criando várias páginas — 15:04

Criando Banco de Dados Firebase — 17:54

Pegando informações do Banco — 11:21

Atualização do KV via Python — 06:43

ScrollView — 14:57

Adicionando Banner via Python — 10:04

Criando Widget Banner de Vendas — 33:32

Lista de Fotos de Perfil — 17:51

Atualizando Foto no Firebase — 14:48

Página Login — 20:40

Criando Conta com Google API — 18:28

Exibindo Erros — 10:15

Salvando Token — 15:41

Criando Usuário no Banco — 10:31

Carregando Dados após Criar Conta — 9:10

Mantendo Login — 16:02

Função de Login — 9:16

Criando ID Compartilhável — 16:57

Preenchendo Total de Vendas e ID — 10:02

Página Adicionar Vendedor — 11:05

Banner Vendedor + Banco — 40:58

Adicionando Vendedor à Equipe — 24:21

Tela Adicionar Vendas — 19:49

Lista de Clientes e Produtos — 12:23

Marcar Cliente Selecionado — 25:13

Adicionar Venda no Banco — 42:41

Bug da Home — 11:54

Página de Todas as Vendas — 23:11

Vendas Duplicadas / Outros Vendedores — 07:23

Carregar Info de Outros Vendedores — 25:28

Ajustando Botão Voltar — 05:03

Corrigindo Vendas Sobrepostas — 05:05

Regras de Segurança Firebase — 19:50

Autenticação Firebase nas Requisições — 13:51

Encerrando o Aplicativo — 03:28

Deploy Android – GitHub — 10:54

Deploy – Ajustando o Código — 07:24

Deploy – Gerar APK/AAB — 1:01:35

Deploy – Release AAB — 13:57



Arquivo de interface do aplicativo.
1. main.kv
Responsável por:

Estrutura das telas

Layouts (BoxLayout, FloatLayout, GridLayout)

Componentes (botões, labels, inputs, imagens)

Posições, tamanhos e comportamento visual

Widgets personalizados (banners, cards, listas)

Navegação via ScreenManager

Toda a parte visual do app está concentrada aqui.

2. myfirebase.py

Arquivo responsável pela comunicação com o Firebase.

Inclui:

Login e Criação de Usuário (Firebase Auth via Google REST API)

Salvamento de token

Regras de autenticação

Funções para criar, buscar, atualizar e deletar dados

Comunicação com o Realtime Database

Funções reutilizáveis para todo o app

Esse arquivo é o “cérebro” do backend do aplicativo.




