class Inventario:

    def verificar(self, producto):
        print(f"Verificando el stock de {producto}")
        return True


class Pago:

    def procesar(self, monto):
        print(f"Procesando pago: ${monto}")
        return True


class Envio:

    def crear_envio(self, producto):
        print(f"Preparando el envio de {producto}")


class TiendaFacade:

    def __init__(self):
        self.inventario = Inventario()
        self.pago = Pago()
        self.envio = Envio()

    def comprar(self, producto, precio):

        if not self.inventario.verificar(producto):
            print("No hay stock")
            return False

        if not self.pago.procesar(precio):
            print("Fallo el pago")
            return False

        self.envio.crear_envio(producto)

        print("Compra completada")
        return True


class SistemaNotificacion:

    def notificar(self, producto, compra_exitosa):

        if compra_exitosa:
            print("SE HIZO UNA COMPRA EXITOSA DEL PRODUCTO:", producto)


def main():

    tienda = TiendaFacade()
    notificacion = SistemaNotificacion()

    producto = "Laptop"
    precio = 1500

    resultado = tienda.comprar(producto, precio)

    notificacion.notificar(producto, resultado)


main()
  