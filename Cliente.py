"""
Programa hecho por "Aaron Osbiel Garza Sedeño"
Practica 1, aplicaciones para comunicaciones de red
Profesora Tanibet Perez de los Santos Mondragon

20/03/2023
aplicacion Cliente
"""

import socket # Para conexion de los mismos
import pickle # Usado en esta practica para enviar/recibir los datos de cliente y servidor

#Importa el juego
from Gato import GatoDummy
#Se piden los datos del cliente
HOST = input("Introduce la direccion Ip del servidor: ")  #Se debe introducir la direccion Ip del server
PORT = int(input("Introduce el puerto del servidor: "))       # the port we're connecting to

#Se conecta con el servidor
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print(f"\nSe ha conectado con: {s.getsockname()}!")

#Inicia el juego como el jugador "O"
player_o = GatoDummy("O")

#Variable booleana para permitir que el juego se pueda repetir
rematch = True

while rematch == True:
    #Empieza el juego y el codigo
    print(f"\n\n Gato ")

    #Dibuja el cuadro vacio pero sin poder hacer nada
    player_o.draw_grid()

    #Como el servidor va primero el cliente tiene que esperar la respuesta y por tanto recibir el primer tablero
    print(f"\nEsperando al otro jugador...")
    x_symbol_list = s.recv(1024)
    x_symbol_list = pickle.loads(x_symbol_list) #Se usa pickle para transformar y para recibir los datos del jugador "X" (servidor)
    player_o.update_symbol_list(x_symbol_list) #Se actualizan los datos

    #Estara en bucle el ciclo hasta que alguno de los jugadores gane o empaten
    while player_o.did_win("O") == False and player_o.did_win("X") == False and player_o.is_draw() == False:
        #Dibuja el cuadro y pregunta las coordenadas al jugador
        print(f"\n       Tu turno!")
        print(f"Ejemplo: A1, B2, C3, advertencia no pongas una casilla ocupada o perderas turno")
        player_o.draw_grid()
        player_coord = input(f"Introduce tus coordenadas:  ")
        player_o.edit_square(player_coord)

        #Dibuja el cuadro actualizado de nuevo
        player_o.draw_grid()

        #Convierte los datos con pickle para transformar y se envia al servidor
        o_symbol_list = pickle.dumps(player_o.symbol_list)
        s.send(o_symbol_list)

        # Si el cliente ganó con el último movimiento o es un empate, terminara el ciclo del ciclo
        if player_o.did_win("O") == True or player_o.is_draw() == True:
            break

        #Espera a recibir el tablero del servidor para recibirlo por pickle y convertir el cuadro para el servidor
        print(f"\nWaiting for other player...")
        x_symbol_list = s.recv(1024)
        x_symbol_list = pickle.loads(x_symbol_list)
        player_o.update_symbol_list(x_symbol_list)

    #Termina el juego y muestra los mensajes segun que haya ocurrido
    if player_o.did_win("O") == True:
        print(f"Felicidades, ganaste!")
    elif player_o.is_draw() == True:
        print(f"Es un empate!")
    else:
        print(f"Lo siento, el servidor gano :C")

    #Se usa pickle para convertir la respuesta y enviarla al servidor
    print(f"\nEsperando al otro jugador...")
    host_response = s.recv(1024)
    host_response = pickle.loads(host_response)
    client_response = "N"

    #Si el servidor quiere una revancha el cliente espera y envia su respuesta
    if host_response == "Y":
        print(f"\nEl servidor le gustaria una revancha!")
        client_response = input("Revancha? (Y/N): ")
        client_response = client_response.capitalize()
        temp_client_resp = client_response

        #informar al anfitrión lo que decidió el cliente
        client_response = pickle.dumps(client_response) #Se usa pickle para transformar y enviar el mensaje
        s.send(client_response)

        #En caso de que el cliente quiera una revancha se abre el siguiente if
        if temp_client_resp == "Y":
            player_o.restart()

        #En caso de que el cliente no quiera una revancha, y se termina el ciclo rematch y el de eleccion
        else:
            rematch = False

    #En caso de que el servidor no quiera una revancha se termina el ciclo
    else:
        print(f"\nEl servidor no quiere una revancha.")
        rematch = False
#Esto se muestra al finalizar el ciclo while de rematch
spacer = input(f"\nGracias por jugar!\nPresiona Enter para terminar...\n")
#Se cierra el socket y la conexion
s.close()