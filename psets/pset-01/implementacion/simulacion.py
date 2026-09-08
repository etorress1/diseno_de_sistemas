from datetime import datetime, timedelta

from clases import (
    Estudiante,
    Capitan,
    Administrador,
    Equipo,
    Cancha,
    Disponibilidad,
    Politicas,
    Reserva
)


print("========================================")
print("SIMULACIÓN RESERVAU")
print("========================================")


# =========================================================
# CREACIÓN DE USUARIOS
# =========================================================

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

administrador = Administrador(
    "Administrador",
    "admin@usfq.edu.ec",
    3
)


# =========================================================
# EQUIPO
# =========================================================

equipo = Equipo(
    "USFQ Eagles",
    "Fútbol"
)

capitan.liderar(equipo)

print("\nEquipo creado:")
print(f"Equipo: {equipo.nombre}")
print(f"Capitán: {equipo.capitan.nombre}")


# =========================================================
# CANCHA
# =========================================================

cancha = Cancha(
    "C01",
    "Fútbol"
)

print("\nCancha creada:")
print(cancha.codigo)


# =========================================================
# DISPONIBILIDAD
# =========================================================

inicio = datetime.now() + timedelta(hours=3)

fin = inicio + timedelta(hours=1)

disponibilidad = Disponibilidad(
    inicio,
    fin
)

cancha.agregar_disponibilidad(
    disponibilidad
)

print("\nDisponibilidad creada.")


# =========================================================
# POLÍTICA
# =========================================================

politica = Politicas(
    "Política de reservas",
    7
)


# =========================================================
# RESERVA DEL CAPITÁN
# =========================================================

print("\n----------------------------------------")
print("CASO DE USO: REALIZAR RESERVA")
print("----------------------------------------")

print("1. El capitán solicita realizar una reserva.")

print("2. El sistema verifica disponibilidad.")

if cancha.disponible(disponibilidad):

    print("   La cancha está disponible.")

    print("3. El sistema valida las políticas.")

    if politica.puede_reservar(
        capitan,
        disponibilidad
    ):

        print("   Las políticas permiten la reserva.")

        print("4. El sistema aplica la regla de prioridad.")

        if capitan.regla_prioridad.tiene_prioridad(
            disponibilidad
        ):
            print(
                "   El capitán tiene prioridad "
                "antes de las 18:00."
            )
        else:
            print("   No existe prioridad.")

        print("5. El sistema crea la reserva.")

        reserva = Reserva(
            1,
            capitan,
            cancha,
            disponibilidad,
            politica
        )

        print("6. El sistema confirma la reserva.")

        reserva.confirmar()


# =========================================================
# CANCELACIÓN
# =========================================================

print("\n----------------------------------------")
print("CASO DE USO: CANCELAR RESERVA")
print("----------------------------------------")

print("1. El capitán solicita cancelar la reserva.")

print("2. El sistema verifica el tiempo restante.")

capitan.cancelar_reserva(reserva)


# =========================================================
# ADMINISTRADOR
# =========================================================

print("\n----------------------------------------")
print("CASO DE USO: GESTIONAR CANCHA")
print("----------------------------------------")

administrador.gestionar_cancha(cancha)


print("\n----------------------------------------")
print("CASO DE USO: INTERVENIR EN CONFLICTO")
print("----------------------------------------")

administrador.intervenir_conflicto(reserva)


print("\n========================================")
print("SIMULACIÓN FINALIZADA")
print("========================================")