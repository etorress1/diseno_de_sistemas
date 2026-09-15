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
        return "Reserva confirmada para " + self.solicitante

class ReservPrioritaria:
    def __init__(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
            self.cancha = cancha
            self.fecha = fecha
            self.hora_inicio = hora_inicio
            self.hora_fin = hora_fin
            self.solicitante = solicitante
    
    def confirmar(self):
            return "Reserva con prioridadconfirmada para " + self.solicitante

def reserva_desde_web():
    if solicitante es EquipoOficial
    else: 
         reserva = reserva_regular  #pseudocodigo



def reservar_desde_hall():
     