import random

class Director:

    #El Agente Director es un Agente Reactivo Simple
    """El agente requiere de que un estudiante interactue con el """
    reglas = {"Estudiante-Solicita":"Habilitar-Estudiante",
             "Estudiante-Termina" : "Pedir-Lista-Materias"}

    #El Agente Director guarda el registro de las materias a los que los estudiantes se inscriben
    #Todos pasan por este registro
    registro = []
    def __init__(self):
        self.activo = True
        self.estado = 'Estudiante-Solicita'

    def actuar(self,percepcion,est,lista):
        if not percepcion:
            return 'esperar'
        if percepcion in self.reglas.keys():
            if percepcion == "Estudia-Solicita":
                self.habilitarEst(est, lista)
                return self.reglas[percepcion]
            else:
                self.solicitarMateriasEst(est)
                return self.reglas[percepcion]
    #Podemos habilitar al Estudiante
    def habilitarEst(self,est,lista):
        self.estado = 'Ocupado'
        if est.codSis != None and est.codigoMat != None and est in lista:
            #Se define el tiempo que tendra el estudiante para realizar su inscripcion
            est.tiempo = random.randint(20,60)
            return True
        else:
            self.estado = 'Estudiante-Solicita'
            return False
    #Solicitar al estudiante materias escogidas
    def solicitarMateriasEst(self,est):
        self.estado = 'Ocupado'
        informe = {(est.nombre,est.codSis):est.materiasElegidas}
        self.registro.append(informe)
        self.estado = 'Estudia-Solicita'