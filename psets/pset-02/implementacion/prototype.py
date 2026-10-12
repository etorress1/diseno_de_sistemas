
from copy import deepcopy


class Bloqueo:
    def __init__(
        self,
        motivo,
        fecha,
        hora_inicio,
        hora_fin,
        cancha=None,
        equipo_montaje=None,
    ):
        self.motivo = motivo
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.cancha = cancha
        self.equipo_montaje = list(equipo_montaje or [])

    def clonar(self, cancha, fecha):
        copia = deepcopy(self)
        copia.cancha = cancha
        copia.fecha = fecha
        return copia