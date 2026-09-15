from singleton import GestorDeConfiguracion


def test_rechaza_reserva():
    config = GestorDeConfiguracion.obtener_objeto()
    config.modo_mantenimiento = True


    assert GestorDeConfiguracion.reserva_permitida(config) is False


def test_reserva_aceptada():
    config = GestorDeConfiguracion.obtener_objeto()

    assert GestorDeConfiguracion.reserva_permitida(config) is True
        

#El problema viene del que el singleton es una variable global

