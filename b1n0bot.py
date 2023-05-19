#testar com o run_grep e run_wgrep
# o bot agora precisa receber um input junto com o comando
import telebot
import subprocess

botToken_API = "5898652267:AAFqK7EwtLJMVLd6_TUYzg0fcmsTjIVfimo"

bot = telebot.TeleBot(botToken_API)

####################################################################################################
################################## Parâmetros Globais ##############################################

showMenuCommand = "/menu"            #comando para mostrar menu
limiteResultados = 70                #limite de resultados que aparecerão
sistemaOperacional = ['Windows', 'Linux']
soHospedagem = sistemaOperacional[0] # escolher   0 - Windows 
                                     #            1 - Linux

initialMessage = """                              
b1n0 Consultant

Selecione uma opção:
    /cpf       - Puxa dados com o cpf - não usar pontuação (exemplo: /cpf 12345678911 )

    /nome     - Puxa dados com o nome - não usar acentuação (exemplo: /nome jose braganca sou)

    /opt3      - opções futuras...
"""

####################################################################################################
####################################### FilePaths ##################################################
filename = 'c:\\Users\\Parizzi\\Desktop\\jbr_PF.txt'




####################################################################################################
##################################### Funções Greps ###############################################

#Windows
def run_wgrep(pattern):
  print("usuário deu o Input: "+pattern)
  comando = ['powershell.exe', 'findstr', '/i', '/C:'+"\""+pattern+"\"", filename]
  resultado = subprocess.run(comando, capture_output=True, text=True)

  if resultado.returncode == 0:
      saida = resultado.stdout
      linhas = len(saida.strip().split('\n'))
      print('pesquisa realizada com o input: '+pattern)
      print(f"Número de pessoas que possuem nome ou CPF similar: {linhas}")
      if linhas > limiteResultados:
          print("O input encontrou mais resultados que o limite definido, o usuário foi orientado para ser mais específico.")
          return(f"muitos resultados que contenham \"{pattern}\": {linhas} pessoas, seja mais específico no nome ou CPF")
      else:
          print("resposta enviada para o solicitante")
          return((f"Número de pessoas com nome ou CPF similar: {linhas}\n\n")+saida)
  else:
      erro = resultado.stderr
      print(erro)
      print("Usuário deu o Input: "+pattern)
      print("Não foi possível encontrar este nome ou CPF")
      return("Não foi possível encontrar este nome ou CPF")


#Linux
def run_grep(pattern):
    try:
        # Executa o comando 'grep' com as opções e argumentos fornecidos
        output = subprocess.check_output(['grep', '-i', pattern, filename])
        
        # Decodifica a saída do comando para uma string legível
        output = output.decode('utf-8')
        
        # Print da saída
        print(output)
    except subprocess.CalledProcessError as e:
        # Caso ocorra um erro ao executar o comando 'grep' - verificar quando não acha resultado
        print(f"Erro: {e}")

# Exemplo de uso no linux - precisa testar
#arquivo = 'exemplo.txt'
#padrao = 'palavra'
#run_grep(padrao, arquivo)



####################################################################################################
################################# Comandos - Opções ################################################
@bot.message_handler(commands=["cpf", "CPF", "Cpf"]) #tipos de comandos aceitos para iniciar o código
def cpf(mensagem):
  cpf_em_pesquisa = mensagem.text.lower().split("/cpf ", 1)[1] # text.lower() deixa Case Insensitive
  bot.reply_to(mensagem, "Pesquisando CPF: " + cpf_em_pesquisa)  # manobra para que seja dado o comando /cpf <numero>

#cpf
  if soHospedagem == "Windows": #Verifica se o bot está em um windows
    resposta = run_wgrep(cpf_em_pesquisa)
  elif soHospedagem == "Linux":
    resposta = run_grep(cpf_em_pesquisa)
  else:
    resposta = "erro a definir Sistema Operacional de hospedagem"

  bot.reply_to(mensagem, resposta) #ato de responder

#nome
@bot.message_handler(commands=["nome", "Nome", "NOME"])
def nome(mensagem):
  nome_em_pesquisa = mensagem.text.lower().split("/nome ", 1)[1] # text.lower() deixa Case Insensitive
  bot.reply_to(mensagem, "Pesquisando nome: " + nome_em_pesquisa)


  if soHospedagem == "Windows": #Verifica se o bot está em um windows
    resposta = run_wgrep(nome_em_pesquisa)
  elif soHospedagem == "Linux":
    resposta = run_grep(nome_em_pesquisa)
  else:
    resposta = "erro a definir Sistema Operacional de hospedagem"

  bot.reply_to(mensagem, resposta) #ato de responder


@bot.message_handler(commands=["opt2"]) #usar no futuro
def nome(mensagem):
  bot.reply_to("pesquisando Opt...")
    
  if soHospedagem == "Windows":
    resposta = run_wgrep()
  elif soHospedagem == "Linux":
    resposta = run_grep()
  else:
    resposta = "erro a definir Sistema Operacional de hospedagem"


    bot.reply_to(mensagem, resposta)
    pass

@bot.message_handler(commands=["opt3"]) #usar no futuro
def opt3(mensagem):
    bot.reply_to("essa opção ainda será construída para outros fins")    

    bot.reply_to(mensagem, resposta)
    pass




########################################################################################################
#funções operacionais








########################################################################################################
#funcionamento inicial do bot
def initialInput(mensagem):
    if mensagem.text.lower() == showMenuCommand:  #text.lower() deixa Case Insensitive
        return True
    else:
        return False

@bot.message_handler(func=initialInput)
def responder(mensagem):
    bot.reply_to(mensagem, initialMessage)

bot.polling() #manter bot rodando e escutando
