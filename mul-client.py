import socket

host = '192.168.1.1'
port = 1233

ClientSocket = socket.socket()
print('Conectando...')
try:
    ClientSocket.connect((host, port))

    Response = ClientSocket.recv(2048)
    print(Response.decode('utf-8'))

    while True:
        Input = input('Prompt: ')
        if Input:
            ClientSocket.send(str.encode(Input))
            Response = ClientSocket.recv(2048)
            if not Response: break
            print(Response.decode('utf-8'))

except socket.error as e:
    print(str(e))

ClientSocket.close()