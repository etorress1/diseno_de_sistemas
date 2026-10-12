
from datetime import datetime, timedelta
from threading import Lock

from abstract_factory import FabricaCampusNorte, FabricaCampusSur
from builder import ReservaRecurrenteBuilder
from concurrencia import GestorConcurrencia
from factories import (
    CreadorReservaEstudiante,
    CreadorReservaCapitan,
)
from prototype import Bloqueo


class ReservaUFacade:
    """Coordina las operaciones principales de ReservaU."""

    def __init__(self):
        self.reservas = []
        self.bloqueos = []
        self._siguiente_id = 1
        self._gestor_concurrencia = GestorConcurrencia()
        self._lock_datos = Lock()

        self.fabricas = {
            "Campus Norte": FabricaCampusNorte(),
            "Campus Sur": FabricaCampusSur(),
        }

    def _nueva_id(self):
        with self._lock_datos:
            identificador = self._siguiente_id
            self._siguiente_id += 1
            return identificador

    @staticmethod
    def _clave(cancha, disponibilidad):
        inicio = disponibilidad.fecha_hora_inicio
        return cancha.codigo, inicio

    def reservar(
        self,
        solicitante,
        cancha,
        disponibilidad,
        politica,
        sede="Campus Norte",
    ):
        print(f"\n[Facade] Solicitud de reserva en {sede}.")

        if sede not in self.fabricas:
            print("[Facade] Sede no reconocida.")
            return None

        fabrica = self.fabricas[sede]
        validador = fabrica.crear_validador()
        notificador = fabrica.crear_notificador()

        if not validador.validar(disponibilidad):
            print("[Facade] Reserva rechazada: horario fuera de la sede.")
            return None

        if getattr(solicitante, "suspendido_hasta", None):
            if datetime.now() < solicitante.suspendido_hasta:
                print("[Facade] Reserva rechazada: solicitante suspendido.")
                return None

        if isinstance(solicitante, type(None)):
            print("[Facade] Reserva rechazada: solicitante inválido.")
            return None

        if isinstance(solicitante, __import__("dominio").Capitan):
            creador = CreadorReservaCapitan()
        else:
            creador = CreadorReservaEstudiante()

        identificador = self._nueva_id()
        reserva = creador.crear_reserva(
            identificador,
            solicitante,
            cancha,
            disponibilidad,
            politica,
        )
        reserva.sede = sede

        def registrar():
            if not cancha.disponible(disponibilidad):
                return False

            if hasattr(politica, "puede_reservar"):
                if not politica.puede_reservar(
                    solicitante, disponibilidad
                ):
                    return False

            if not cancha.tiene_disponibilidad_registrada(disponibilidad):
                return False

            return reserva.confirmar()

        clave = self._clave(cancha, disponibilidad)
        confirmada = self._gestor_concurrencia.reservar_atomicamente(
            clave, registrar
        )

        if not confirmada:
            print("[Facade] Reserva rechazada: franja no disponible.")
            return None

        self.reservas.append(reserva)

        if hasattr(solicitante, "reservas"):
            solicitante.reservas.append(reserva)

        notificador.notificar(
            getattr(solicitante, "email", "usuario"),
            f"Reserva {reserva.id} confirmada en {sede}.",
        )
        return reserva

    def cancelar(self, reserva, horas_restantes=None, administrativa=False):
        if reserva is None:
            print("[Facade] No se puede cancelar una reserva inexistente.")
            return False

        if horas_restantes is None:
            diferencia = (
                reserva.disponibilidad.fecha_hora_inicio - datetime.now()
            )
            horas_restantes = diferencia.total_seconds() / 3600

        if administrativa:
            resultado = reserva.estrategia_cancelacion.__class__.__name__
            from estrategias import AnulacionAdministrativa
            resultado = AnulacionAdministrativa().cancelar(reserva)
        elif hasattr(reserva, "estrategia_cancelacion"):
            resultado = reserva.estrategia_cancelacion.cancelar(
                reserva, horas_restantes
            )
        else:
            resultado = reserva.cancelar()

        if resultado == "NO_SHOW" or getattr(reserva, "estado", "") == "NO_SHOW":
            self._registrar_no_show(reserva.usuario)

        return resultado

    def _registrar_no_show(self, solicitante):
        ahora = datetime.now()
        if not hasattr(solicitante, "no_shows"):
            solicitante.no_shows = []

        solicitante.no_shows.append(ahora)
        inicio_mes = ahora.replace(day=1, hour=0, minute=0, second=0)

        del solicitante.no_shows[
            :sum(1 for fecha in solicitante.no_shows if fecha < inicio_mes)
        ]

        from configuracion import ConfiguracionReservaU
        configuracion = ConfiguracionReservaU()

        if len(solicitante.no_shows) >= configuracion.limite_no_shows:
            solicitante.suspendido_hasta = (
                ahora + timedelta(days=configuracion.dias_suspension)
            )
            print(
                f"[Facade] {solicitante.nombre} queda suspendido "
                f"hasta {solicitante.suspendido_hasta:%Y-%m-%d %H:%M}."
            )

    def reservar_recurrente(
        self,
        solicitante,
        cancha,
        fecha_inicio,
        franja,
        politica,
        semanas=2,
        equipo_prestado=None,
        notas="",
        sede="Campus Norte",
    ):
        recurrente = (
            ReservaRecurrenteBuilder()
            .con_cancha(cancha)
            .con_fecha_inicio(fecha_inicio)
            .con_franja(franja)
            .con_solicitante(solicitante)
            .con_semanas(semanas)
            .con_equipo_prestado(equipo_prestado or [])
            .con_notas(notas)
            .construir()
        )

        print(
            f"\n[Facade] Validando recurrencia de {semanas} semanas. "
            "No se registrará ninguna hasta verificar todas."
        )

        candidatas = []
        for semana in range(recurrente.semanas):
            inicio = recurrente.fecha_inicio + timedelta(weeks=semana)
            fin = inicio + timedelta(
                hours=(
                    recurrente.franja.fecha_hora_fin
                    - recurrente.franja.fecha_hora_inicio
                ).total_seconds() / 3600
            )

            from dominio import Disponibilidad
            disponibilidad = Disponibilidad(inicio, fin)

            if not cancha.disponible(disponibilidad):
                print(
                    f"[Facade] Conflicto en la semana {semana + 1}. "
                    "Se cancela toda la operación."
                )
                return []

            candidatas.append(disponibilidad)

        creadas = []
        for disponibilidad in candidatas:
            reserva = self.reservar(
                solicitante,
                cancha,
                disponibilidad,
                politica,
                sede,
            )
            if reserva is None:
                print("[Facade] Conflicto durante el registro; recurrencia detenida.")
                return []
            reserva.equipo_prestado = recurrente.equipo_prestado
            reserva.notas = recurrente.notas
            creadas.append(reserva)

        print(f"[Facade] Recurrencia confirmada: {len(creadas)} reservas.")
        return creadas

    def bloquear(self, plantilla, canchas_fechas):
        print("\n[Facade] Aplicando bloqueos desde una plantilla.")

        creados = []
        for cancha, fecha in canchas_fechas:
            bloqueo = plantilla.clonar(cancha, fecha)

            afectadas = [
                reserva
                for reserva in self.reservas
                if reserva.cancha == cancha
                and reserva.disponibilidad.fecha_hora_inicio.date() == fecha
                and reserva.estado.lower() == "confirmada"
                and reserva.disponibilidad.fecha_hora_inicio.time()
                < bloqueo.hora_fin
                and reserva.disponibilidad.fecha_hora_fin.time()
                > bloqueo.hora_inicio
            ]

            for reserva in afectadas:
                self.cancelar(reserva, administrativa=True)
                sede = getattr(reserva, "sede", "Campus Norte")
                notificador = self.fabricas[sede].crear_notificador()
                notificador.notificar(
                    getattr(reserva.usuario, "email", "usuario"),
                    f"Reserva {reserva.id} anulada por: {bloqueo.motivo}.",
                )

            self.bloqueos.append(bloqueo)
            creados.append(bloqueo)
            print(f"[Facade] Bloqueo aplicado a cancha {cancha.codigo}.")

        return creados