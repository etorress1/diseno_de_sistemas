
from threading import Lock


class GestorConcurrencia:
    def __init__(self):
        self._bloqueo = Lock()
        self._reservas_confirmadas = set()

    def reservar_atomicamente(self, clave, operacion_registro):
        """
        clave identifica la cancha y la franja horaria.

        operacion_registro se ejecuta únicamente si la clave
        todavía no tiene una reserva confirmada.
        """
        with self._bloqueo:
            if clave in self._reservas_confirmadas:
                return False

            resultado = operacion_registro()

            if resultado:
                self._reservas_confirmadas.add(clave)

            return bool(resultado)