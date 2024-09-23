import random
import time

# Clase para las cartas
class Carta:
    def __init__(self, rango, valor):
        self.rango = rango
        self.valor = valor

# Clase para la baraja
class Baraja:
    def __init__(self):
        rangos = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        valores = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
        self.cartas = [Carta(rango, valores[rango]) for rango in rangos]
    
    def sacar_carta(self):
        return random.choice(self.cartas)

# Clase para un jugador (puede ser el usuario o la casa)
class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []
        self.total = 0
    
    def agregar_carta(self, carta):
        self.mano.append(carta)
        self.total += carta.valor
        # Si obtiene un As, pregunta si quiere que valga 1 o 11
        if carta.rango == 'A' and self.nombre == 'Jugador':
            valor_as = int(input("Obtuviste un As, ¿quieres que valga 1 o 11? "))
            self.total += valor_as - carta.valor
    
    def mostrar_mano(self):
        cartas = ", ".join([carta.rango for carta in self.mano])
        print(f"{self.nombre} tiene: {cartas} (Total: {self.total})")
    
    def quiere_otra_carta(self):
        decision = input("¿Quieres otra carta? (s/n): ").lower()
        return decision == 's'

# Clase para el dealer
class Dealer(Jugador):
    def __init__(self):
        super().__init__('Dealer')
    
    def jugar(self, baraja):
        while self.total < 17:
            carta = baraja.sacar_carta()
            print("El dealer toma otra carta...")
            time.sleep(1)
            self.agregar_carta(carta)
            self.mostrar_mano()
            time.sleep(1)

# Clase para el juego
class Blackjack:
    def __init__(self):
        self.baraja = Baraja()
        self.jugador = Jugador('Jugador')
        self.dealer = Dealer()
        self.balance = 500
    
    def jugar_ronda(self):
        print(f"Tu saldo actual es: {self.balance}")
        apuesta = int(input("¿Cuánto quieres apostar? "))

        if self.balance >= apuesta > 0:
            self.balance -= apuesta
        else:
            print("Apuesta no válida.")
            return

        # Repartir cartas iniciales
        for _ in range(2):
            self.jugador.agregar_carta(self.baraja.sacar_carta())
            self.dealer.agregar_carta(self.baraja.sacar_carta())

        self.jugador.mostrar_mano()
        self.dealer.mostrar_mano()

        # Turno del jugador
        while self.jugador.total < 21 and self.jugador.quiere_otra_carta():
            carta = self.baraja.sacar_carta()
            self.jugador.agregar_carta(carta)
            self.jugador.mostrar_mano()
        
        # Si el jugador se pasa de 21, pierde automáticamente
        if self.jugador.total > 21:
            print("Te pasaste de 21, pierdes.")
            return
        
        # Turno del dealer
        self.dealer.jugar(self.baraja)

        # Comparar resultados
        self.comparar_resultados(apuesta)

    def comparar_resultados(self, apuesta):
        if self.jugador.total > 21:
            print("Te pasaste de 21, pierdes.")
        elif self.dealer.total > 21:
            print(f"La casa se pasó de 21. ¡Ganaste {apuesta * 2}!")
            self.balance += apuesta * 2
        elif self.jugador.total > self.dealer.total:
            print(f"¡Ganaste {apuesta * 2}!")
            self.balance += apuesta * 2
        elif self.jugador.total < self.dealer.total:
            print("Perdiste.")
        else:
            print("Empate. Recuperas tu apuesta.")
            self.balance += apuesta
    
    def jugar(self):
        while True:
            self.jugar_ronda()
            seguir = input("¿Quieres seguir jugando? (s/n): ").lower()
            if seguir == 'n':
                print(f"Te retiras con un saldo de {self.balance}.")
                break

# Iniciar el juego
juego = Blackjack()
juego.jugar()

