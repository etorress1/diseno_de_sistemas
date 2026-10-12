
from dominio import Reserva
from estrategias import (
    CancelacionEstudiante,
    CancelacionCapitan,
    SinPrioridad,
    PrioridadAntesDeLas6,
)


class CreadorReserva:
    """Creador base de reservas."""

    def crear_reserva(
        self, identificador, solicitante, cancha, disponibilidad, politica
    ):
        raise NotImplementedError


class CreadorReservaEstudiante(CreadorReserva):
    """Crea reservas regulares de estudiantes."""

    def crear_reserva(
        self, identificador, solicitante, cancha, disponibilidad, politica
    ):
        reserva = Reserva(
            identificador,
            solicitante,
            cancha,
            disponibilidad,
            politica,
        )
        reserva.estrategia_cancelacion = CancelacionEstudiante()
        reserva.regla_prioridad = SinPrioridad()
        return reserva


class CreadorReservaCapitan(CreadorReserva):
    """Crea reservas oficiales de equipos."""

    def crear_reserva(
        self, identificador, solicitante, cancha, disponibilidad, politica
    ):
        reserva = Reserva(
            identificador,
            solicitante,
            cancha,
            disponibilidad,
            politica,
        )
        reserva.estrategia_cancelacion = CancelacionCapitan()
        reserva.regla_prioridad = PrioridadAntesDeLas6()
        return reserva