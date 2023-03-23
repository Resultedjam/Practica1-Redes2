"""
Programa hecho por "Aaron Osbiel Garza Sedeño"
Practica 1, aplicaciones para comunicaciones de red
Profesora Tanibet Perez de los Santos Mondragon

20/03/2023
aplicacion Servidor

"""


import socket # Para conexion de los mismos
import pickle # Usado en esta practica para enviar/recibir los datos de cliente y servidor

#Agarra el juego hecho en una clase aparte de python
from Gato import GatoDummy

HOST = '192.168.0.10' #Esta sera la direccion IP donde ira el servidor
PORT = 12783       #Puerto para que se conecten los clientes

#Inicia el server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

#Acepta la conexion con el cliente
client_socket, client_address = s.accept()
print(f"\nConectando con: {client_address}!")

#Inicia el juego como el jugador "X"
player_x = GatoDummy("X")

#Variable booleana para permitir que el juego se pueda repetir
rematch = True

while rematch == True:
    #Empieza el juego y el codigo
    print(f"\n\n Gato ")

    #Estara en bucle el ciclo hasta que alguno de los jugadores gane o empaten
    while player_x.did_win("X") == False and player_x.did_win("O") == False and player_x.is_draw() == False:
        #Dibuja el cuadro y pregunta las coordenadas al jugador
        print(f"\n       Tu turno!")
        print(f"Ejemplo: A1, B2, C3, advertencia no pongas una casilla ocupada o perderas turno")
        player_x.draw_grid()
        player_coord = input(f"Introduce las coordenadas: ")
        player_x.edit_square(player_coord)

        #Dibuja el cuadro actualizado de nuevo
        player_x.draw_grid()

        #Se usa pickle para enviar los simbolos colocalos de el jugador X (Servidor) al cuadro del cliente
        x_symbol_list = pickle.dumps(player_x.symbol_list)
        client_socket.send(x_symbol_list)

        # Si el servidor ganó con el último movimiento o es un empate, terminara el ciclo del ciclo
        if player_x.did_win("X") == True or player_x.is_draw() == True:
            break

        #Espera a recibir el tablero del cliente para recibirlo por pickle y convertir el cuadro para el cliente
        print(f"\nEsperando al otro jugador...")
        o_symbol_list = client_socket.recv(1024)
        o_symbol_list = pickle.loads(o_symbol_list)
        player_x.update_symbol_list(o_symbol_list)

    #Termina el juego y muestra los mensajes segun que haya ocurrido
    if player_x.did_win("X") == True:
        print(f"Felicidades, ganaste!")
    elif player_x.is_draw() == True:
        print(f"Es un empate!")
    else:
        print(f"Lo siento, el cliente gano :c")

    #Pregunta por la revancha
    host_response = input(f"\nRevancha? (Y/N): ")
    host_response = host_response.capitalize()
    temp_host_resp = host_response
    client_response = ""

    #Se usa pickle para convertir la respuesta y enviarla al cliente
    host_response = pickle.dumps(host_response)
    client_socket.send(host_response)

    #Si el servidor no quiere una revancha termina el ciclo while rematch
    if temp_host_resp == "N":
        rematch = False

    #Si el servidor quiere una revancha esperamos la respuesta del cliente
    else:
        #Esperamos recibir la respuesta del cliente
        print(f"Esperando una respuesta...")
        client_response = client_socket.recv(1024)
        client_response = pickle.loads(client_response) #se usa pickle para recibir la respuesta del cliente

        #Si la cliente no quiere una revancha y termina el bucle.
        if client_response == "N":
            print(f"\nEl cliente no quiere una revancha.")
            rematch = False

        #si tanto el servidor como el cliente quieren una revancha, se reinicia el juego y volvemos a la linea 27
        else:
            player_x.restart()
#Esto se muestra al finalizar el ciclo while de rematch
spacer = input(f"\nGracias por jugar!\nPresiona Enter para terminar...\n")
#Se cierra el socket y la conexion
client_socket.close()