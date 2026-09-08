from datetime import datetime


# =========================================================
# REGLAS DE PRIORIDAD
# =========================================================

class ReglaPrioridad:

    def tiene_prioridad(self, disponibilidad):
        return False


class PrioridadAntesDeLas6(ReglaPrioridad):

    def tiene_prioridad(self, disponibilidad):
        return disponibilidad.fecha_hora_inicio.hour < 18


class SinPrioridad(ReglaPrioridad):

    def tiene_prioridad(self, disponibilidad):
        return False


# =========================================================
# USUARIO
# =========================================================

class Usuario:

    def __init__(self, nombre, email, id_usuario):
        self.nombre = nombre
        self.email = email
        self.id = id_usuario


# =========================================================
# ESTUDIANTE
# =========================================================

class Estudiante(Usuario):

    def __init__(self, nombre, email, id_usuario, codigo_estud):
        super().__init__(nombre, email, id_usuario)

        self.codigo_estud = codigo_estud
        self.reservas = []
        self.regla_prioridad = SinPrioridad()

    def realizar_reserva(self, reserva):
        print(f"{self.nombre} solicita realizar una reserva.")
        self.reservas.append(reserva)

    def cancelar_reserva(self, reserva):
        print(f"{self.nombre} solicita cancelar la reserva {reserva.id}.")
        reserva.cancelar()


# =========================================================
# CAPITÁN
# =========================================================

class Capitan(Estudiante):

    def __init__(
        self,
        nombre,
        email,
        id_usuario,
        codigo_estud,
        fecha_in,
        fecha_fin
    ):
        super().__init__(
            nombre,
            email,
            id_usuario,
            codigo_estud
        )

        self.fecha_in = fecha_in
        self.fecha_fin = fecha_fin

        # El capitán recibe una regla de prioridad
        self.regla_prioridad = PrioridadAntesDeLas6()

        self.equipo = None

    def liderar(self, equipo):
        self.equipo = equipo
        equipo.capitan = self


# =========================================================
# ADMINISTRADOR
# =========================================================

class Administrador(Usuario):

    def gestionar_cancha(self, cancha):
        print(
            f"Administrador gestiona la cancha {cancha.codigo}."
        )

    def intervenir_conflicto(self, reserva):
        print(
            f"Administrador interviene en la reserva "
            f"{reserva.id}."
        )


# =========================================================
# EQUIPO
# =========================================================

class Equipo:

    def __init__(self, nombre, deporte):
        self.nombre = nombre
        self.deporte = deporte
        self.capitan = None


# =========================================================
# DISPONIBILIDAD
# =========================================================

class Disponibilidad:

    def __init__(
        self,
        fecha_hora_inicio,
        fecha_hora_fin
    ):
        self.fecha_hora_inicio = fecha_hora_inicio
        self.fecha_hora_fin = fecha_hora_fin

    def es_horario_prioritario(self):
        return self.fecha_hora_inicio.hour < 18


# =========================================================
# CANCHA
# =========================================================

class Cancha:

    def __init__(self, codigo, deporte):
        self.codigo = codigo
        self.deporte = deporte
        self.disponibilidades = []
        self.reservas = []

    def agregar_disponibilidad(self, disponibilidad):
        self.disponibilidades.append(disponibilidad)

    def disponible(self, disponibilidad):

        for reserva in self.reservas:

            if reserva.disponibilidad == disponibilidad:
                return False

        return True


# =========================================================
# POLÍTICAS
# =========================================================

class Politicas:

    def __init__(self, nombre, dias_anticipacion):
        self.nombre = nombre
        self.dias_anticipacion = dias_anticipacion

    def puede_reservar(self, usuario, disponibilidad):

        return True


# =========================================================
# RESERVA
# =========================================================

class Reserva:

    def __init__(
        self,
        id_reserva,
        usuario,
        cancha,
        disponibilidad,
        politica
    ):
        self.id = id_reserva
        self.creada = datetime.now()
        self.estado = "pendiente"

        self.usuario = usuario
        self.cancha = cancha
        self.disponibilidad = disponibilidad
        self.politica = politica

    def confirmar(self):

        if self.cancha.disponible(self.disponibilidad):

            self.estado = "confirmada"

            self.cancha.reservas.append(self)

            print(
                f"Reserva {self.id} confirmada."
            )

            return True

        print("La cancha no está disponible.")

        return False

    def cancelar(self):

        ahora = datetime.now()

        tiempo_restante = (
            self.disponibilidad.fecha_hora_inicio - ahora
        )

        horas_restantes = tiempo_restante.total_seconds() / 3600

        if horas_restantes < 2:

            self.registrar_no_show()

        else:

            self.estado = "cancelada"

            print(
                f"Reserva {self.id} cancelada normalmente."
            )

    def registrar_no_show(self):

        self.estado = "no-show"

        print(
            f"Reserva {self.id} registrada como NO-SHOW."
        )