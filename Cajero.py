import random
import string
import time

#El agente Cajero es un Agente Reactivo Simple:
"""El agente Cajero la unica accion que realiza es devolver un codigo de matricula a un estudiante"""
class Cajero:
    reglas = {"AlumnoSolicita":"CobrarAlumno",
              "EstudiantePaga":"DevolverCodigo",
               "AlumnoAtendido":"AñadirLista"
             }
    #Estos son los alumnos que pagaron y por ende son habilitados
    habilitados = []

    def __init__(self):
        self.activo = True
        self.estado = "AlumnoSolicita"

    #Para actuar el Agente Cajero, necesita una percepcion que le de un Estudiante
    def actuar(self,es,percepcion):
        if not percepcion:
            return ' '
        if percepcion in self.reglas.keys():
            if percepcion == 'AlumnoSolicita':
               return self.cobrar(es)

            elif percepcion == 'EstudiantePaga':
                self.devolver(es)
                return self.reglas[percepcion]
            else:
                self.addCodigo(self.habilitados,es)
                return self.reglas[percepcion]
        return ' '

    #El agente Cajero puede cobrar al estudiante
    def cobrar(self,es):
        self.estado = "EstudiantePaga"
        # El agente Cajero pregunta si el estudiante no es nulo
        if es.codSis != None:
            # Si en caso no lo es se debe reducir la cantidad de dinero del estudiante
            if es.dineroSis >= 20:
                es.dineroSis = es.dineroSis - 20
                return True
            else:
                print("\n" + es.nombre + " no cuenta con suficiente dinero")
                return False
    #El agente Cajero puede devolver codigo
    def devolver(self,es):
        #El agente Cajero pregunta si el estudiante no es nulo
        if es.codSis != None:
            #Se le devuelve el codigo para la matricula
            es.codigoMat = self.get_random_string(10)
            self.estado = "AlumnoAtendido"
            # Añadimos al estudiante a la lista de habilitados
            self.habilitados.append(es)
            self.estado = "AlumnoSolicita"

        else:
            print('Error de Estudiante')

    #Este metodo nos sirve para generar codigos
    def get_random_string(self,longitud):
        #Escoger de todas las letras un conjunto
        letras = string.ascii_lowercase
        result_str = ''.join(random.choice(letras) for i in range(longitud))
        return result_str

