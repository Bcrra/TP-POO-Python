def menu_opciones():
    print("Sistema de Gestion de Facultad:")
    print("1-Agregar Estudiante:")
    print("2-Agregar Curso:")
    print("3-Inscribir Estudiante a Curso:")
    print("4-Dar de Baja Estudiante de Curso:")
    print("5-Consultar Estado de Cursos:")
    print("6-Consultar Estado de Estudiantes:")
    print("7-Salir:")

    return input("Seleccione una opcion: ")


class Estudiante:
    def __init__(self, nombre_apellido: str, matricula: int, carrera: str):
        self.__nombre_apellido = nombre_apellido
        self.__matricula = matricula
        self.__carrera = carrera
        self.cursos_inscriptos = []

    def obtenerNombre(self):
        return self.__nombre_apellido

    def obtenerMatricula(self):
        return self.__matricula

    def obtenerCarrera(self):
        return self.__carrera


class Curso:
    def __init__(self, nombre_curso: str, codigo_curso: int, profesor: str, capacidad: int):
        self.__nombre_curso = nombre_curso
        self.__codigo_curso = codigo_curso
        self.__profesor = profesor
        self.__capacidad = capacidad
        self.inscriptos = []

    def obtenerNombreCurso(self):
        return self.__nombre_curso

    def obtenerCodigo(self):
        return self.__codigo_curso

    def obtenerProfesor(self):
        return self.__profesor

    def obtenerCapacidad(self):
        return self.__capacidad


class SistemaFacultad:
    def __init__(self):
        self.lista_estudiantes: list[Estudiante] = []
        self.lista_cursos: list[Curso] = []

    def buscarEstudiante(self, matricula: int):
        for estudiante in self.lista_estudiantes:
            if estudiante.obtenerMatricula() == matricula:
                return estudiante
        return None

    def buscarCurso(self, codigo_curso: int):
        for curso in self.lista_cursos:
            if curso.obtenerCodigo() == codigo_curso:
                return curso
        return None

    def agregarEstudiante(self):
        while True:
            nombre_apellido = input("Ingrese Nombre y Apellido del estudiante a ingresar: ")
            if nombre_apellido == "":
                print("Error: El nombre no puede estar vacío.")
                continue
            contiene_numero = False
            for caracter in nombre_apellido:
                if caracter in "0123456789":
                    contiene_numero = True
            if contiene_numero:
                print("El nombre y apellido no puede contener números. Intente de nuevo.")
            else:
                break

        while True:
            matricula = int(input("Ingrese matricula correspondiente: "))
            if self.buscarEstudiante(matricula) is not None:
                print("Ya existe un estudiante registrado con la matrícula", matricula)
            else:
                break

        print("Seleccione la carrera del estudiante:")
        print("1- Análisis Funcional de Sistemas Informáticos")
        print("2- Desarrollo de Software")
        print("3- Infraestructura de la Información")

        carreras_disponibles = {
            "1": "Análisis Funcional de Sistemas Informáticos",
            "2": "Desarrollo de Software",
            "3": "Infraestructura de la Información",
        }
        while True:
            opcion = input("Ingrese una opción (1-3): ")
            if opcion in carreras_disponibles:
                carrera = carreras_disponibles[opcion]
                break
            print("Opción inválida. Debe ingresar 1, 2 o 3.")

        self.lista_estudiantes.append(Estudiante(nombre_apellido, matricula, carrera))
        print("El estudiante se agregó con éxito.")

    def agregarCurso(self):
        while True:
            nombre_curso = input("Ingrese el nombre del curso a agregar: ")
            if nombre_curso == "":
                print("Error: El nombre del curso no puede estar vacío.")
            else:
                break

        while True:
            codigo_curso = int(input("Ingrese el codigo del curso correspondiente: "))
            if self.buscarCurso(codigo_curso) is not None:
                print("Ya existe un curso registrado con el código", codigo_curso)
            else:
                break

        profesor = input("Ingrese el profesor/a encargado/a del curso: ")
        capacidad = int(input("Ingrese la capacidad maxima de alumnos que puede tener el curso: "))

        self.lista_cursos.append(Curso(nombre_curso, codigo_curso, profesor, capacidad))
        print("El curso se agregó con éxito.")

    def inscribirEstudiante(self):
        matricula = int(input("Ingrese la matricula del estudiante: "))
        codigo_curso = int(input("Ingrese el codigo del curso: "))

        estudiante = self.buscarEstudiante(matricula)
        curso = self.buscarCurso(codigo_curso)

        if estudiante is None:
            print("No se encontró ningún estudiante con esa matrícula.")
            return

        if curso is None:
            print("No se encontró ningún curso con ese código.")
            return

        if len(curso.inscriptos) >= curso.obtenerCapacidad():
            print("El curso ya alcanzó su capacidad máxima de alumnos.")
            return

        curso.inscriptos.append(estudiante)
        estudiante.cursos_inscriptos.append(curso)
        print("Estudiante:", estudiante.obtenerNombre(), "Matrícula:", estudiante.obtenerMatricula(), "fue inscripto/a correctamente")

    def darDeBajaEstudiante(self):
        matricula = int(input("Ingrese la matricula del estudiante a dar de baja: "))
        codigo_curso = int(input("Ingrese el codigo del curso: "))

        estudiante = self.buscarEstudiante(matricula)
        curso = self.buscarCurso(codigo_curso)

        if estudiante is None:
            print(" No se encontró ningún estudiante con esa matrícula.")
            return

        if curso is None:
            print("No se encontró ningún curso con ese código.")
            return

        if curso not in estudiante.cursos_inscriptos:
            print("El estudiante no estába inscripto en el curso.")
            return

        curso.inscriptos.remove(estudiante)
        estudiante.cursos_inscriptos.remove(curso)
        print("El estudiante con el siguiente numero de matricula", matricula, "se ha dado de baja del curso con el siguiente codigo ", codigo_curso)

    def mostrarCursos(self):
        if not self.lista_cursos:
            print("No hay cursos registrados en el sistema.")
            return

        print("ESTADO DE CURSOS")
        for curso in self.lista_cursos:
            total_inscriptos = len(curso.inscriptos)
            cupos_libres = curso.obtenerCapacidad() - total_inscriptos

            print("Curso:", curso.obtenerNombreCurso(), "Código:", curso.obtenerCodigo())
            print("  Profesor:", curso.obtenerProfesor())
            print("  Inscriptos:", total_inscriptos, "/ Capacidad Máxima:", curso.obtenerCapacidad())
            print("  Cupos disponibles:", cupos_libres)

    def mostrarEstudiantes(self):
        if not self.lista_estudiantes:
            print("No hay estudiantes registrados en el sistema.")
            return

        print("ESTADO DE ESTUDIANTES")
        for estudiante in self.lista_estudiantes:
            print("Estudiante:", estudiante.obtenerNombre(), "Matrícula:", estudiante.obtenerMatricula())
            print("  Carrera:", estudiante.obtenerCarrera())

            if estudiante.cursos_inscriptos:
                print("  Cursos inscriptos:")
                for curso in estudiante.cursos_inscriptos:
                    print("-", curso.obtenerNombreCurso())
            else:
                print("  Cursos inscriptos: Ninguno")


def main():
    sistema = SistemaFacultad()
    while True:
        opcion = menu_opciones()

        if opcion == "7":
            break
        elif opcion == "1":
            sistema.agregarEstudiante()
        elif opcion == "2":
            sistema.agregarCurso()
        elif opcion == "3":
            sistema.inscribirEstudiante()
        elif opcion == "4":
            sistema.darDeBajaEstudiante()
        elif opcion == "5":
            sistema.mostrarCursos()
        elif opcion == "6":
            sistema.mostrarEstudiantes()

    print("Programa Terminado")


main()
