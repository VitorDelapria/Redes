import socket  # Importa o módulo de socket para comunicação de rede
import hashlib  # Importa o módulo hashlib para cálculo de hash
import os  # Importa o módulo os para manipulação de caminhos de arquivo

def main():
    # Cria um socket do cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conecta o socket a um endereço e porta específicos (no caso, localhost na porta 12345)
    client_socket.connect(('localhost', 12345))
    # Define o diretório onde os arquivos serão salvos no cliente
    tcp_client_dir = os.path.join(os.getcwd(), r"C:\Users\vitor\Desktop\Arquivos\Redes de Computadores 1\TCPClienteServer\TCPClient")

    # Garante que o diretório existe
    if not os.path.exists(tcp_client_dir):
        os.makedirs(tcp_client_dir)

    # Loop principal do cliente
    while True:
        print("Digite uma requisição (Sair, Arquivo <NOME.EXT>, Chat):")
        input_data = input()

        # Verifica se não foi inserida nenhuma entrada
        if not input_data:
            continue

        # Envia os dados de entrada para o servidor
        client_socket.sendall(input_data.encode())

        # Verifica se a entrada indica o encerramento da conexão
        if input_data.startswith("Sair"):
            print("Encerrando conexão...")
            break
        
        # Verifica se a entrada indica solicitação de arquivo
        elif input_data.startswith("Arquivo"):
            # Recebe a resposta do servidor
            response = client_socket.recv(1024)
            # Imprime a resposta do servidor
            print("Resposta do servidor:", response.decode().strip())

            # Verifica se a resposta indica que o arquivo não foi encontrado
            if response.startswith(b"NOK"):
                print(response.strip().decode())
            
            # Verifica se a resposta indica que o arquivo foi encontrado
            elif response.startswith(b"OK"):
                # Divide a resposta para obter informações sobre o arquivo
                parts = response.split()
                if len(parts) == 4:
                    # Extrai informações do nome do arquivo, tamanho e hash
                    filename = parts[1].decode()
                    file_size = int(parts[2].decode())
                    expected_hash = parts[3].decode().strip()

                    # Define o caminho completo do arquivo
                    file_path = os.path.join(tcp_client_dir, filename)
                    # Abre o arquivo para escrita binária
                    with open(file_path, "wb") as file:
                        remaining_bytes = file_size
                        # Recebe os dados do arquivo em pedaços e escreve no arquivo local
                        while remaining_bytes > 0:
                            chunk_data = client_socket.recv(min(1024, remaining_bytes))
                            file.write(chunk_data)
                            remaining_bytes -= len(chunk_data)

                    # Abre o arquivo recém-gravado para leitura binária
                    with open(file_path, "rb") as file:
                        # Lê os dados do arquivo
                        file_data = file.read()
                        # Calcula o hash MD5 dos dados do arquivo
                        file_hash = hashlib.md5(file_data).hexdigest()

                        # Verifica se o hash do arquivo recebido corresponde ao esperado
                        if file_hash == expected_hash:
                            print("Arquivo recebido com sucesso e verificado.")
                        else:
                            print("Erro na verificação de integridade do arquivo.")
        
        # Verifica se a entrada indica iniciar um chat
        elif input_data.startswith("Chat"):
            print("Chat iniciado. Digite 'Sair' para encerrar.")
            while True:
                # Solicita uma mensagem do usuário do cliente
                chat_input = input("Você: ")
                # Envia a mensagem do cliente para o servidor
                client_socket.sendall(chat_input.encode())

                # Verifica se o cliente deseja encerrar o chat
                if chat_input.strip() == "Sair":
                    print("Encerrando chat...")
                    break

                # Recebe a resposta do servidor (mensagem do outro lado do chat)
                chat_response = client_socket.recv(1024)
                # Verifica se não há mais mensagens
                if not chat_response:
                    print("Conexão encerrada pelo servidor.")
                    break

                # Imprime a mensagem recebida do servidor
                print("Servidor:", chat_response.decode().strip())

    # Fecha o socket do cliente
    client_socket.close()

if __name__ == "__main__":
    main()
