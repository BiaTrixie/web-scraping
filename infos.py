import csv
import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Função para obter o conteúdo do elemento span de uma URL
def get_content(url):
    try:
        # Definindo um cabeçalho de usuário simulando um navegador web
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
        }
        # Faz a requisição HTTP com o cabeçalho definido
        response = requests.get(url, headers=headers)
        # Verifica se a requisição foi bem sucedida
        if response.status_code == 200:
            # Faz o parsing do HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            # Encontra o elemento span do título
            title_element = soup.select_one('.cont-title span')
            # Encontra o elemento div do 'Sobre'
            about_element = soup.find('div', class_='info-primary digital')
            # Encontra o elemento span da descrição
            description_element = soup.select_one('.box-detail span')
            # Encontra o elemento div das características
            amenities_element = soup.find('div', class_='box-amenities')
            # Retorna o título, sobre, descrição e características
            title = title_element.text.strip() if title_element else "Título não encontrado"
            about = about_element.text.strip() if about_element else "Sobre não encontrado"
            description = description_element.text.strip() if description_element else "Descrição não encontrada"
            amenities = amenities_element.text.strip() if amenities_element else "Características não encontradas"
            return title, about, description, amenities
        else:
            return f"Erro ao acessar a URL: {response.status_code}"
    except Exception as e:
        return f"Erro durante o acesso à URL: {str(e)}"

# Lista para armazenar os títulos, descrições e características
properties = []

# Abre o arquivo CSV e lê os URLs
with open('links_imoveis.csv', 'r') as file:
    reader = csv.reader(file)
    # Pula o cabeçalho se existir
    next(reader, None)
    # Itera sobre as linhas do arquivo CSV
    for row in reader:
        url = row[0]
        # Obtém o título, sobre, descrição e características da URL atual
        title, about, description, amenities = get_content(url)
        # Adiciona o título, sobre, descrição e características à lista
        properties.append((url, title, about, description, amenities))

# Criar documento PDF
doc = SimpleDocTemplate("infos.pdf", pagesize=letter)
styles = getSampleStyleSheet()

# Conteúdo do PDF
content = []

# Adicionar cabeçalho
content.append(Paragraph("Imóveis", styles['Title']))

# Adicionar informações de cada imóvel
for url, title, about, description, amenities in properties:
    content.append(Paragraph(f"URL: {url}", styles['Normal']))
    content.append(Paragraph(f"Título: {title}", styles['Normal']))
    content.append(Paragraph(f"Sobre: {about}", styles['Normal']))
    content.append(Paragraph(f"Descrição: {description}", styles['Normal']))
    content.append(Paragraph(f"Características: {amenities}", styles['Normal']))
    # Adiciona espaço em branco entre os imóveis
    content.append(Spacer(1, 12))  # 12 é a altura em pontos
    # Adiciona um parágrafo em branco para separar os imóveis
    content.append(Paragraph("\n", styles['Normal']))

# Adicionar conteúdo ao documento
doc.build(content)
