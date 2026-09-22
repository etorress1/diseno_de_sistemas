class Estudiante:
    def __init__(self, nombre):
        self.nombre = nombre


class EquipoOficial:
    def __init__(self, nombre):
        self.nombre = nombre


class ReservaRegular:
    def __init__(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        self.cancha = cancha
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.solicitante = solicitante

    def confirmar(self):
        return "Reserva regular confirmada para " + self.solicitante.nombre


class ReservaPrioritaria:
    def __init__(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        self.cancha = cancha
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.solicitante = solicitante

    def confirmar(self):
        return "Reserva con prioridad confirmada para " + self.solicitante.nombre


class CreadorDeReserva:
    def crear_reserva(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        raise NotImplementedError


class CreadorDeReservaRegular(CreadorDeReserva):
    def crear_reserva(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        return ReservaRegular(
            cancha,
            fecha,
            hora_inicio,
            hora_fin,
            solicitante
        )


class CreadorDeReservaPrioritaria(CreadorDeReserva):
    def crear_reserva(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        return ReservaPrioritaria(
            cancha,
            fecha,
            hora_inicio,
            hora_fin,
            solicitante
        )


class FabricaDeReservas:

    @staticmethod
    def elegir_creador(solicitante):

        if isinstance(solicitante, Estudiante):
            return CreadorDeReservaRegular()

        if isinstance(solicitante, EquipoOficial):
            return CreadorDeReservaPrioritaria()

        raise RuntimeError("Tipo de solicitante no válido")


def reserva_desde_web(cancha, fecha, hora_inicio, hora_fin, solicitante):

    creador = FabricaDeReservas.elegir_creador(solicitante)

    reserva = creador.crear_reserva(
        cancha,
        fecha,
        hora_inicio,
        hora_fin,
        solicitante
    )

    return reserva


def main():

    reserva1 = reserva_desde_web(
        "Cancha de futbol",
        "2026-09-17",
        "18:00",
        "20:00",
        Estudiante("Erick")
    )

    print(reserva1.confirmar())

    reserva2 = reserva_desde_web(
        "Cancha de futbol",
        "2026-09-17",
        "18:00",
        "20:00",
        EquipoOficial("Aguilas")
    )

   
    print(reserva2.confirmar())


if __name__ == "__main__":
    main()