class ComportamientoGraznar:
    def graznar(self):
        raise NotImplementedError


class GraznidoNormal(ComportamientoGraznar):
    def graznar(self):
        print("CUACK CUACK.")


class GraznidoDeGoma(ComportamientoGraznar):
    def graznar(self):
        print("Chirrido de goma.")


class ComportamientoVuelo:
    def volar(self):
        raise NotImplementedError


class VuelaConAlas(ComportamientoVuelo):
    def volar(self):
        return "Volando con alas"


class NoVuela(ComportamientoVuelo):
    def volar(self):
        return "No vuela"


class Pato:

    def __init__(self, comportamiento_vuelo, comportamiento_graznar):
        self.comportamiento_vuelo = comportamiento_vuelo
        self.comportamiento_graznar = comportamiento_graznar

    def nadar(self):
        print("Nadando.")

    def graznar(self):
        self.comportamiento_graznar.graznar()

    def volar(self):
        print(self.comportamiento_vuelo.volar())


class PatoSalvaje(Pato):
    def __init__(self):
        vuela_alas = VuelaConAlas()
        graznido_normal = GraznidoNormal()
        super().__init__(vuela_alas, graznido_normal)


class PatoDeGoma(Pato):
    def __init__(self):
        no_vuela = NoVuela()
        graznido_de_goma = GraznidoDeGoma()
        super().__init__(no_vuela, graznido_de_goma)


if __name__ == "__main__":
    salvaje = PatoSalvaje()
    salvaje.nadar()
    salvaje.graznar()
    salvaje.volar()

    print()

    goma = PatoDeGoma()
    goma.nadar()
    goma.graznar()
    goma.volar()