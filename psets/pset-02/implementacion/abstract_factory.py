
from datetime import time


class ValidadorHorario:
    def validar(self, disponibilidad):
        raise NotImplementedError



class ValidadorCampusNorte(ValidadorHorario):
    def validar(self, disponibilidad):
        hora = disponibilidad.fecha_hora_inicio.time()
        return time(6, 0) <= hora < time(22, 0)


class ValidadorCampusSur(ValidadorHorario):
    def validar(self, disponibilidad):
        hora = disponibilidad.fecha_hora_inicio.time()
        return time(7, 0) <= hora < time(23, 0)


class Notificador:
    def notificar(self, destinatario, mensaje):
        raise NotImplementedError


class NotificadorCorreo(Notificador):
    def notificar(self, destinatario, mensaje):
        print(
            f"[CORREO INSTITUCIONAL] Para: {destinatario} | {mensaje}"
        )


class NotificadorSMS(Notificador):
    def notificar(self, destinatario, mensaje):
        print(f"[SMS] Para: {destinatario} | {mensaje}")


class FabricaSede:
    def crear_validador(self):
        raise NotImplementedError

    def crear_notificador(self):
        raise NotImplementedError


class FabricaCampusNorte(FabricaSede):
    def crear_validador(self):
        return ValidadorCampusNorte()

    def crear_notificador(self):
        return NotificadorCorreo()


class FabricaCampusSur(FabricaSede):
    def crear_validador(self):
        return ValidadorCampusSur()

    def crear_notificador(self):
        return NotificadorSMS()