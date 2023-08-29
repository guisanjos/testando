from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from bs4 import BeautifulSoup
import requests

# Configs Telegram
token = '6603448630:AAHoOqEE3pXlyItk_3iBKoeZ3NpmGkE4rIU'
chat_id = '1292526319'

# Chrome Driver
var_strChromeDriver = 'C:\Treinamento\chromedriver-win64\chromedriver-win64\chromedriver.exe'

# Variáveis de tela de Login
var_strUrlLogin = 'https://dashboard.1daybot.com/login'
var_strUsuario = 'guilhermedosanjos.2001@gmail.com'
var_strSenha = 'Guitarra345'

# Variável de redirecionamento
var_strUrlArbitragem = 'https://dashboard.1daybot.com/manual-arbitration'

# Configurando as opções do navegador
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito') # Janela Anônima
# chrome_options.add_argument('--headless') # Background

# Inicialize o driver do Selenium
driver = webdriver.Chrome(executable_path=var_strChromeDriver, options=chrome_options)

# Abra a página de login
driver.get('https://dashboard.1daybot.com/login')
driver.maximize_window()

# Preencha os campos de usuário e senha
usuario = driver.find_element(By.XPATH, '//input[@id="login-email"]')
senha = driver.find_element(By.XPATH, '//input[@id="login-password"]')

usuario.send_keys(var_strUsuario)  # Substitua 'seu_usuario' pelo seu nome de usuário
senha.send_keys(var_strSenha)      # Substitua 'sua_senha' pela sua senha
senha.send_keys(Keys.TAB) # Dá um TAB na senha para atualizar o campo

# Clique no botão de login
sleep(1)
login_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
login_btn.click()

# Aguarde até que o elemento 'DASHBOARD' apareça
wait = WebDriverWait(driver, 30)
dashboard_element = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[@class='content-header-title float-left pr-1 mb-0']")))

# Navegue para a tela de Arbitragem
driver.get('https://dashboard.1daybot.com/manual-arbitration')

encontrado = False

while encontrado == False:

    wait = WebDriverWait(driver, 30)
    dashboard_element = wait.until(EC.presence_of_element_located((By.XPATH, "//h4[@class='text-lg']")))

    # Encontre todos os elementos "card-body"
    card_bodies = driver.find_elements_by_xpath('//div[@class="card-body"]')

    # Itere por todos os cards
    for indice, card_body in enumerate(card_bodies):
        # Use XPath para localizar o elemento com o valor da porcentagem
        percentual_element = card_body.find_element_by_xpath('.//p[contains(text(), "Diferença percentual:")]/following-sibling::p[@class="h5 text-info"]')

        # Obtenha o valor da porcentagem como uma string
        percentual_str = percentual_element.text

        # Remova o caractere de porcentagem e converta para um número decimal
        percentual = float(percentual_str.strip('%'))

        # Verifique se o maior percentual é igual a 0.4
        if percentual >= 0.4:

            # Encontrou o percentual desejado, clique no botão "Executar Operação" do card correspondente

            btn_executar = card_body.find_element_by_xpath('.//button[contains(text(), "Executar operação")]')
            btn_executar.click()

            btn_license = driver.find_element(By.XPATH, "//button[@class='list-group-item list-group-item-action']")
            btn_license.click()

            encontrado = True

            requests.get('https://api.telegram.org/bot' + token +"/sendMessage?chat_id="+ chat_id + "&text=" + "Executada a Operação. Valor: " + str(percentual))

            break  # Saia do loop do For Each
        
    # Se o maior percentual não for igual a 0.4, faça um refresh na página e continue procurando
    driver.refresh()

print("Sucesso na execução")
driver.quit()

