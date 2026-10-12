class ConfiguracionReservaU:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)

            cls._instancia.hora_limite_prioridad = 18
            cls._instancia.horas_cancelacion_estudiante = 2
            cls._instancia.horas_cancelacion_capitan = 24
            cls._instancia.limite_no_shows = 3
            cls._instancia.dias_suspension = 7

        return cls._instancia

    @classmethod
    def instancia(cls):
        return cls()