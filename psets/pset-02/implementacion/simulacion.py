
from datetime import datetime, timedelta
from threading import Thread, Barrier

from dominio import (
    Estudiante,
    Capitan,
    Administrador,
    Equipo,
    Cancha,
    Disponibilidad,
    Politicas,
)
from facade import ReservaUFacade
from prototype import Bloqueo


def crear_disponibilidad(fecha, hora, duracion=1):
    inicio = fecha.replace(
        hour=hora, minute=0, second=0, microsecond=0
    )
    return Disponibilidad(inicio, inicio + timedelta(hours=duracion))


def encabezado(numero, texto):
    print("\n" + "=" * 65)
    print(f"ESCENARIO {numero}: {texto}")
    print("=" * 65)


def ejecutar_simulacion():
    sistema = ReservaUFacade()
    politica = Politicas("Política general", 7)

    estudiante = Estudiante(
        "Juan", "juan@usfq.edu.ec", 1, "00123456"
    )
    estudiante2 = Estudiante(
        "Ana", "ana@usfq.edu.ec", 2, "00123457"
    )
    capitan = Capitan(
        "Carlos", "carlos@usfq.edu.ec", 3, "00123458",
        "2026-09-01", "2027-09-01"
    )
    administrador = Administrador(
        "Administrador", "admin@usfq.edu.ec", 4
    )
    equipo = Equipo("USFQ Eagles", "Fútbol")
    capitan.liderar(equipo)

    norte = Cancha("N-01", "Fútbol")
    sur = Cancha("S-01", "Fútbol")
    cancha_recurrente = Cancha("N-02", "Fútbol")
    cancha_bloqueo = Cancha("N-03", "Fútbol")

    base = datetime.now() + timedelta(days=5)
    base = base.replace(minute=0, second=0, microsecond=0)

    # 1. Una reserva por sede y su notificación correspondiente.
    encabezado(1, "Reservas en Campus Norte y Campus Sur")

    reserva_norte = sistema.reservar(
        estudiante, norte, crear_disponibilidad(base, 10),
        politica, "Campus Norte"
    )
    reserva_sur = sistema.reservar(
        estudiante2, sur, crear_disponibilidad(base, 11),
        politica, "Campus Sur"
    )

    # 2. Rechazo por horario fuera de la sede.
    encabezado(2, "Rechazo por horario fuera del permitido")

    sistema.reservar(
        estudiante, norte, crear_disponibilidad(base, 23),
        politica, "Campus Norte"
    )

    # 3. Recurrencia exitosa y recurrencia con conflicto.
    encabezado(3, "Reserva recurrente: éxito y conflicto")

    sistema.reservar_recurrente(
        capitan,
        cancha_recurrente,
        base.replace(hour=14),
        crear_disponibilidad(base, 14),
        politica,
        semanas=3,
        equipo_prestado=["balón", "chalecos"],
        notas="Entrenamiento semanal",
        sede="Campus Norte",
    )

    cancha_conflicto = Cancha("N-04", "Fútbol")
    fecha_conflicto = base + timedelta(weeks=1)
    sistema.reservar(
        estudiante2,
        cancha_conflicto,
        crear_disponibilidad(fecha_conflicto, 16),
        politica,
        "Campus Norte",
    )

    sistema.reservar_recurrente(
        capitan,
        cancha_conflicto,
        base.replace(hour=16),
        crear_disponibilidad(base, 16),
        politica,
        semanas=3,
        sede="Campus Norte",
    )

    # 4. Tres resultados de cancelación.
    encabezado(4, "Cancelaciones con resultados distintos")

    reserva_estudiante = sistema.reservar(
        estudiante,
        Cancha("N-05", "Fútbol"),
        crear_disponibilidad(base, 15),
        politica,
        "Campus Norte",
    )
    sistema.cancelar(reserva_estudiante, horas_restantes=5)

    reserva_capitan = sistema.reservar(
        capitan,
        Cancha("N-06", "Fútbol"),
        crear_disponibilidad(base, 17),
        politica,
        "Campus Norte",
    )
    sistema.cancelar(reserva_capitan, horas_restantes=1)

    reserva_admin = sistema.reservar(
        estudiante2,
        Cancha("N-07", "Fútbol"),
        crear_disponibilidad(base, 18),
        politica,
        "Campus Norte",
    )
    sistema.cancelar(
        reserva_admin, horas_restantes=1, administrativa=True
    )

    # 5. Tres no-shows y un intento posterior.
    encabezado(5, "Suspensión tras tres no-shows")

    for numero in range(3):
        cancha = Cancha(f"SUSP-{numero + 1}", "Fútbol")
        disponibilidad = crear_disponibilidad(
            base + timedelta(days=numero), 12
        )
        reserva = sistema.reservar(
            capitan, cancha, disponibilidad, politica, "Campus Norte"
        )
        sistema.cancelar(reserva, horas_restantes=1)

    sistema.reservar(
        capitan,
        Cancha("SUSP-INTENTO", "Fútbol"),
        crear_disponibilidad(base + timedelta(days=4), 12),
        politica,
        "Campus Norte",
    )

    # 6. Clonar bloqueos a varias canchas y fechas.
    encabezado(6, "Bloqueos clonados y notificación de afectados")

    fecha_bloqueo = base.date()
    reserva_afectada = sistema.reservar(
        estudiante,
        cancha_bloqueo,
        crear_disponibilidad(base, 19),
        politica,
        "Campus Norte",
    )

    plantilla = Bloqueo(
        motivo="Mantenimiento",
        fecha=fecha_bloqueo,
        hora_inicio=__import__("datetime").time(19, 0),
        hora_fin=__import__("datetime").time(20, 0),
        equipo_montaje=["herramientas"],
    )

    sistema.bloquear(
        plantilla,
        [
            (cancha_bloqueo, fecha_bloqueo),
            (Cancha("N-08", "Fútbol"), fecha_bloqueo),
        ],
    )

    # 7. Dos hilos intentan reservar la misma cancha y franja.
    encabezado(7, "Concurrencia: una sola reserva confirmada")

    cancha_compartida = Cancha("CONC-01", "Fútbol")
    franja_compartida = crear_disponibilidad(base + timedelta(days=8), 13)
    barrera = Barrier(2)
    resultados = []

    def intentar(usuario):
        barrera.wait()
        resultado = sistema.reservar(
            usuario,
            cancha_compartida,
            franja_compartida,
            politica,
            "Campus Norte",
        )
        resultados.append(resultado)

    hilo1 = Thread(target=intentar, args=(estudiante,))
    hilo2 = Thread(target=intentar, args=(estudiante2,))
    hilo1.start()
    hilo2.start()
    hilo1.join()
    hilo2.join()

    exitosas = sum(resultado is not None for resultado in resultados)
    print(f"\nResultado concurrente: {exitosas} reserva(s) confirmada(s).")
    print("SIMULACIÓN FINALIZADA")


if __name__ == "__main__":
    ejecutar_simulacion()