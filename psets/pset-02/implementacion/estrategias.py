
from datetime import datetime

from configuracion import ConfiguracionReservaU


class ReglaPrioridad:
    """Interfaz para las reglas de prioridad."""

    def tiene_prioridad(self, disponibilidad, ahora=None):
        raise NotImplementedError(
            "La estrategia debe implementar tiene_prioridad()."
        )


class PrioridadAntesDeLas6(ReglaPrioridad):
    """Da prioridad a capitanes antes de la hora límite configurada."""

    def tiene_prioridad(self, disponibilidad, ahora=None):
        configuracion = ConfiguracionReservaU()
        hora_limite = configuracion.hora_limite_prioridad

        fecha_hora = getattr(
            disponibilidad, "fecha_hora_inicio", None
        )

        if fecha_hora is None:
            fecha_hora = getattr(disponibilidad, "fecha_hora", None)

        if fecha_hora is None:
            hora = getattr(disponibilidad, "hora_inicio", None)
            if hora is None:
                return False
            return hora.hour < hora_limite

        return fecha_hora.hour < hora_limite


class SinPrioridad(ReglaPrioridad):
    """No concede prioridad especial."""

    def tiene_prioridad(self, disponibilidad, ahora=None):
        return False


class PoliticaCancelacion:
    """Interfaz para las políticas de cancelación."""

    def cancelar(self, reserva, horas_restantes):
        raise NotImplementedError(
            "La estrategia debe implementar cancelar()."
        )


class CancelacionEstudiante(PoliticaCancelacion):
    """Un estudiante genera un no-show si cancela con menos de 2 horas."""

    def cancelar(self, reserva, horas_restantes):
        configuracion = ConfiguracionReservaU()

        if horas_restantes < configuracion.horas_cancelacion_estudiante:
            reserva.registrar_no_show()
            reserva.estado = "NO_SHOW"
            print("Cancelación tardía: se registra un no-show.")
            return "NO_SHOW"

        reserva.estado = "CANCELADA"
        print("Reserva cancelada a tiempo, sin penalidad.")
        return "CANCELADA"




class CancelacionCapitan(PoliticaCancelacion):
    """Un capitán genera un no-show si cancela con menos de 24 horas."""

    def cancelar(self, reserva, horas_restantes):
        configuracion = ConfiguracionReservaU()

        if horas_restantes < configuracion.horas_cancelacion_capitan:
            reserva.registrar_no_show()
            reserva.estado = "NO_SHOW"
            print("Cancelación tardía del capitán: se registra un no-show.")
            return "NO_SHOW"

        reserva.estado = "CANCELADA"
        print("Reserva del equipo cancelada a tiempo.")
        return "CANCELADA"


class AnulacionAdministrativa(PoliticaCancelacion):
    """El administrador anula sin penalizar al solicitante."""

    def cancelar(self, reserva, horas_restantes=None):
        reserva.estado = "ANULADA"
        print("Reserva anulada por administración, sin penalidad.")
        return "ANULADA"