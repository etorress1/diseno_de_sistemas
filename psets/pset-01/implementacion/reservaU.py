from datetime import datetime


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

    def realizar_reserva(self, reserva):
        self.reservas.append(reserva)
        print(f"{self.nombre} realizó la reserva {reserva.id}")


# =========================================================
# CAPITÁN
# =========================================================

class Capitan(Estudiante):
    def __init__(self, nombre, email, id_usuario, codigo_estud,
                 fecha_in, fecha_fin):
        super().__init__(nombre, email, id_usuario, codigo_estud)
        self.fecha_in = fecha_in
        self.fecha_fin = fecha_fin
        self.equipo = None

    def liderar(self, equipo):
        self.equipo = equipo
        equipo.capitan = self
        print(f"{self.nombre} ahora lidera al equipo {equipo.nombre}")

    def tiene_prioridad(self, disponibilidad):
        return (
            disponibilidad.es_horario_prioritario()
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
    def __init__(self, fecha_hora_inicio, fecha_hora_fin):
        self.fecha_hora_inicio = fecha_hora_inicio
        self.fecha_hora_fin = fecha_hora_fin

    def es_horario_prioritario(self):
        """
        El horario es prioritario si comienza antes de las 18:00.
        """
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

    def disponible(self, disponibilidad):
        """
        Verifica si la disponibilidad todavía puede reservarse.
        """
        for reserva in self.reservas:
            if reserva.disponibilidad == disponibilidad:
                return False

        return True

    def agregar_disponibilidad(self, disponibilidad):
        self.disponibilidades.append(disponibilidad)


# =========================================================
# POLÍTICAS
# =========================================================

class Politicas:
    def __init__(self, nombre, dias_anticipacion):
        self.nombre = nombre
        self.dias_anticipacion = dias_anticipacion

    def puede_reservar(self, usuario, disponibilidad):
        """
        Verifica si el usuario puede realizar una reserva.

        Los capitanes tienen prioridad en horarios
        anteriores a las 18:00.
        """

        if isinstance(usuario, Capitan):
            if disponibilidad.es_horario_prioritario():
                print(
                    f"{usuario.nombre} tiene prioridad "
                    f"por ser capitán."
                )

        return True


# =========================================================
# RESERVA
# =========================================================

class Reserva:
    def __init__(self, id_reserva, usuario, cancha,
                 disponibilidad, politica):
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
            self.usuario.reservas.append(self)

            print(f"Reserva {self.id} confirmada.")
        else:
            print("La cancha ya no está disponible.")

    def cancelar(self):
        self.estado = "cancelada"

        if self in self.cancha.reservas:
            self.cancha.reservas.remove(self)

        if self in self.usuario.reservas:
            self.usuario.reservas.remove(self)

        print(f"Reserva {self.id} cancelada.")


# =========================================================
# EJEMPLO DE USO
# =========================================================

if __name__ == "__main__":

    # -----------------------------------------------------
    # Crear estudiantes
    # -----------------------------------------------------

    estudiante = Estudiante(
        "Juan",
        "juan@usfq.edu.ec",
        1,
        "00123456"
    )

    capitan = Capitan(
        "Carlos",
        "carlos@usfq.edu.ec",
        2,
        "00654321",
        "2026-09-01",
        "2027-09-01"
    )

    # -----------------------------------------------------
    # Crear equipo
    # -----------------------------------------------------

    equipo = Equipo(
        "USFQ Eagles",
        "Fútbol"
    )

    capitan.liderar(equipo)

    # -----------------------------------------------------
    # Crear cancha
    # -----------------------------------------------------

    cancha = Cancha(
        "C01",
        "Fútbol"
    )

    # -----------------------------------------------------
    # Crear disponibilidad
    # -----------------------------------------------------

    disponibilidad = Disponibilidad(
        datetime(2026, 9, 10, 17, 0),
        datetime(2026, 9, 10, 18, 0)
    )

    cancha.agregar_disponibilidad(disponibilidad)

    # -----------------------------------------------------
    # Crear política
    # -----------------------------------------------------

    politica = Politicas(
        "Política de reservas",
        7
    )

    # -----------------------------------------------------
    # Verificar disponibilidad
    # -----------------------------------------------------

    if cancha.disponible(disponibilidad):

        print("La cancha está disponible.")

        # -------------------------------------------------
        # Verificar política
        # -------------------------------------------------

        if politica.puede_reservar(capitan, disponibilidad):

            # ---------------------------------------------
            # Crear reserva
            # ---------------------------------------------

            reserva = Reserva(
                1,
                capitan,
                cancha,
                disponibilidad,
                politica
            )

            # ---------------------------------------------
            # Confirmar reserva
            # ---------------------------------------------

            reserva.confirmar()

    else:
        print("La cancha no está disponible.")