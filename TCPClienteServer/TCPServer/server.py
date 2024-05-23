import socket  # Importa o módulo de socket para comunicação de rede
import threading  # Importa o módulo threading para permitir operações concorrentes
import os  # Importa o módulo os para manipulação de caminhos de arquivo
import hashlib  # Importa o módulo hashlib para cálculo de hash

def handle_client(client_socket):
    print("Cliente conectado.")
    while True:
        # Recebe dados do cliente
        data = client_socket.recv(1024)
        # Verifica se não há mais dados
        if not data:
            break
        
        # Decodifica os dados recebidos e remove espaços em branco
        request = data.decode().strip()
        
        # Verifica se o cliente solicitou encerrar a conexão
        if request.startswith("Sair"):
            print("Cliente desconectado.")
            break
        
        # Verifica se o cliente solicitou um arquivo
        elif request.startswith("Arquivo"):
            print("Estou Aqui! 1")
            # Divide a requisição para obter o nome do arquivo
            parts = request.split(' ')
            # Verifica se a requisição tem o formato esperado
            if len(parts) == 2:
                # Extrai o nome do arquivo
                filename = parts[1].strip()
                # Monta o caminho completo do arquivo
                file_path = os.path.join(r"C:\Users\vitor\Desktop\Arquivos\Redes de Computadores 1\TCPClienteServer\TCPServer", filename)
                try:
                    # Tenta abrir o arquivo solicitado em modo de leitura binária
                    with open(file_path, "rb") as file:
                        print("Estou Aqui! 2")
                        # Lê os dados do arquivo
                        file_data = file.read()
                        # Obtém o tamanho do arquivo
                        file_size = len(file_data)
                        # Calcula o hash MD5 dos dados do arquivo
                        file_hash = hashlib.md5(file_data).hexdigest()
                        
                        # Cria uma resposta com informações sobre o arquivo
                        response = f"OK {filename} {file_size} {file_hash}\n"
                        # Envia a resposta para o cliente
                        client_socket.sendall(response.encode())
                        # Envia os dados do arquivo para o cliente
                        client_socket.sendall(file_data)
                        print("Estou Aqui! 3")
                except FileNotFoundError:
                    print("Estou Aqui! 4")
                    # Envia uma resposta informando que o arquivo não foi encontrado
                    client_socket.sendall(b"NOK Arquivo inexistente\n")
        
        # Verifica se o cliente iniciou um chat
        elif request.startswith("Chat"):
            print("Chat iniciado. Digite 'Sair' para encerrar.")
            while True:
                # Recebe a mensagem do cliente
                chat_response = client_socket.recv(1024)
                # Verifica se não há mais mensagens
                if not chat_response:
                    print("Conexão encerrada pelo cliente.")
                    break

                # Exibe a mensagem do cliente no console do servidor
                print("Cliente:", chat_response.decode().strip())

                # Solicita uma mensagem do usuário do servidor
                chat_input = input("Você: ")
                # Envia a mensagem do servidor para o cliente
                client_socket.sendall(chat_input.encode())
                
                # Verifica se o servidor quer encerrar o chat
                if chat_input.strip() == "Sair":
                    print("Encerrando chat...")
                    break

    # Fecha o socket do cliente
    client_socket.close()

def main():
    # Cria um socket do servidor
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Liga o servidor a todas as interfaces na porta 12345
    server.bind(('0.0.0.0', 12345))
    # Começa a ouvir por conexões, com backlog de até 5 conexões pendentes
    server.listen(5)
    print("Servidor ouvindo na porta 12345")
    
    # Loop principal do servidor
    while True:
        # Aceita uma conexão do cliente e retorna um novo socket e o endereço do cliente
        client_socket, addr = server.accept()
        # Cria uma nova thread para lidar com o cliente
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        # Inicia a thread
        client_handler.start()

if __name__ == "__main__":
    main()
