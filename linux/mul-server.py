import socket
import random
import sys
from _thread import *

sys.stdout = open('out.log','wt')

host = '0.0.0.0'
port = 1233
ThreadCount = 0


IMAGES = ['''

    +---++
    |   ||
        ||
        ||
        ||
        ||
        ///////////''', '''

    +---++
    |   ||
    O   ||
        ||
        ||
        ||
        ///////////''', '''

    +---++
    |   ||
    O   ||
    |   ||
        ||
        ||
        ///////////''', '''

    +---++
    |   ||
    O   ||
   /|   ||
        ||
        ||
        ///////////''', '''

    +---++
    |   ||
    O   ||
   /|\  ||
        ||
        ||
        ///////////''', '''

    +---++
    |   ||
    O   ||
   /|\  ||
    |   ||
        ||
        ///////////''', '''

    +---++
    |   ||
    O   ||
   /|\  ||
    |   ||
   /    ||
        ///////////''', '''

    +---++
    |   ||
    O   ||
   /|\  ||
    |   ||
   / \  ||
        ///////////''', '''
''']

WORDS = [
    'lavadora',
    'secadora',
    'sofa',
    'gobierno',
    'diputado',
    'democracia',
    'computadora',
    'teclado',
    'pesadilla',
    'telematica',
    'umsa',
    'informatica',
    'bolivia'
]

def random_word():
    idx = random.randint(0, len(WORDS) - 1)
    return WORDS[idx]

def client_handler(connection):
    connection.sendall(str.encode('Bienvenido al SERVIDOR AHORCADO de 273...\n\nIngresa tu nombre:'))
    data = connection.recv(2048)
    nombre = data.decode('utf-8')

    print('Ha iniciado un juego:', nombre)

    connection.sendall(str.encode('Listo para empezar? S/N:'))
    data = connection.recv(2048)
    resp = data.decode('utf-8')
    if resp.upper() != 'S': connection.close()

    word = random_word()
    hidden_word = [" _ "] * len(word)
    tries = 0
    sents = []

    #img = IMAGES[0] + "\n" + ' '.join(hidden_word).upper() + "\n" + ' '.join(sents).upper() + '\n------------------------------------------'
    img = display_board_str(sents, hidden_word, tries)
    reply = img + '\nIngresa una letra:'
    connection.sendall(str.encode(reply))

    while True:
        data = connection.recv(2048)
        message = data.decode('utf-8')
        if message.upper() == 'BYE': break

        current_letter = str(message)
        if len(current_letter) == 1:
            sents.append(' ' + current_letter + ' ')

            letter_indexes = []
            for idx in range(len(word)):
                if word[idx] == current_letter:
                    letter_indexes.append(idx)

            if len(letter_indexes) == 0:
                tries += 1

                if tries == 7:
                    print('msg: PERDIO', nombre)
                    img = display_board_str(sents, hidden_word, tries)
                    img = img + '\nPerdiste! La palabra correcta era {}'.format(word.upper())
                    #reply = '{img}'
                    connection.sendall(str.encode(img))
                    break

            else:
                for idx in letter_indexes:
                    hidden_word[idx] = ' ' + current_letter + ' '

                letter_indexes = []
            try:
                hidden_word.index(' _ ')
            except ValueError:
                print('msg: GANO', nombre)
                img = display_board_str(sents, hidden_word, tries)
                img = img + '\nFelicidades! Ganaste. La palabra es: {}'.format(word.upper())
                #reply = '{img}'
                connection.sendall(str.encode(img))
                break

            img = display_board_str(sents, hidden_word, tries)
            img = img + '\nIngresa una letra:'

            #reply = '{img}'
            connection.sendall(str.encode(img))
        else:
            connection.sendall(str.encode('Ingresa solo una letra:'))

    connection.close()


def accept_connections(ServerSocket):
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))

    start_new_thread(client_handler, (Client,))


def start_server(host, port):
    ServerSocket = socket.socket()
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))
    print('Servidor esta escuchando en el puerto: {port}...')
    ServerSocket.listen()

    while True:
        accept_connections(ServerSocket)


def display_board(sents, hidden_word, tries):
    print(IMAGES[tries])
    print('')
    print(' '.join(hidden_word).upper())
    print('')
    print(' '.join(sents).upper())
    print('------------------------------------------')

def display_board_str(sents, hidden_word, tries):
    str = IMAGES[tries]
    str = str + '\n'
    str = str + ' '.join(hidden_word).upper()
    str = str + '\n\n'
    str = str + ' '.join(sents).upper()
    str = str + '\n------------------------------------------'
    return str

def run():
    word = random_word()
    hidden_word = [" _ "] * len(word)
    tries = 0
    sents = []

    while True:
        display_board(sents, hidden_word, tries)
        current_letter = str(input('Escoge una letra: '))
        sents.append(' ' + current_letter + ' ')

        letter_indexes = []
        for idx in range(len(word)):
            if word[idx] == current_letter:
                letter_indexes.append(idx)

        if len(letter_indexes) == 0:
            tries += 1

            if tries == 7:
                display_board(sents, hidden_word, tries)
                print('')
                print('¡Perdiste! La palabra correcta era {}'.format(word))
                break
        else:
            for idx in letter_indexes:
                hidden_word[idx] = ' ' + current_letter + ' '

            letter_indexes = []

        try:
            hidden_word.index(' _ ')
        except ValueError:
            print('')
            print('¡Felicidades! Ganaste. La palabra es: {}'.format(word.upper()))
            break

start_server(host, port)
