
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# PARA RODAR O CHROME EM 2NDO PLANO:
#=========================================================
"""
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.headless = True #also works
nav = webdriver.Chrome(options=chrome_options)
"""
#=========================================================
# Passo 1: Pegar a cotação do Dólar

# Abrir um navegador
navegador = webdriver.Chrome()

navegador.get("https://www.google.com/")

"""
navegador.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação dólar")

navegador.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

cotacao_dolar =  navegador.find_element_by_xpath('//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")
"""

# SELENIUM JUST REMOVED THE METHOD 'find_element_by_xpath()'. NOW NEED TO USE:

navegador.find_element("xpath",'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação dólar")

navegador.find_element("xpath",'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

cotacao_dolar =  navegador.find_element("xpath",'//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")
print(cotacao_dolar)

#=========================================================
# Passo 2: Pegar a cotação do Euro

navegador = webdriver.Chrome()

navegador.get("https://www.google.com/")

navegador.find_element("xpath",'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação euro")

navegador.find_element("xpath",'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

cotacao_euro =  navegador.find_element("xpath",'//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")

print(cotacao_euro)

#=========================================================
# Passo 3: Pegar a cotação do Ouro

navegador = webdriver.Chrome()

navegador.get("https://www.melhorcambio.com/ouro-hoje")

cotacao_ouro =  navegador.find_element("xpath",'//*[@id="comercial"]').get_attribute("value")

# substituindo o separador obtido para o formato padrão do python
cotacao_ouro =  cotacao_ouro.replace(",",".")

print(cotacao_ouro)

#=========================================================
# Passo 4: Importar a lista de produtos

import pandas as pd

tabela = pd.read_excel("Produtos.xlsx")
display(tabela)

#=========================================================
# Passo 5: Recalcular o preço de cada produto

# atualizar a cotação (nas linhas onde a coluna "Moeda" = Dólar)
tabela.loc[tabela["Moeda"] == "Dólar","Cotação"] = float(cotacao_dolar)
tabela.loc[tabela["Moeda"] == "Euro","Cotação"] = float(cotacao_euro)
tabela.loc[tabela["Moeda"] == "Ouro","Cotação"] = float(cotacao_ouro)
#display(tabela)

# atualizar o preço base reais (preço base original * cotação)
tabela["Preço Base Reais"] = tabela["Preço Base Original"] * tabela["Cotação"]

# atualizar o preço final (preço base reais * Margem)
tabela["Preço Final"] = tabela["Preço Base Reais"] * tabela["Margem"]

display(tabela)

#=========================================================
# Passo 6: Salvar os novos preços dos produtos. Agora vamos exportar a nova base de preços atualizada

tabela.to_excel("Produtos-ATUALIZADO.xlsx", index=False)