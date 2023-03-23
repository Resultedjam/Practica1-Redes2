"""
Programa hecho por "Aaron Osbiel Garza Sedeño"
Practica 1, aplicaciones para comunicaciones de red
Profesora Tanibet Perez de los Santos Mondragon

20/03/2023
aplicacion Gato
"""
class GatoDummy():

    def __init__(self, player_symbol):
        #Inicializa los simbolos
        self.symbol_list = []

        #Define las 9 casillas y las deja en blanco
        for i in range(9):
            self.symbol_list.append(" ") 

        #Se declara el simbolo del jugador
        self.player_symbol = player_symbol


    def restart(self):
        #Limpia el cuadro en cuanto se reinicie el juego
        for i in range(9):
            self.symbol_list[i] = " "


    def draw_grid(self):
        #La parte superior de las columnas para guiar las coordenadas
        print("\n       A   B   C\n")
        
        #Despliega la primera fila
        row_one = "   1   " + self.symbol_list[0]
        row_one += " ║ " + self.symbol_list[1]
        row_one += " ║ " + self.symbol_list[2]
        print(row_one)

        #Despliega el divisor
        print("      ═══╬═══╬═══")

        #Despliega la segunda fila
        row_two = "   2   " + self.symbol_list[3]
        row_two += " ║ " + self.symbol_list[4]
        row_two += " ║ " + self.symbol_list[5]
        print(row_two)

        #Despliega el divisor
        print("      ═══╬═══╬═══")

        # Despliega la tercera y ultima fila
        row_three = "   3   " + self.symbol_list[6]
        row_three += " ║ " + self.symbol_list[7]
        row_three += " ║ " + self.symbol_list[8]
        print(row_three, "\n")


    def edit_square(self, grid_coord):
        #Cambia de posicion las coordenadas en caso de que se hayan escrito como "1A" a "A1" y tener un solo formato
        if grid_coord[0].isdigit():
            grid_coord = grid_coord[1] + grid_coord[0]

        #Divide la coordenada
        col = grid_coord[0].capitalize()
        row = grid_coord[1]

        #Convierte "A1" en 0, "C3" en 8, y así sucesivamente
        grid_index = 0

        if row == "1":
            if col == "A":
                grid_index = 0
            elif col == "B":
                grid_index = 1
            elif col == "C":
                grid_index = 2
        elif row == "2":
            if col == "A":
                grid_index = 3
            elif col == "B":
                grid_index = 4
            elif col == "C":
                grid_index = 5
        elif row == "3":
            if col == "A":
                grid_index = 6
            elif col == "B":
                grid_index = 7
            elif col == "C":
                grid_index = 8

        if self.symbol_list[grid_index] == " ":
            self.symbol_list[grid_index] = self.player_symbol


    def update_symbol_list(self, new_symbol_list):
        for i in range(9):
            self.symbol_list[i] = new_symbol_list[i]


    def did_win(self, player_symbol):
        #variable local hecha para reemplazar la lista de self.symbol
        g = []
        for i in range(9):
            g.append(self.symbol_list[i])

        # de igual manera para reemplazar self.player_symbol
        sym = player_symbol

        #checa la fila superior
        if g[0] == sym and g[1] == sym and g[2] == sym:
            return True

        #checa la fila de enmedio
        elif g[3] == sym and g[4] == sym and g[5] == sym:
            return True
        
        #checa la fila inferior
        elif g[6] == sym and g[7] == sym and g[8] == sym:
            return True 

        #checa la columna izquierda
        elif g[0] == sym and g[3] == sym and g[6] == sym:
            return True 

        #checa la columna de en medio
        elif g[1] == sym and g[4] == sym and g[7] == sym:
            return True 

        #checa la columna derecha
        elif g[2] == sym and g[5] == sym and g[8] == sym:
            return True

        #checa la columna
        elif g[2] == sym and g[4] == sym and g[6] == sym:
            return True 

        #checa de arriba a la izquierda a abajo a la derecha
        elif g[0] == sym and g[4] == sym and g[8] == sym:
            return True 

        #Si no ha ganado nadie todavia
        return False


    def is_draw(self):
        #Checa si todos los espacios están ocupados
        num_blanks = 0
        for i in range(9):
                if self.symbol_list[i] == " ":
                    num_blanks += 1

        #si el jugador no ganó y no quedan espacios, es un empate
        if self.did_win(self.player_symbol) == False and num_blanks == 0:
            return True
        else:
            return False
