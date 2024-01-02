import random
import string

class Estudiante:
    def __init__(self, nombre, codSis, semestre, dineroDis):
        self.nombre = nombre
        self.codSis = codSis
        self.semestre = semestre
        self.dineroSis = dineroDis
        self.codigoMat = ''


#El agente Cajero es un Agente Reactivo Simple
class Cajero:
    def __init__(self,reglas):
        self.activo = True
        self.reglas = reglas
        self.percepciones = ""

    def devolver(self,est):
        "Actua según la percepcion recibida"
        if est != None:
            est.dineroSis = est.dineroSis - 10
            est.codigoMat = self.get_random_string(7)
        else:
            print('Error de Estudiante')

    def get_random_string(self,longitud):
        #Escoger de todas las letras
        letras = string.ascii_lowercase
        result_str = ''.join(random.choice(letras) for i in range(longitud))
        return result_str



