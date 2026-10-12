
from datetime import datetime, timedelta


# ============================================================
# USUARIOS
# ============================================================

class Usuario:
    def __init__(self, nombre, email, identificador):
        self.nombre = nombre
        self.email = email
        self.identificador = identificador

        self.reservas = []
        self.no_shows = []
        self.suspendido_hasta = None

    def esta_suspendido(self, ahora=None):
        """Comprueba si el usuario mantiene una suspensión activa."""
        if ahora is None:
            ahora = datetime.now()

        if self.suspendido_hasta is None:
            return False

        if ahora >= self.suspendido_hasta:
            self.suspendido_hasta = None
            return False

        return True

    def registrar_no_show(self, fecha=None):
        """
        Registra una inasistencia y comprueba si el usuario debe
        ser suspendido por acumular el límite mensual configurado.
        """
        if fecha is None:
            fecha = datetime.now()

        self.no_shows.append(fecha)

        # Se importa aquí para evitar dependencias circulares.
        from configuracion import ConfiguracionReservaU

        configuracion = ConfiguracionReservaU()

        inicio_mes = fecha.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        no_shows_mes = [
            registro
            for registro in self.no_shows
            if inicio_mes <= registro <= fecha
        ]

        cantidad = len(no_shows_mes)

        if cantidad >= configuracion.limite_no_shows:
            nueva_suspension = fecha + timedelta(
                days=configuracion.dias_suspension
            )

            # No se acorta una suspensión que ya termine después.
            if (
                self.suspendido_hasta is None
                or self.suspendido_hasta < nueva_suspension
            ):
                self.suspendido_hasta = nueva_suspension

            print(
                f"[SUSPENSIÓN] {self.nombre} suspendido hasta "
                f"{self.suspendido_hasta.strftime('%Y-%m-%d %H:%M')}."
            )

        return cantidad

    def __str__(self):
        return f"{self.nombre} ({self.email})"


class Estudiante(Usuario):
    def __init__(self, nombre, email, identificador, identificacion):
        super().__init__(nombre, email, identificador)
        self.identificacion = identificacion


class Capitan(Estudiante):
    def __init__(
        self,
        nombre,
        email,
        identificador,
        identificacion,
        fecha_inicio,
        fecha_fin
    ):
        super().__init__(
            nombre,
            email,
            identificador,
            identificacion
        )

        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.equipo = None

    def liderar(self, equipo):
        """Asocia al capitán con su equipo."""
        self.equipo = equipo
        equipo.capitan = self

    def __str__(self):
        return f"Capitán: {self.nombre}"


class Administrador(Usuario):
    def __init__(self, nombre, email, identificador):
        super().__init__(nombre, email, identificador)


# ============================================================
# EQUIPOS
# ============================================================

class Equipo:
    def __init__(self, nombre, deporte):
        self.nombre = nombre
        self.deporte = deporte
        self.capitan = None

    def asignar_capitan(self, capitan):
        self.capitan = capitan
        capitan.equipo = self

    def __str__(self):
        nombre_capitan = (
            self.capitan.nombre
            if self.capitan is not None
            else "Sin capitán"
        )

        return (
            f"Equipo: {self.nombre} | "
            f"Deporte: {self.deporte} | "
            f"Capitán: {nombre_capitan}"
        )


# ============================================================
# DISPONIBILIDAD
# ============================================================

class Disponibilidad:
    def __init__(self, fecha_hora_inicio, fecha_hora_fin):
        if not isinstance(fecha_hora_inicio, datetime):
            raise TypeError(
                "La fecha y hora de inicio debe ser un datetime."
            )

        if not isinstance(fecha_hora_fin, datetime):
            raise TypeError(
                "La fecha y hora de fin debe ser un datetime."
            )

        if fecha_hora_fin <= fecha_hora_inicio:
            raise ValueError(
                "La fecha y hora de fin debe ser posterior al inicio."
            )

        self.fecha_hora_inicio = fecha_hora_inicio
        self.fecha_hora_fin = fecha_hora_fin

    @property
    def fecha_hora(self):
        """Compatibilidad con código que consulta la fecha de inicio."""
        return self.fecha_hora_inicio

    @property
    def hora_inicio(self):
        return self.fecha_hora_inicio.time()

    @property
    def hora_fin(self):
        return self.fecha_hora_fin.time()

    @property
    def fecha(self):
        return self.fecha_hora_inicio.date()

    def se_superpone(self, otra):
        """Devuelve True si dos intervalos temporales se cruzan."""
        return (
            self.fecha_hora_inicio < otra.fecha_hora_fin
            and otra.fecha_hora_inicio < self.fecha_hora_fin
        )

    def __str__(self):
        return (
            f"{self.fecha_hora_inicio.strftime('%Y-%m-%d %H:%M')} - "
            f"{self.fecha_hora_fin.strftime('%Y-%m-%d %H:%M')}"
        )


# ============================================================
# CANCHAS
# ============================================================

class Cancha:
    def __init__(self, codigo, deporte):
        self.codigo = codigo
        self.deporte = deporte
        self.disponibilidades = []
        self.reservas = []

    def agregar_disponibilidad(self, disponibilidad):
        if not isinstance(disponibilidad, Disponibilidad):
            raise TypeError(
                "Se debe proporcionar un objeto Disponibilidad."
            )

        self.disponibilidades.append(disponibilidad)

    def tiene_disponibilidad_registrada(self, disponibilidad):
        """
        Comprueba que todo el intervalo solicitado esté dentro
        de un intervalo de disponibilidad registrado.

        Si no se registraron intervalos explícitos, se permite
        continuar con la validación de las demás reglas.
        """
        if not self.disponibilidades:
            return True

        for intervalo in self.disponibilidades:
            if (
                intervalo.fecha_hora_inicio
                <= disponibilidad.fecha_hora_inicio
                and disponibilidad.fecha_hora_fin
                <= intervalo.fecha_hora_fin
            ):
                return True

        return False

    def disponible(self, disponibilidad):
        """Comprueba que no exista una reserva activa superpuesta."""
        estados_no_activos = {
            "CANCELADA",
            "ANULADA",
            "NO_SHOW"
        }

        for reserva in self.reservas:
            estado = str(reserva.estado).upper().replace("-", "_")

            if estado in estados_no_activos:
                continue

            if reserva.disponibilidad.se_superpone(disponibilidad):
                return False

        return True

    def __str__(self):
        return f"Cancha {self.codigo} ({self.deporte})"


# ============================================================
# POLÍTICAS DE RESERVA
# ============================================================

class Politicas:
    def __init__(self, nombre, limite_no_shows=3):
        self.nombre = nombre
        self.limite_no_shows = limite_no_shows

    def puede_reservar(self, usuario, disponibilidad=None):
        """Comprueba si el usuario puede realizar una reserva."""
        if usuario.esta_suspendido():
            print(
                f"[RECHAZADA] {usuario.nombre} está suspendido "
                f"hasta {usuario.suspendido_hasta}."
            )
            return False

        return True

    def __str__(self):
        return f"Política: {self.nombre}"


# ============================================================
# RESERVAS
# ============================================================

class Reserva:
    def __init__(
        self,
        identificador,
        usuario,
        cancha,
        disponibilidad,
        politica
    ):
        self.id = identificador
        self.usuario = usuario

        # Alias para mantener compatibilidad con la fachada.
        self.solicitante = usuario

        self.cancha = cancha
        self.disponibilidad = disponibilidad
        self.politica = politica

        self.estado = "PENDIENTE"
        self.sede = None
        self.equipo_prestado = []
        self.notas = ""

        # Se asignan desde las fábricas correspondientes.
        self.estrategia_cancelacion = None
        self.regla_prioridad = None

        # Evita registrar dos veces la misma inasistencia.
        self.no_show_registrado = False

    def confirmar(self):
        """Confirma la reserva si la cancha sigue disponible."""
        if self.estado != "PENDIENTE":
            return False

        if not self.cancha.disponible(self.disponibilidad):
            print(
                f"[RECHAZADA] La cancha {self.cancha.codigo} "
                f"ya está ocupada en ese horario."
            )
            return False

        self.estado = "CONFIRMADA"

        if self not in self.cancha.reservas:
            self.cancha.reservas.append(self)

        if self not in self.usuario.reservas:
            self.usuario.reservas.append(self)

        print(
            f"[CONFIRMADA] Reserva {self.id} | "
            f"{self.cancha.codigo} | {self.disponibilidad}"
        )

        return True

    def registrar_no_show(self):
        """
        Marca la reserva como una inasistencia una sola vez.

        El registro mensual del usuario se realiza por separado,
        desde la fachada, mediante usuario.registrar_no_show().
        """
        if self.no_show_registrado:
            return False

        self.no_show_registrado = True
        return True

    def cancelar(self, horas_restantes=None):
        """
        Delega la cancelación a la estrategia correspondiente.

        La estrategia debe devolver CANCELADA, NO_SHOW o ANULADA.
        """
        if self.estado != "CONFIRMADA":
            print(
                f"[RECHAZADA] No se puede cancelar la reserva "
                f"{self.id}: su estado es {self.estado}."
            )
            return False

        if self.estrategia_cancelacion is None:
            raise ValueError(
                "La reserva no tiene una estrategia de cancelación."
            )

        if horas_restantes is None:
            diferencia = (
                self.disponibilidad.fecha_hora_inicio - datetime.now()
            )
            horas_restantes = diferencia.total_seconds() / 3600

        return self.estrategia_cancelacion.cancelar(
            self,
            horas_restantes
        )

    def anular(self):
        """Anula administrativamente una reserva confirmada."""
        if self.estado != "CONFIRMADA":
            return False

        self.estado = "ANULADA"

        print(
            f"[ANULADA] Reserva {self.id} anulada administrativamente."
        )

        return True

    def __str__(self):
        return (
            f"Reserva {self.id} | "
            f"Usuario: {self.usuario.nombre} | "
            f"Cancha: {self.cancha.codigo} | "
            f"Horario: {self.disponibilidad} | "
            f"Estado: {self.estado}"
        )