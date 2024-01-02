from Estudiante import Estudiante
from Cajero import Cajero
from Administrador import Administrador
from Director import Director

"""PLANIFICACION DE INSCRIPCION DE UN ESTUDIANTE A LA FCYT ()
    Lo primero que haremos será crear a los Agentes Cajero, Director y Administrador
    Estos 3 agentes estaran a la espera
    El Agente Cajero y el Agente Director estan a la Espera de que llegue un Agente Estudiante 
"""
c = Cajero()
d = Director()
a = Administrador()

"""La creacion de los Agentes tipo Estudiante es independiente, pero para el plan a seguir dependen de los otros agentes
    Un estudiante tiene un nombre, su codigo sis, el semestre en el que se encuentra, si esta retrasado en algunas materias    
    Tiene unas materias aprobadas, y el numero de materias 
"""
e1 = Estudiante('Pepito',14532,2,100,True,['Algebra I','Intro a la Progra','Fisica I'],4)
e2 = Estudiante('Carla',233456,4,70,False,['Algebra I','Intro a la Progra','Fisica I','Calculo I','Elementos', 'Arq de Computadores',
'Calculo II', 'Matematica Discreta', 'Taller de Programacion','Logica', 'Teoria de Grafos', 'Taller de Bajo Nivel'],5)
e3 = Estudiante('Julian',12432,1,150,False,[],6)
e4 = Estudiante('Paola',145630,1,50,False,[],2)
e5 = Estudiante('Marcos',99982,1,30,False,[],2)
e6 = Estudiante('Leonel',56743,1,70,False,[],4)
e7 = Estudiante('Adriana',9896473,1,150,False,[],5)
e8 = Estudiante('Evelin',76423,1,300,False,[],7)
e9 = Estudiante('Teresa',43276,1,50,False,[],4)
e10 = Estudiante('Cristobal',145630,3,50,True,['Calculo I', 'Matematica Discreta','Logica'],2)
e11 = Estudiante('Amanda',64582,1,30,False,[],2)
e12 = Estudiante('Katherine',43238,4,70,False,['Algebra I','Intro a la Progra','Fisica I','Calculo I','Elementos',
'Calculo II', 'Matematica Discreta', 'Taller de Bajo Nivel'],4)
e13 = Estudiante('Rodrigo',95321,1,150,False,[],5)
e14 = Estudiante('Pablo',14652,1,300,False,[],7)




listaMaterias = a.listaMaterias
listaCupos = a.cuposActuales

