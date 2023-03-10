#https://www.youtube.com/watch?v=H-XpwSz4x8Y
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import telepot
import time, sys
from credenciais import chave,grupo

options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\Gilson Barbosa\AppData\Local\Google\Chrome\User Data\Profile 3") #e.g. 
options.add_argument(r'--profile-directory=YourProfileDir') #e.g. Profile 3
options.headless = False
navegador = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

valorMin = 900
valorMax = 1200
indice = 1
contadorMsg = -1

url = f'https://www.olx.com.br/videogames/estado-sp/sao-paulo-e-regiao?pe={valorMax}&ps={valorMin}&vgt=1&vgm=1&vgm=16&vgm=15'

navegador.get(url)

# Aguarda o usuário fazer login na página para que salve a sessão de login
input('Caso não esteja logado na conta, faça login e depois digite Enter: ')
while True:

   try:
      navegador.get(url)
      # Consultar o id do anuncio
      div = navegador.find_element_by_xpath(f'//*[@id="listing-main-content-slot"]/div[11]/div/div/div/ul/li[{indice}]/div/a') # Div master aonde está todas as informações   

      # Id do anuncio 1
      id1 = div.get_attribute('data-lurker_list_id')
      id2 = BeautifulSoup(id1, 'html.parser') # Id do anuncio
      id3 = str(id2)
      print('Primeiro id {}'.format(id2))
      
      # -------------------------- // --------------------------
      # Ler o TXT para saber se o número é igual ao anterior
      with open('id_anuncio.txt','r') as arquivo:
         for id_anuncio in arquivo:
            id_anuncio
            print('O id anterior é: {}'.format(id_anuncio))
      # -------------------------- // --------------------------
      # Primeiro ID do anuncio da página

      def idAtual():
         global id1, id2
         id1 = div.get_attribute('data-lurker_list_id')
         id2 = BeautifulSoup(id1, 'html.parser') # Id do anuncio
         print('ID atualizado {}'.format(id2))
      idAtual()

      #time.sleep(10)

      if id_anuncio != id3:
         
         # Traz os valores
         titulo  = div.get_attribute('title') # Título do anuncio
         titulo1 = BeautifulSoup(titulo, 'html.parser') # Título do anuncio
         titulo2 = str(titulo1)
         
         #valor do anuncio
         div2 = navegador.find_element_by_xpath(f'//*[@id="listing-main-content-slot"]/div[11]/div/div/div/ul/li[{indice}]/div/a/div/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/span')
         # Local 
         div3 = navegador.find_element_by_xpath(f'//*[@id="listing-main-content-slot"]/div[11]/div/div/div/ul/li[{indice}]/div/a/div/div[2]/div[2]/div[3]/div[1]/div/div/span')
         #postado
         div4 = navegador.find_element_by_xpath(f'//*[@id="listing-main-content-slot"]/div[11]/div/div/div/ul/li[{indice}]/div/a/div/div[2]/div[2]/div[3]/div[2]/span')

         # Buscar o paramentros
         link    = div.get_attribute('href') # Link do anuncio
         valor   = div2.get_attribute('innerText') # Valor do anuncio
         local   = div3.get_attribute('innerText') # Local do anuncio
         postado = div4.get_attribute('innerText') # Data de postagem do anuncio

         #resultados da busca dos parametros
         soup1 = BeautifulSoup(link, 'html.parser') # Link do anuncio  
         soup2 = BeautifulSoup(valor, 'html.parser') # Valor do anuncio
         soup3 = BeautifulSoup(local, 'html.parser') # Local do anuncio
         soup4 = BeautifulSoup(postado, 'html.parser') # Data do anuncio
         soup5 = str(soup1) # Link do anuncio em string

         consulta2 = str(soup1)# Link em string
         consulta3 = str(soup2)# Valor em string
         consulta4 = str(soup3)# Local em string
         consulta5 = str(soup4)# Data da postagem em string

         #time.sleep(5)
         # -------------------------- // --------------------------

         # -------------------------- // --------------------------
         # Atualiza o TXT com o novo id
         with open('id_anuncio.txt','w') as arquivo:
            arquivo.write(str(id3))

         # -------------------------- // --------------------------
         #Acessa o link do primeiro anuncio
         navegador.get(soup5)

         # -------------------------- // --------------------------
         #Descrição do anuncio
         descricao = navegador.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/div[28]/div/div/div')
         descricao1 = descricao.get_attribute('innerText') # Descrição do anuncio
         descricao2 = BeautifulSoup(descricao1, 'html.parser') 
         descricao3 = str(descricao2) # Descrição do anuncio em string

         # -------------------------- // --------------------------
          #Mensagem formatada para postar no telegram
         msgTelegram = f'Produto: {titulo2}\n\nValor: {consulta3}\n\nLocal: {consulta4}\n\nAnuncio: {consulta2}\n\nDescrição: {descricao3}\n\nPostagem: {consulta5}\n\n'

         # -------------------------- // --------------------------
         # Bot telegram
         chave = chave
         bot = telepot.Bot(chave)
         resposta = bot.getUpdates()

         # Envia mensagem no telegram
         bot.sendMessage(grupo, msgTelegram)   

         # -------------------------- // --------------------------

      else:
         print('Não encontrou produto novo, produto anterior {}'.format(id_anuncio))    
         

   except Exception as e:
      print('Falhou a busca')
   
   # -------------------------- // --------------------------      
   # Contagem para começar a nova busca
   for i in range(30,-1,-1):
    sys.stdout.write("\rNova busca vai ser executada em: {}".format(i))
    sys.stdout.flush()
    time.sleep(1)

   print ("\nRealizando Nova busca")
   # -------------------------- // --------------------------  