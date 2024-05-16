import subprocess

# Diretório onde os scripts estão localizados
script_directory = "C:\\Users\\beatr\\OneDrive\\Documents\\python\\scrapping\\"

# Executar o script links.py
print("Executando links.py...")
subprocess.run(["python", script_directory + "links.py"])

# Executar o script infos.py
print("Executando infos.py...")
subprocess.run(["python", script_directory + "infos.py"])

# Executar o script upload.py
print("Executando upload.py...")
subprocess.run(["python", script_directory + "upload.py"])

print("Todos os scripts foram executados com sucesso.")
input("Pressione Enter para sair...")
