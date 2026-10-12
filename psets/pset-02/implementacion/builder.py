
class ReservaRecurrente:
    def __init__(
        self,
        cancha,
        fecha_inicio,
        franja,
        solicitante,
        semanas=2,
        equipo_prestado=None,
        notas="",
    ):
        self.cancha = cancha
        self.fecha_inicio = fecha_inicio
        self.franja = franja
        self.solicitante = solicitante
        self.semanas = semanas
        self.equipo_prestado = equipo_prestado or []
        self.notas = notas


class ReservaRecurrenteBuilder:
    def __init__(self):
        self._cancha = None
        self._fecha_inicio = None
        self._franja = None
        self._solicitante = None
        self._semanas = 2
        self._equipo_prestado = []
        self._notas = ""

    def con_cancha(self, cancha):
        self._cancha = cancha
        return self

    def con_fecha_inicio(self, fecha_inicio):
        self._fecha_inicio = fecha_inicio
        return self

    def con_franja(self, franja):
        self._franja = franja
        return self

    def con_solicitante(self, solicitante):
        self._solicitante = solicitante
        return self

    def con_semanas(self, semanas):
        if not 2 <= semanas <= 8:
            raise ValueError("La recurrencia debe tener entre 2 y 8 semanas.")
        self._semanas = semanas
        return self

    def con_equipo_prestado(self, equipo):
        self._equipo_prestado = list(equipo)
        return self

    def con_notas(self, notas):
        self._notas = notas
        return self

    def construir(self):
        if any(
            valor is None
            for valor in (
                self._cancha,
                self._fecha_inicio,
                self._franja,
                self._solicitante,
            )
        ):
            raise ValueError(
                "Faltan datos obligatorios para la reserva recurrente."
            )

        return ReservaRecurrente(
            cancha=self._cancha,
            fecha_inicio=self._fecha_inicio,
            franja=self._franja,
            solicitante=self._solicitante,
            semanas=self._semanas,
            equipo_prestado=self._equipo_prestado,
            notas=self._notas,
        )