def validar_nombre(cadena: str):
    for caracter in cadena:
        if caracter.isdigit():
            return False
    return True


def validar_dni(dni: str):
    if dni.isdigit() and len(dni) in (6, 7):
        return True
    return False


class Socio:
    def __init__(self, dni: str, nombre_completo: str):
        self.__dni = dni
        self.__nombre_completo = nombre_completo
        self.__libros_prestados = []
        self.modificarDni(dni)
        self.modificarNombre(nombre_completo)

    def obtenerNombre(self):
        return self.__nombre_completo

    def modificarNombre(self, nombre_completo: str):
        if validar_nombre(nombre_completo):
            self.__nombre_completo = nombre_completo
            return True
        print("El nombre no puede contener números.")
        return False

    def obtenerDni(self):
        return self.__dni

    def modificarDni(self, dni: str):
        if validar_dni(dni):
            self.__dni = dni
            return True
        print("El DNI debe contener solo números y tener entre 6 y 7 dígitos.")
        return False

    def obtenerPrestamos(self):
        return self.__libros_prestados

    def sumarPrestamo(self, libro):
        self.__libros_prestados.append(libro)

    def quitarPrestamo(self, libro):
        if libro in self.__libros_prestados:
            self.__libros_prestados.remove(libro)


class Libro:
    def __init__(self, titulo: str, autor: str, isbn: str, ejemplares: int):
        self.__titulo = titulo
        self.__autor = autor
        self.__isbn = isbn
        self.__ejemplares = ejemplares
        self.__socios_con_prestamo = []

    def obtenerTitulo(self):
        return self.__titulo

    def obtenerAutor(self):
        return self.__autor

    def obtenerIsbn(self):
        return self.__isbn

    def obtenerEjemplares(self):
        return self.__ejemplares

    def modificarEjemplares(self, cantidad_nueva: int):
        self.__ejemplares = cantidad_nueva

    def obtenerSocios(self):
        return self.__socios_con_prestamo

    def tieneDisponibles(self):
        if len(self.__socios_con_prestamo) < self.__ejemplares:
            return True
        return False

    def asignarA(self, socio):
        if self.tieneDisponibles():
            self.__socios_con_prestamo.append(socio)

    def liberarDe(self, socio):
        if socio in self.__socios_con_prestamo:
            self.__socios_con_prestamo.remove(socio)


class SistemaBiblioteca:
    def __init__(self):
        self.__catalogo = []
        self.__socios = []

    def buscarLibro(self, isbn):
        for libro in self.__catalogo:
            if libro.obtenerIsbn() == isbn:
                return libro
        return None

    def buscarSocio(self, dni):
        for socio in self.__socios:
            if socio.obtenerDni() == dni:
                return socio
        return None

    def agregarLibro(self):
        isbn = input("Ingrese el ISBN del libro: ")
        libro = self.buscarLibro(isbn)

        if libro != None:
            cantidad_extra = int(input("El libro ya existe. ¿Cuántos ejemplares desea agregar?: "))
            libro.modificarEjemplares(libro.obtenerEjemplares() + cantidad_extra)
            print("Ejemplares agregados con éxito.")
        else:
            titulo = input("Ingrese el título del libro: ")
            autor = input("Ingrese el autor del libro: ")
            ejemplares = int(input("Ingrese la cantidad de ejemplares: "))
            self.__catalogo.append(Libro(titulo, autor, isbn, ejemplares))
            print("Libro registrado con éxito.")

    def eliminarLibro(self):
        isbn = input("Ingrese el ISBN del libro a borrar: ")
        libro = self.buscarLibro(isbn)
        if libro == None:
            print("No se encontró un libro con ese ISBN.")
        else:
            self.__catalogo.remove(libro)
            print("Libro eliminado del sistema.")

    def agregarSocio(self):
        nombre_completo = input("Ingrese el nombre del socio: ")
        if not validar_nombre(nombre_completo):
            print("El nombre no puede contener números.")
            return

        dni = input("Ingrese el DNI del socio: ")
        if not validar_dni(dni):
            print(" El DNI debe ser numérico y tener entre 6 y 7 dígitos.")
            return

        if self.buscarSocio(dni) != None:
            print("Ya existe un miembro registrado con ese DNI.")
            return

        self.__socios.append(Socio(dni, nombre_completo))
        print("Socio registrado con éxito.")

    def eliminarSocio(self):
        dni = input("Ingrese el DNI de la persona a borrar: ")
        socio = self.buscarSocio(dni)
        if socio == None:
            print("No se encontró ningún socio con ese DNI.")
            return

        if len(socio.obtenerPrestamos()) > 0:
            print("No se puede borrar el socio porque tiene libros prestados pendientes.")
            return

        self.__socios.remove(socio)
        print("Socio eliminado con éxito.")

    def prestarLibro(self):
        dni = input("Ingrese el DNI del socio: ")
        isbn = input("Ingrese el ISBN del libro a prestar: ")

        libro = self.buscarLibro(isbn)
        if libro == None:
            print("El libro no existe.")
            return

        socio = self.buscarSocio(dni)
        if socio == None:
            print("El miembro no existe.")
            return

        if not libro.tieneDisponibles():
            print("No hay ejemplares disponibles de este libro.")
            return

        libro.asignarA(socio)
        socio.sumarPrestamo(libro)
        print("Préstamo realizado con éxito.")

    def devolverLibro(self):
        dni = input("Ingrese el DNI del socio: ")
        isbn = input("Ingrese el ISBN del libro a devolver: ")

        libro = self.buscarLibro(isbn)
        socio = self.buscarSocio(dni)

        if libro == None or socio == None:
            print("Datos incorrectos de libro o miembro.")
            return

        if socio not in libro.obtenerSocios():
            print("Ese miembro no tenía prestado este libro.")
            return

        libro.liberarDe(socio)
        socio.quitarPrestamo(libro)
        print("Libro devuelto con éxito.")

    def mostrarLibros(self):
        if len(self.__catalogo) == 0:
            print("No hay libros registrados.")
            return

        print("ESTADO DE LIBROS")
        for libro in self.__catalogo:
            disponibles = libro.obtenerEjemplares() - len(libro.obtenerSocios())
            if libro.tieneDisponibles():
                estado = "Disponible"
            else:
                estado = "No disponible"

            print("Título: " + libro.obtenerTitulo() + " | ISBN: " + libro.obtenerIsbn() + " | Estado: " + estado + " (" + str(disponibles) + "/" + str(libro.obtenerEjemplares()) + " disponibles)")

            for socio in libro.obtenerSocios():
                print("Prestado a: " + socio.obtenerNombre())

    def mostrarSocios(self):
        if len(self.__socios) == 0:
            print("No hay miembros registrados.")
            return

        print(" ESTADO DE MIEMBROS")
        for socio in self.__socios:
            print("Socio: " + socio.obtenerNombre() + " DNI: " + socio.obtenerDni())
            if len(socio.obtenerPrestamos()) > 0:
                for libro in socio.obtenerPrestamos():
                    print(" Libro prestado: " + libro.obtenerTitulo())
            else:
                print(" No tiene libros prestados ")

    def consultarLibrosSocio(self):
        dni = input("Ingrese el DNI del socio a consultar: ")
        socio = self.buscarSocio(dni)
        if socio == None:
            print("No existe un socio con ese DNI.")
            return

        print("Libros prestados a " + socio.obtenerNombre() + ":")
        if len(socio.obtenerPrestamos()) == 0:
            print("No posee libros prestados actualmente.")
        else:
            for libro in socio.obtenerPrestamos():
                print(libro.obtenerTitulo() + " ISBN: " + libro.obtenerIsbn())


def menu_opciones():
    print(" Sistema Biblioteca ")
    print("1- Agregar Libro")
    print("2- Quitar Libro")
    print("3- Agregar Miembro")
    print("4- Borrar Miembro")
    print("5- Prestar Libro")
    print("6- Devolver Libro")
    print("7- Mostrar Estado de Libros")
    print("8- Mostrar Estado de Miembros")
    print("9- Consultar Libros de un Miembro")
    print("10- Salir")
    return input("Seleccione una opción: ")


def main():
    mi_biblioteca = SistemaBiblioteca()
    while True:
        opcion = menu_opciones()

        if opcion == "10":
            break
        elif opcion == "1":
            mi_biblioteca.agregarLibro()
        elif opcion == "2":
            mi_biblioteca.eliminarLibro()
        elif opcion == "3":
            mi_biblioteca.agregarSocio()
        elif opcion == "4":
            mi_biblioteca.eliminarSocio()
        elif opcion == "5":
            mi_biblioteca.prestarLibro()
        elif opcion == "6":
            mi_biblioteca.devolverLibro()
        elif opcion == "7":
            mi_biblioteca.mostrarLibros()
        elif opcion == "8":
            mi_biblioteca.mostrarSocios()
        elif opcion == "9":
            mi_biblioteca.consultarLibrosSocio()

    print("Programa Terminado.")


main()
