
# VIDEOJUEGO TURNOS LABORATORIO SEMANA 7
#-----------------------------------------------

#CLASE PERSONAJE

class Personaje:
    def __init__(self, nombre, vida, ataque):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque
        self.estrategia = None

    def atacar(self, objetivo):
        if self.estrategia is None:
            print("No hay una estrategia seleccionada.")
            return

        self.estrategia.atacar(self, objetivo)

    def recibir_danio(self, danio):
        self.vida -= danio

        if self.vida < 0:
            self.vida = 0

    def esta_vivo(self):
        return self.vida > 0

    def mostrar_estado(self):
        print(
            f"{self.nombre} | "
            f"Vida: {self.vida} | "
            f"Ataque: {self.ataque}"
        )


# PERSONAJES HERENCIA


class Guerrero(Personaje):
    def __init__(self):
        super().__init__("Guerrero", 100, 20)


class Dragon(Personaje):
    def __init__(self):
        super().__init__("Dragon", 120, 25)


class Soldado(Personaje):
    def __init__(self):
        super().__init__("Soldado", 100, 22)


class Alien(Personaje):
    def __init__(self):
        super().__init__("Alien", 110, 24)

 
# FACTORY PERSONAJES

class PersonajeFactory:

    @staticmethod
    def crear(tipo):
        tipo = tipo.lower()

        if tipo == "guerrero":
            return Guerrero()

        elif tipo == "dragon":
            return Dragon()

        elif tipo == "soldado":
            return Soldado()

        elif tipo == "alien":
            return Alien()

        else:
            raise ValueError("Tipo de personaje no válido.")


# ABSTRACT FACTORY PARA LOS MUNDOS
class FabricaMundo:

    def crear_jugador(self):
        raise NotImplementedError

    def crear_enemigo(self):
        raise NotImplementedError


class FantasyFactory(FabricaMundo):

    def crear_jugador(self):
        return PersonajeFactory.crear("guerrero")

    def crear_enemigo(self):
        return PersonajeFactory.crear("dragon")


class SciFiFactory(FabricaMundo):

    def crear_jugador(self):
        return PersonajeFactory.crear("soldado")

    def crear_enemigo(self):
        return PersonajeFactory.crear("alien")



# STRATEGY PARA ATAQUES


class EstrategiaAtaque:

    def atacar(self, atacante, objetivo):
        raise NotImplementedError


class AtaqueNormal(EstrategiaAtaque):

    def atacar(self, atacante, objetivo):
        danio = atacante.ataque

        print(
            f"{atacante.nombre} realiza un ataque normal "
            f"y causa {danio} de daño."
        )

        objetivo.recibir_danio(danio)


class AtaqueFuerte(EstrategiaAtaque):

    def atacar(self, atacante, objetivo):
        danio = atacante.ataque * 2

        print(
            f"{atacante.nombre} realiza un ataque fuerte "
            f"y causa {danio} de daño."
        )

        objetivo.recibir_danio(danio)


# SINGLETON

class GameConfig:
    _objeto = None

    def __init__(self):
        self.dificultad = "Normal"
        self.numero_maximo_turnos = 20

    @staticmethod
    def obtener_objeto():
        if GameConfig._objeto is None:
            GameConfig._objeto = GameConfig()

        return GameConfig._objeto


# FACHADA

class GameFacade:

    def __init__(self):
        self.config = GameConfig()

        self.mundo = None
        self.jugador = None
        self.enemigo = None

    # CREAR MUNDO

    def crear_mundo(self, opcion):

        if opcion == "1":
            self.mundo = FantasyFactory()

        elif opcion == "2":
            self.mundo = SciFiFactory()

        else:
            raise ValueError("Mundo no válido.")

        self.jugador = self.mundo.crear_jugador()
        self.enemigo = self.mundo.crear_enemigo()

    # SELECCIONAR ESTRATEGIA

    def seleccionar_estrategia(self):

        print("\nSeleccione estrategia de ataque:")
        print("1. Ataque normal")
        print("2. Ataque fuerte")

        opcion = input("Opción: ")

        if opcion == "1":
            self.jugador.estrategia = AtaqueNormal()

        elif opcion == "2":
            self.jugador.estrategia = AtaqueFuerte()

        else:
            print("Opción no válida.")
            self.seleccionar_estrategia()

    # MOSTRAR ESTADO

    def mostrar_estado(self):
        print("\n-----------------------------")
        print("ESTADO DEL COMBATE")
        print("-----------------------------")

        print("Jugador:")
        self.jugador.mostrar_estado()

        print("\nEnemigo:")
        self.enemigo.mostrar_estado()

        print("-----------------------------")

    # EJECUTAR TURNO

    def ejecutar_turno(self, numero_turno):

        print(f"\n========== TURNO {numero_turno} ==========")

        self.seleccionar_estrategia()

        # Ataque del jugador
        self.jugador.atacar(self.enemigo)

        # Comprobar si el enemigo fue derrotado
        if not self.enemigo.esta_vivo():
            print(f"\n{self.enemigo.nombre} ha sido derrotado.")
            return False

        # Respuesta del enemigo
        print(f"\n{self.enemigo.nombre} contraataca.")

        danio_enemigo = self.enemigo.ataque

        print(
            f"{self.enemigo.nombre} causa "
            f"{danio_enemigo} de daño."
        )

        self.jugador.recibir_danio(danio_enemigo)

        # Comprobar si el jugador fue derrotado
        if not self.jugador.esta_vivo():
            print(f"\n{self.jugador.nombre} ha sido derrotado.")
            return False

        self.mostrar_estado()

        return True
    
    # DETERMINAR GANADOR

    def determinar_ganador(self):

        print("\n=============================")
        print("         RESULTADO")
        print("=============================")

        if self.jugador.esta_vivo() and not self.enemigo.esta_vivo():
            print(f"¡Ganador: {self.jugador.nombre}!")

        elif self.enemigo.esta_vivo() and not self.jugador.esta_vivo():
            print(f"Ganador: {self.enemigo.nombre}")

        else:
            print("La partida terminó sin ganador.")

    # INICIAR JUEGO

    def iniciar(self):

        print("=============================")
        print("   JUEGUITO POR TURNOS :)")
        print("=============================")

        print("\nSeleccione un mundo:")
        print("1. Fantasía")
        print("2. Ciencia ficción")

        opcion = input("Opción: ")

        while opcion not in ["1", "2"]:
            print("Opción no válida.")
            opcion = input("Seleccione 1 o 2: ")

        # Crear mundo y personajes
        self.crear_mundo(opcion)

        print("\nMundo creado correctamente.")

        print("\nJugador:")
        self.jugador.mostrar_estado()

        print("\nEnemigo:")
        self.enemigo.mostrar_estado()

        # Ejecutar combate
        turno = 1

        while (
            self.jugador.esta_vivo()
            and self.enemigo.esta_vivo()
            and turno <= self.config.numero_maximo_turnos
        ):

            continuar = self.ejecutar_turno(turno)

            if not continuar:
                break

            turno += 1

        # Si se alcanzó el límite
        if (
            self.jugador.esta_vivo()
            and self.enemigo.esta_vivo()
            and turno > self.config.numero_maximo_turnos
        ):
            print("\nSe alcanzó el número máximo de turnos.")

        self.determinar_ganador()


#----------------------------MAIN----------------------------

def main():
    if __name__ == "__main__":
        juego = GameFacade()
        juego.iniciar()

main()
