from abc import ABC, abstractmethod


class Boton(ABC):
    @abstractmethod
    def renderizar(self):
        pass


class Menu(ABC):
    @abstractmethod
    def renderizar(self):
        pass


class MenuWindows(Menu):
    def renderizar(self):
        print("Menú estilo Windows...")


class BotonWindows(Boton):
    def renderizar(self):
        print("Botón estilo Windows...")


class MenuMac(Menu):
    def renderizar(self):
        print("Menú estilo Mac...")


class BotonMac(Boton):
    def renderizar(self):
        print("Botón estilo Mac...")


class UIFactoryABC(ABC):

    @abstractmethod
    def crear_boton(self):
        pass

    @abstractmethod
    def crear_menu(self):
        pass


class WindowsFactory(UIFactoryABC):

    def crear_boton(self):
        return BotonWindows()

    def crear_menu(self):
        return MenuWindows()


class MacFactory(UIFactoryABC):

    def crear_boton(self):
        return BotonMac()

    def crear_menu(self):
        return MenuMac()


def crear_UI(factory, sistema):
    boton = factory.crear_boton()
    menu = factory.crear_menu()

    boton.renderizar()
    menu.renderizar()

    print(f"✓ Estilo seleccionado: {sistema}")


def main():

    sistema = "Mac"

    if sistema == "Windows":
        factory = WindowsFactory()

    elif sistema == "Mac":
        factory = MacFactory()

    crear_UI(factory, sistema)


main()

