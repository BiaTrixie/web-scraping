from openai import OpenAI

# Inicialize o cliente OpenAI
client = OpenAI()

# ID do vetor existente
vector_store_id = "vs_3RdjwlHA5gHR1BLBOtYU33P9"

# Lista todos os arquivos do vetor
vector_store_files = client.beta.vector_stores.files.list(vector_store_id=vector_store_id)

# Itera sobre a lista de arquivos e exclui cada um deles
for file in vector_store_files:
    deleted_file = client.beta.vector_stores.files.delete(vector_store_id=vector_store_id, file_id=file.id)
    if deleted_file.id:
        print(f"Arquivo {file.id} excluído com sucesso.")
    else:
        print(f"Falha ao excluir o arquivo {file.id}.")

# Após excluir todos os arquivos, você pode adicionar o novo arquivo
# Carregar o novo arquivo para a OpenAI
uploaded_file = client.files.create(
    file=open("infos.pdf", "rb"),
    purpose="assistants"
)

# Verifique se o upload foi bem-sucedido
if uploaded_file.id:
    print("Arquivo carregado com sucesso. ID do arquivo:", uploaded_file.id)
    # Adicione o novo arquivo ao vetor
    vector_store_file = client.beta.vector_stores.files.create(
        vector_store_id=vector_store_id,
        file_id=uploaded_file.id
    )
    # Verifique se o arquivo foi adicionado ao vetor com sucesso
    if vector_store_file.id:
        print("Arquivo adicionado com sucesso ao vetor. ID do arquivo no vetor:", vector_store_file.id)
    else:
        print("Erro ao adicionar o arquivo ao vetor.")
else:
    print("Erro ao carregar o arquivo.")
