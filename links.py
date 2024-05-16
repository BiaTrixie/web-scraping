from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import csv

# Configurar as opções do Chrome para executar em modo headless
chrome_options = Options()
chrome_options.add_argument("--headless")

# Inicializar o driver do navegador Chrome com as opções configuradas
driver = webdriver.Chrome(options=chrome_options)

# URL da página que contém os links para os imóveis
url = "https://www.atresimobiliaria.com.br/imoveis/para-alugar"

# Fazer a requisição HTTP
driver.get(url)

# Função para rolar a página até o final
def scroll_to_bottom():
    # Rolar a página até o final
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Aguardar alguns segundos para o carregamento dos novos elementos após a rolagem
    time.sleep(5)

# Rolar até o final da página quando ela for carregada
scroll_to_bottom()

# Aguardar alguns segundos para garantir que todos os elementos tenham sido carregados
time.sleep(5)

# Função para clicar automaticamente no botão "Ver mais" e aguardar o carregamento dos novos elementos
def click_ver_mais():
    try:
        # Encontrar o botão "Ver mais"
        ver_mais_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-md.btn-primary.btn-next")
        # Verificar se o texto do span dentro do botão é "Ver mais"
        if ver_mais_button.text.strip() == "Ver mais":
            # Clicar no botão "Ver mais"
            ver_mais_button.click()
            return True
        else:
            print("O botão não contém o texto 'Ver mais'.")
            return False
    except:
        print("O botão 'Ver mais' não foi encontrado.")
        return False

# Enquanto o botão "Ver mais" estiver presente e contiver o texto "Ver mais", clique nele
while click_ver_mais():
    # Rolagem automática após clicar no botão "Ver mais"
    scroll_to_bottom()

# Obter o HTML atualizado da página
html = driver.page_source

# Criar um objeto BeautifulSoup com o conteúdo da página
soup = BeautifulSoup(html, "html.parser")

# Encontrar todos os elementos <a> com a classe "card-with-buttons borderHover"
link_elements = soup.find_all("a", class_="card-with-buttons borderHover")

# Criar um novo arquivo CSV para salvar os links
with open('links_imoveis.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Criar o escritor CSV
    writer = csv.writer(csvfile)
    
    # Iterar sobre os elementos encontrados e escrever os links no arquivo CSV
    for link_element in link_elements:
        # Obter o link completo
        link = "https://www.atresimobiliaria.com.br" + link_element.get('href')
        writer.writerow([link])

print("Links dos imóveis foram coletados e salvos com sucesso.")

# Fechar o navegador
driver.quit()
