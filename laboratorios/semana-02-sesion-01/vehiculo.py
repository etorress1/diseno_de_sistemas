class ComportamientoMover:
    def mover(self):
        raise NotImplementedError


class MuevePorCarretera(ComportamientoMover):
    def mover(self):
        print("Conduciendo por carretera")


class MuevePorMar(ComportamientoMover):
    def mover(self):
        print("Navegando por agua")


class MuevePorCielo(ComportamientoMover):
    def mover(self):
        print("Volando por aire")


class Vehiculo:

    def __init__(self, comportamiento_mover):
        self.comportamiento_mover = comportamiento_mover

    def mover(self):
        self.comportamiento_mover.mover()


class Auto(Vehiculo):
    def __init__(self):
        mueve_carretera = MuevePorCarretera()
        super().__init__(mueve_carretera)


class Bote(Vehiculo):
    def __init__(self):
        mueve_mar = MuevePorMar()
        super().__init__(mueve_mar)


class Avion(Vehiculo):
    def __init__(self):
        mueve_cielo = MuevePorCielo()
        super().__init__(mueve_cielo)


if __name__ == "__main__":

    auto = Auto()
    auto.mover()

    bote = Bote()
    bote.mover()

    avion = Avion()
    avion.mover()