import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from datetime import date
from datetime import datetime
import chromedriver_autoinstaller
from pyvirtualdisplay import Display
import pandas as pd
import pytz
import os

email = os.environ["email"]
login = os.environ["login"]
senha = os.environ["senha"]
meu_email = os.environ["meu_email"]

fuso_horario_local = datetime.now().astimezone().tzinfo
print("Fuso horário local:", fuso_horario_local)

fuso_horario_brasilia = pytz.timezone('America/Sao_Paulo')
print("Fuso horário de Brasília:", fuso_horario_brasilia)

agora_local = datetime.now(fuso_horario_local)
print("Data e hora local:", agora_local)

# Converte a data e hora local para o fuso horário de Brasília
agora_brasilia = agora_local.astimezone(fuso_horario_brasilia)
print("Data e hora em Brasília:", agora_brasilia)

display = Display(visible=0, size=(1366,768))  
display.start()

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

chrome_options = webdriver.ChromeOptions()    
# Add your options as needed    
options = [
  # Define window size here
   "--window-size=1366,768",
    "--ignore-certificate-errors"
    "--oobe-timezone-override"
    #"--headless",
    #"--disable-gpu",
    #"--window-size=1920,1200",
    #"--ignore-certificate-errors",
    #"--disable-extensions",
    #"--no-sandbox",
    #"--disable-dev-shm-usage",
    #'--remote-debugging-port=9222'
]

for option in options:
    chrome_options.add_argument(option)

chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'pt,pt_BR'})

    
driver = webdriver.Chrome(options = chrome_options)

# Descobre o dia do próximo jogo
driver.get(
    'https://www.google.com/search?client=opera-gx&q=jogo+do+gremio&sourceid=opera&ie=UTF-8&oe=UTF-8#sie=t;/m/019m51;2;/m/0fnk7q;mt;fp;1;;;')
time.sleep(5)



dia_hoje, mes_hoje, ano_hoje = str(date.today()).split('-')[2], str(date.today()).split('-')[1], \
str(date.today()).split('-')[0]
if int(ano_hoje) % 4 == 0:
    fev = 29
else:
    fev = 28

dias_nos_meses = [31, fev, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

for i in range(5):
    data_do_jogo = driver.find_elements(By.XPATH,
                                        '//*[@id="liveresults-sports-immersive__updatable-team-matches"]/div[1]/div/table/tbody/tr[15]/td[1]/div/div/div/table/tbody/tr[3]/td[3]/div/div/div/div[1]')[
        0].text
    ultimo_jogo = driver.find_elements(By.XPATH,
                                       '//*[@id="liveresults-sports-immersive__updatable-team-matches"]/div[1]/div/table/tbody/tr[14]/td[2]/div/div/div/table/tbody/tr[3]/td[3]/div[1]/div/div[2]/span')[
        0].text
    print(data_do_jogo)
    if data_do_jogo == "Amanhã":
        dia_do_jogo, mes_do_jogo = str(int(dia_hoje) + 1), mes_hoje
    elif data_do_jogo == "Hoje":
        dia_do_jogo, mes_do_jogo = dia_hoje, mes_hoje
    elif data_do_jogo == "Ontem":
        dia_do_jogo, mes_do_jogo = str(int(dia_hoje) - 1), mes_hoje
    else:
        data_do_jogo = data_do_jogo.split(sep='/')
        dia_do_jogo, mes_do_jogo = data_do_jogo[0][len(data_do_jogo[0]) - 2:len(data_do_jogo[0])], data_do_jogo[1]
    dia_do_jogo = str(int(dia_do_jogo))
    adversario = driver.find_elements(By.CSS_SELECTOR, 'div[class="liveresults-sports-immersive__hide-element"]')
    mandante = adversario[56 + 2 * i].text
    visitante = adversario[57 + 2 * i].text
    horario = driver.find_element(By.CSS_SELECTOR,
                                  'div[class="imspo_mt__ndl-p imspo_mt__pm-inf imspo_mt__pm-infc imso-medium-font"]').text
    if mes_do_jogo == mes_hoje:
        if dia_do_jogo >= dia_hoje:
            break
    elif mes_do_jogo > mes_hoje:
        break

print(horario)

# Abre a agenda e marca o jogo
if ultimo_jogo == "Ontem":
    driver.get(
        'https://accounts.google.com/v3/signin/identifier?dsh=S-2147361052%3A1687457378165668&continue=https%3A%2F%2Fwww.google.com.br%2F%3Fhl%3Dpt-BR&ec=GAZAmgQ&hl=pt-BR&ifkv=Af_xneErVfVvqkiHY5cyJjLeVVju0xBl2DLNF0Xj0P12mebqOJQ27IhLAJCo8QfGoLW4_0eHtHUE&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
    driver.find_element(By.CSS_SELECTOR, 'input[class="whsOnd zHQkBf"]').send_keys(meu_email)
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR,
                        'button[class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b"]').click()
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, 'input[class="kc-input-class"]').send_keys(login)
    driver.find_element(By.CSS_SELECTOR, 'input[id="password"]').send_keys(senha)
    time.sleep(4)
    driver.find_element(By.CSS_SELECTOR, 'input[class="kc-button-class  "]').click()
    time.sleep(7)
    driver.get('https://calendar.google.com/calendar/u/0/r')
    time.sleep(5)

    while True:
        driver.find_element(By.XPATH, '//*[@id="gb"]/div[2]/div[2]/div[1]/div/div/div[1]/div/span[3]/button').click()
        data_agenda = driver.find_element(By.CSS_SELECTOR, 'div[class="rSoRzd"]').text.split(' ')
        dia_ag, mes_ag = data_agenda[1][0:2], data_agenda[0]
        dia_ag = dia_ag.replace(",", "")
        print(dia_ag)
        if dia_ag == dia_do_jogo:
            break
    driver.find_element(By.CSS_SELECTOR, 'div[class="U26fgb c7fp5b FS4hgd GDoOPd mAozAc"]').click()
    time.sleep(15)
    driver.find_element(By.CSS_SELECTOR, 'div[class="jO7h3c"]').click()
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, 'input[class="VfPpkd-fmcmS-wGMbrd "][aria-label="Add title"]').send_keys(
        mandante + ' x ' + visitante)
    time.sleep(4)
    driver.find_element(By.CSS_SELECTOR,
                        'span[data-key="startTime"]').click()
    time.sleep(4)
    driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Start time"]').send_keys(
        str(int(horario.split(':')[0]) % 12) + ':' + horario.split(':')[1] + ['am', 'pm'][
            int(horario.split(':')[0]) // 12])
    time.sleep(4)
    driver.find_element(By.CSS_SELECTOR, 'input[aria-label="End time"]').send_keys(
        str((int(horario.split(':')[0]) + 2) % 12) + ':' + horario.split(':')[1] + ['am', 'pm'][
            (int(horario.split(':')[0]) + 2) // 12])
    time.sleep(6)
    driver.find_element(By.XPATH,
                        '//*[@id="yDmH0d"]/div/div/div[2]/span/div/div[1]/div[2]/div[2]/div[4]/button').click()

# garante que está logado no e-mail
if data_do_jogo == "Amanhã":
  driver.get(
        'https://accounts.google.com/v3/signin/identifier?dsh=S-2147361052%3A1687457378165668&continue=https%3A%2F%2Fwww.google.com.br%2F%3Fhl%3Dpt-BR&ec=GAZAmgQ&hl=pt-BR&ifkv=Af_xneErVfVvqkiHY5cyJjLeVVju0xBl2DLNF0Xj0P12mebqOJQ27IhLAJCo8QfGoLW4_0eHtHUE&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
  driver.find_element(By.CSS_SELECTOR, 'input[class="whsOnd zHQkBf"]').send_keys(meu_email)
  time.sleep(1)
  driver.find_element(By.CSS_SELECTOR,
                        'button[class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b"]').click()
  time.sleep(5)
  driver.find_element(By.CSS_SELECTOR, 'input[class="kc-input-class"]').send_keys(login)
  driver.find_element(By.CSS_SELECTOR, 'input[id="password"]').send_keys(senha)
  time.sleep(4)
  driver.find_element(By.CSS_SELECTOR, 'input[class="kc-button-class  "]').click()
  time.sleep(7)

emails = pd.read_csv(email)# envia os e-mails
emails = emails.iloc[:,1]
# envia os e-mails
if ultimo_jogo == "Ontem":
    for email in emails:
        time.sleep(7)
        driver.get('https://mail.google.com/mail/u/0/#inbox?compose=new')
        time.sleep(8)
        driver.find_element(By.CSS_SELECTOR, 'input[class="agP aFw"]').send_keys(email)
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, 'input[name="subjectbox"]').send_keys(
            'Próximo jogo: ' + mandante + ' x ' + visitante + ' às ' + horario)
        if mandante == "Grêmio":
            adversario = visitante
        else:
            adversario = mandante
        driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Corpo da mensagem"]').send_keys(
            'Olá!\nVenho por meio desta avisar que o próximo jogo do Grêmio é ' + ' '.join(
                data_do_jogo) + ".\nO jogo é contra o " + adversario + ". Vai dar tudo certo e o Grêmio vai ganhar desse timinho!!!\n\nAté um dia desses!\nE-mail enviado automaticamente pelo Lucas")
        driver.fullscreen_window()
        time.sleep(5)
        driver.find_element(By.CSS_SELECTOR, 'div[data-tooltip="Enviar"]').click()
        time.sleep(5)

if data_do_jogo == "Amanhã":
    for email in emails:
        time.sleep(7)
        driver.get('https://mail.google.com/mail/u/0/#inbox?compose=new')
        time.sleep(8)
        driver.find_element(By.CSS_SELECTOR, 'input[class="agP aFw"]').send_keys(email)
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, 'input[name="subjectbox"]').send_keys(
            'Próximo jogo: ' + mandante + ' x ' + visitante + ' às ' + horario)
        if mandante == "Grêmio":
            adversario = visitante
        else:
            adversario = mandante
        driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Corpo da mensagem"]').send_keys(
            'Olá!\nVenho por meio desta lembrar que amanhã tem jogo do Grêmio às' + horario + ".\nO jogo é contra o " + adversario + ". Vai dar tudo certo e o Grêmio vai ganhar desse timinho!!!\n\nAté um dia desses!\nE-mail enviado automaticamente pelo Lucas")
        driver.fullscreen_window()
        time.sleep(5)
        driver.find_element(By.CSS_SELECTOR, 'div[data-tooltip="Enviar"]').click()
        time.sleep(5)
