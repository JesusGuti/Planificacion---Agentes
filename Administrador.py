from Materia import Materia
import random

class Administrador:

    #El agente Administrador es el que se encarga de definir que materias se habilitaran en que momento y con cuantos cupos
    """Este agente esta basado en Modelos:
        Tenemos un modelo Interno el cual representa la lista de Materias, su semestre
        la cantidad de cupos habilitados por materia y los creditos que cuesta la materia
        Tambien tiene: Una lista de cupos momentaneos, estos son menores que los cupos reales y mientras existan cupos reales habilitados
        El agente Administrador debe rellenar esos cupos momentaneos
     """


    def __init__(self):
        self.activo = True
        # Estas son las materias
        self.listaMaterias = [Materia('Algebra I', 1, 8, 2), Materia('Fisica I', 1, 7, 3),
                              Materia('Intro a la Progra', 1, 7, 3), Materia('Calculo I', 1, 9, 3),
                              Materia('Elementos', 2, 7, 5), Materia('Arq de Computadores', 2, 15, 2),
                              Materia('Calculo II', 2, 9, 4), Materia('Matematica Discreta', 2, 14, 2),
                              Materia('Taller de Programacion', 3, 10, 6), Materia('Logica', 3, 5, 7),
                              Materia('Teoria de Grafos', 3, 15, 4), Materia('Taller de Bajo Nivel', 3, 8, 7),
                              Materia('Sistemas Operativos', 4, 8, 5), Materia('Base de Datos', 4, 15, 4),
                              Materia('Estaditica', 4, 10, 3), Materia('Investigacion Operativa', 4, 14, 3),
                              Materia('Taller de BD', 5, 10, 7), Materia('Ing de Software', 5, 5, 10),
                              Materia('Simulacion de Sis', 5, 15, 7), Materia('Inteligencia Artificial', 5, 12, 8),
                              Materia('Taller Ing Software', 6, 5, 15), Materia('Redes', 6, 8, 9),
                              Materia('Robotica', 6, 7, 20), Materia('Problemas NP', 6, 10, 15),
                              ]
        # El agente Administrador puede habilitar de forma aleatoria las materias
        self.desordenarArreglo(self.listaMaterias)
        # El administrador decide los cupos iniciales, para que los alumnos comiencen a inscribirse
        self.cuposActuales = [random.randint(1, 3) for n in range(24)]



    #Cuando los cupos de las materias se terminen es cuando el agente Administrador debe rellenar estos cupos
    #Esta sera su unica accion, entonces debe realizar una busqueda de aquellas materias para las cuales aun hay cupo disponible
    def rellenarCupos(self):
        #El agente va a revisar los cupos actuales existentes
        for i in range(len(self.cuposActuales)):
            if self.cuposActuales[i] == 0:
                if self.listaMaterias[i].cuposHabilitados > 0:
                    #Nos aseguramos que no se den tantos cupos, para poder controlar
                    num = random.randint(0,self.listaMaterias[i].cuposHabilitados)
                    self.cuposActuales[i] = self.cuposActuales[i] + num
                    print("\nAgente Administrador ha rellenado con " + str(num) + "cupos a la materia " + self.listaMaterias[i].nombre)
                else:
                    print("\nCupos agotados")


    def desordenarArreglo(self,lista):
        random.shuffle(lista)

g = Administrador()
g.rellenarCupos()
print(str(g.cuposActuales))