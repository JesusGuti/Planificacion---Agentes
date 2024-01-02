import random
import threading
import time
from Cajero import Cajero
from Administrador import Administrador
from Director import Director

#Los estudiantes son independientes el uno del otro y por tanto
class Estudiante(threading.Thread):
    #Agente Estudiante es un Agente Basado en Utilidad y En objetivos
    global caj,adm,d
    reglasEst = {'no-inscrito' : 'comprar-matricula','inscrito' : 'habilitar-cuenta','habilitado' : 'inscribirse','inhabilitado' : 'dar-listaDir'}
    #El agente Estudiante tiene los distintos atributos
    def __init__(self,nombre, codSis, semestre, dineroDis,retraso,materiasTomadas,numeroMaterias,caje,admi,di):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.nombre = nombre
        self.codSis = codSis
        #Es importante el semestre de cada Agente, por que este definira que criterios debe tener el agente
        """Por razones obvias el agente no seleccionara materias demasiado avanzadas a su nivel, 
           pero si puede tomar materias que debe de semestres anteriores"""
        self.semestre = semestre
        self.dineroSis = dineroDis
        self.codigoMat = ''
        #El atributo tiempo lo definira el Agente Director este valor de tiempo va desde 20 a 60 min
        self.tiempo = None
        self.materiasElegidas = []
        self.retraso = retraso
        self.materiasTomadas = materiasTomadas
        self.numeroMaterias = numeroMaterias
        #El agente tiene un Estado Inicial el cual es no inscrito
        self.estado = 'no-inscrito'
        #El agente tiene un conjunto de acciones
        self.ultimaAccion = None
        #El agente interactua con los otros Agentes
        self.caj = caje
        self.adm = admi
        self.d = di

######################################################################################################################################################
    #Tendremos varios Agentes Estudiantes
    #Define el comportamiento del hilo: En este caso el Agente Estudiante
    def run(self):
        #Si el estudiante no esta inscrito
        if self.estado == 'no-inscrito':
            print('\nEl Agente Estudiante: ' + self.nombre +' está yendo al cajero...')
            #El Agente Estudiante debe esperar a que el cajero termine de atender a otros Agentes
            while(self.caj.estado == "EstudiantePaga" or self.caj.estado == "AlumnoAtendido"):
                    print("\nAgente Estudiante "+ self.nombre + " Esperando en cola de Cajero")
                    time.sleep(3)
            #Cuando le toca el turno al Agente compra su matricula
            print("\nAgente Cajero está atendiendo a " + self.nombre)
            print("\nAgente Cajero cobra 20 Bs de los " + str(self.dineroSis) + " disponibles del Agente Estudiante " + self.nombre)
            if self.actuar('no-inscrito',self.caj,self.adm,self.d,self.adm.listaMaterias,self.adm.cuposActuales):
                print("\n" + self.nombre +" obtuvo el codigo: "+self.codigoMat + " del Agente Cajero")

                #Una vez inscrito el agente debe ser habilitado por el Agente Director"""
                if self.estado == 'inscrito':
                    print(self.nombre + " está "+ self.estado +"(a)")
                    print('\nEstudiante: ' + self.nombre + ' VA donde el director para ser habilitado para la Inscripcion...')
                    #El agente Estudiante debe esperar a ser habilitado por el Director
                    while (self.d.estado == "Estudiante-Termina" or self.d.estado == "Ocupado"):
                        print("\n" + self.nombre + " Esperando a Director para ser habilitado")
                        time.sleep(3)
                    print("\nAgente Director está atendiendo a " + self.nombre)
                    #Una vez que este libre, el agente debe hablar con el Director
                    if self.actuar('inscrito',self.caj,self.adm,self.d,self.adm.listaMaterias,self.adm.cuposActuales):
                        #Si el agente esta Habilitado, ya se le asigno el tiempo que puede realiza la busqueda
                        self.estado == 'habilitado'
                        print("\nEl agente Estudiante: " + self.nombre +" está " +self.estado + " para la inscripcion")
                        if self.estado == 'habilitado':
                            #print("\nEl agente Estudiante: " + self.nombre + " tiene habilitadas las siguientes materias:" + "\n" + str(self.adm.listaMaterias))
                            self.actuar('habilitado',self.caj,self.adm,self.d,self.adm.listaMaterias,self.adm.cuposActuales)

                            #Una vez concluido el proceso de inscripicion, ya sea por que logro su objetivo o por falta de tiempo
                            if self.estado == 'inhabilitado':
                                #El agente Estudiante debe pasar la lista de materias a las cuales se inscribio al Agente Director
                                self.actuar('inhabilitado', self.caj, self.adm, self.d, self.adm.listaMaterias,self.adm.cuposActuales)

                                print("\n" + self.nombre + " se ha inscrito a: " + str(self.materiasElegidas))
                        else:
                            print("\nNo puede inscribirse para: " + self.nombre)
                            self.stop()
                    else:
                        print("\nSe acaba el proceso de Inscripcion para: " + self.nombre)
                        self.stop()
            else:
                print("\nSe acaba el proceso de Inscripcion para: " + self.nombre )
                self.stop()

########################################################################################################################################

    def actuar(self, percepcion,caj,adm,dir,lm,lc):
        #Si la percepcion no es valida el agente Estudiante devuelve una acción nula
        if not percepcion:
            return 'Error'
        if percepcion in self.reglasEst.keys():
            if percepcion == 'no-inscrito':
                return self.solicitarMatricula(caj)

            elif percepcion == 'inscrito':
                return self.hablarDirector(dir,caj.habilitados)

            elif percepcion == 'habilitado':
                self.buscarMateria(lm, lc, adm)
                return self.reglasEst[percepcion]

            elif percepcion == 'inhabilitado':
                self.entregarLista(dir)
                return self.reglasEst[percepcion]
        return ' '

    #Para comenzar su plan el agente debe solicitar Matricula al Agente Cajero
    def solicitarMatricula(self,caj):
        #El agente Estudiante solicita al cajero la matricula para inscripcion
        #caj.devolver(self)
        if caj.actuar(self,'AlumnoSolicita'):
            time.sleep(3)
            caj.actuar(self,'EstudiantePaga')
            self.estado = 'inscrito'
            return True
        else:
            caj.estado = 'AlumnoSolicita'

    #Para comenzar con su inscripcion el agente debe hablar con el Director
    def hablarDirector(self,dir,lista):
        #El agente Estudiante debe hablar con el Director para comenzar con la inscripcion
        if dir.habilitarEst(self,lista):
            self.estado = 'habilitado'
            time.sleep(3)
            dir.estado = 'Estudiante-Solicita'
            return True
        else:
            return False

    #El agente Estudiante una vez pagada su matricula debe comenzar a buscar sus materias
    def buscarMateria(self,listaMat,listaCupos,adm):
        if self.estado == 'habilitado':
            #Mientras al agente aun no se le acabe el tiempo y aun no alcanzo el numero de materias a las cuales quiere inscribirse
            while self.numeroMaterias > 0 and self.tiempo > 0:
                #Una vez comenzado el tiempo de inscripcion el agente estudiante debe comenzar a buscar las materias ofrecidas por el agente Administrador
                for mat in listaMat:
                    if self.numeroMaterias > 0 and  self.tiempo > 0:
                        #Si el agente Estudiante debe materias puede tomar materias inferiores al del semestre actual
                        if self.retraso == True:
                            #El agente puede tomar materias que no haya aprobado ya
                            if mat.semestre == self.semestre or mat.semestre == self.semestre+1 or mat.semestre < self.semestre:
                                #El agente debe evitar las materias ya aprobadas y escogidas
                                if mat.nombre not in self.materiasTomadas and \
                                   mat.nombre not in self.materiasElegidas:

                                    #Una vez vista la materia adecuada el agente intenta ver si hay cupos y si el dinero le alcanza para inscribirse
                                    if listaCupos[listaMat.index(mat)] > 0 and self.dineroSis >= mat.creditos:
                                        self.materiasElegidas.append(mat.nombre)
                                        mat.cuposHabilitados = mat.cuposHabilitados - 1
                                        listaCupos[listaMat.index(mat)] = listaCupos[listaMat.index(mat)] - 1
                                        #Inscribirse a una materia cuesta creditos(Definidos en la clase materia) y tiempo
                                        self.dineroSis = self.dineroSis - mat.creditos
                                        self.tiempo = self.tiempo -  random.randint(4,7) #Un valor de tiempo randomico
                                        self.numeroMaterias = self.numeroMaterias - 1
                                        print(self.nombre + " se inscribio a " + mat.nombre + " con Bs. " + str(mat.creditos) + " y quedan " + str(mat.cuposHabilitados) + " cupos restantes" +
                                              "\n al Agente Estudiante " + self.nombre + " le quedan " + str(self.tiempo) + " minutos, " + str(self.dineroSis) + " Bs y " + str(self.numeroMaterias) + " materias a tomar en esta inscripcion")
                                    else:
                                        #Cuando el Agente Estudiante debe saltar de materia por que ya no hay cupos
                                        #Esto alerta al agente Administrador que debe rellenar los cupos por materia
                                        print("\n De momento no hay cupos para: " + mat.nombre + " para el Agente "+ self.nombre)
                                        print("\nAgente Administrador rellenara cupos espere un momento.................")
                                        adm.rellenarCupos()
                                        #El agente pierde el tiempo por buscar
                                        self.tiempo = self.tiempo - random.randint(4, 7)  # Un valor de tiempo randomico
                                        print('\nBuscar otra materia puede ser mejor opcion ' + self.nombre + " tiempo restante " + str(self.tiempo))
                                else:
                                    print("\nLa Materia "  + mat.nombre + " ya aprobada " + self.nombre)
                            else:
                                #Materia ocupada
                                #El agente pierde el tiempo por buscar
                                self.tiempo = self.tiempo - random.randint(1, 2)  # Un valor de tiempo randomico
                                print("\nLa materia" + mat.nombre + " no está habilitada para usted " + self.nombre +  " ,tiempo restante " + str(self.tiempo))
                        else:
                            if mat.semestre == self.semestre or mat.semestre == self.semestre+1:
                                # El agente debe evitar las materias ya aprobadas
                                if mat.nombre not in self.materiasTomadas and \
                                   mat.nombre not in self.materiasElegidas:
                                    # Una vez vista la materia adecuada el agente intenta ver si hay cupos
                                    if listaCupos[listaMat.index(mat)] > 0:
                                        self.materiasElegidas.append(mat.nombre)
                                        mat.cuposHabilitados = mat.cuposHabilitados - 1
                                        listaCupos[listaMat.index(mat)] = listaCupos[listaMat.index(mat)] - 1
                                        # Inscribirse a una materia cuesta creditos(Definidos en la clase materia) y tiempo
                                        self.dineroSis = self.dineroSis - mat.creditos
                                        self.tiempo = self.tiempo - random.randint(4, 7)  # Un valor de tiempo randomico
                                        self.numeroMaterias = self.numeroMaterias - 1
                                        print("\n" + self.nombre + " se inscribio a " + mat.nombre + " con Bs. " + str(mat.creditos) + " y quedan " + str(mat.cuposHabilitados) + " cupos restantes"+
                                              "\n al Agente Estudiante " + self.nombre + " le quedan " + str(self.tiempo) +" minutos, " +str(self.dineroSis) + " Bs y " + str(self.numeroMaterias) + " materias a tomar en esta inscripcion" )

                                    else:
                                        #El agente pierde el tiempo en buscar cupo
                                        self.tiempo = self.tiempo - random.randint(1, 2)  # Un valor de tiempo randomico
                                        print('\nBuscar otra materia seria mejor opcion ' + self.nombre + " , tiempo restante " + str(self.tiempo))
                                else:
                                    print("\nLa materia " + mat.nombre +  " ya fue aprobada " + self.nombre)
                            else:
                                self.tiempo = self.tiempo - random.randint(1, 2)  # Un valor de tiempo randomico
                                print("\nLa Materia " +mat.nombre + " no está disponible para usted " + self.nombre + " ,tiempo restante "+ str(self.tiempo))

                #Una vez que se acabo su tiempo o logro inscribirse a la cantidad de materias deseada
                #El Agente Estudiante pasa al Estado Inhabilitado
                self.estado = 'inhabilitado'
                print(self.nombre + ", se acabo su proceso de inscripcion por favor pase sus materias al Agente Director")
        else:
            print('El estudiante: '+ self.nombre + 'no está habilitado para inscribirse')

    #El agente debe buscar las materias ya aprobadas, para evitarlas
    def buscarAprobadas(self,nomMat,lista):
        res = False
        if lista != None:
            for l in lista:
                if l.nombre == nomMat:
                    res = True
            return res
        else:
            return res

    #El agente Estudiante debe entregar, la lista de materias
    def entregarLista(self,dir):
        dir.solicitarMateriasEst(self)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

c = Cajero()
a = Administrador()
d = Director()
print("Las materias que esta ofreciendo el Departamento de Informatica y Sistemas este semestre son: \n")
time.sleep(1)
for j in range(len(a.listaMaterias)):
    time.sleep(1)
    print("\n"+a.listaMaterias[j].nombre + " a partir de " + str(a.listaMaterias[j].semestre) + " semestre con " + str(a.listaMaterias[j].cuposHabilitados) + " cupos habilitados al costo de " + str(a.listaMaterias[j].creditos))
time.sleep(7)
print("\n----------------------------------------------------------------------------------------------------------------------------------------")
print("\n¡¡¡¡¡¡¡¡¡¡¡¡¡Comienza la PLANIFICACION!!!!!!!!!!!!!!!!!!!")
c = Cajero()
print("\nAgente Cajero a la escucha")
a = Administrador()
print("\nAgente Administrador a la escucha")
d = Director()
print("\nAgente Director a la escucha")


e1 = Estudiante('Pepito',14532,2,100,True,['Algebra I','Intro a la Progra','Fisica I'],4,c,a,d)
e2 = Estudiante('Carla',233456,4,70,False,['Algebra I','Intro a la Progra','Fisica I','Calculo I','Elementos', 'Arq de Computadores',
'Calculo II', 'Matematica Discreta', 'Taller de Programacion','Logica', 'Teoria de Grafos', 'Taller de Bajo Nivel'],5,c,a,d)
e3 = Estudiante('Julian',12432,1,150,False,[],6,c,a,d)
e4 = Estudiante('Paola',145630,1,10,False,[],2,c,a,d)
e5 = Estudiante('Marcos',99982,1,30,False,[],2,c,a,d)
e6 = Estudiante('Leonel',56743,1,70,False,[],4,c,a,d)
e7 = Estudiante('Adriana',9896473,1,150,False,[],5,c,a,d)
e8 = Estudiante('Evelin',76423,1,300,False,[],7,c,a,d)
e9 = Estudiante('Teresa',43276,1,50,False,[],4,c,a,d)
e10 = Estudiante('Cristobal',145630,3,50,True,['Calculo I', 'Matematica Discreta','Logica'],2,c,a,d)
e11 = Estudiante('Amanda',64582,1,30,False,[],2,c,a,d)
e12 = Estudiante('Katherine',43238,4,70,False,['Algebra I','Intro a la Progra','Fisica I','Calculo I','Elementos',
'Calculo II', 'Matematica Discreta', 'Taller de Bajo Nivel'],4,c,a,d)
e13 = Estudiante('Rodrigo',95321,1,150,False,[],5,c,a,d)
e14 = Estudiante('Pablo',14652,1,300,False,[],7,c,a,d)
e15 = Estudiante('Leticia',789432,1,9,False,[],7,c,a,d)

time.sleep(5)
print("\nAqui vienen los estudiantes!!!!!!!!!!!!!!!!!!!!!!!")
time.sleep(2)
print("\n")
e1.start()
e2.start()
e3.start()
e4.start()
e5.start()
e6.start()
e7.start()
e8.start()
e9.start()
e10.start()
e11.start()
e12.start()
e13.start()
e14.start()
e15.start()

e1.join()
e2.join()
e3.join()
e4.join()
e5.join()
e6.join()
e7.join()
e8.join()
e9.join()
e10.join()
e11.join()
e12.join()
e13.join()
e14.join()
e15.join()

time.sleep(5)
print("\nUna vez acabada la PLANIFICACION el Agente Director posee el siguiente registro de Alumnos Inscritos y sus materias:")
for k in d.registro:
    print(str(k))

print("\nGracias por ver")
