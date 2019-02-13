#! /usr/bin/env python3
import random, math
from persona import Persona
import numpy as np


#Clase de la población
class Poblacion(object):
    '''Clase de las pblaciones'''
    numColumnas = 0
    numFilas = 0
    Origen=False

    #Constructor de la clase donde recibe si dicha poblacion es el origen o no de la infección, y su nombre
    def __init__(self, origen,name):
        self.numColumnas = random.randrange(16, 80)
        self.numFilas = random.randrange(16, 70)
        self.Origen=origen
        self.name = name

        self.matriz = []
        for i in range(self.numFilas):
            matAux = [0] * self.numColumnas
            self.matriz.append(matAux)

    #clase que pone la poblacion de forma aleatoria en una matriz
    def poblar(self,indicePoblacion):
        self.habitantes=[]
        m=0

        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[i])):

                dado = random.randint(1, indicePoblacion)
                if dado == math.ceil(indicePoblacion/2):
                    self.matriz[i][j] = Persona(1, i, j,0)
                    self.habitantes.append(self.matriz[i][j])
                    m +=1
                else:
                    self.matriz[i][j] = 0

        #print("se creo una matriz de " + str(len(self.matriz)) + "- " + str(len(self.matriz[i])))

    #Imprime la matriz con los valores de estado
    def PrintMatNice(self):
        MatrixAux = np.zeros(shape=(len(self.matriz), len(self.matriz[self.numFilas - 1])))

        cadena = ''
        for i in range(len(self.matriz)):
            cadena += '['
            for j in range(len(self.matriz[i])):

                if isinstance(self.matriz[i][j], Persona):

                    MatrixAux[i][j] = self.matriz[i][j].getEstado()

                    cadena += '{:>4s}'.format(str(self.matriz[i][j].getEstado()))

                else:
                    cadena += '{:>4s}'.format(str(self.matriz[i][j]))

                    MatrixAux[i][j] = 0

            cadena += ']\n'
        MatrixAux.astype(int)
        return MatrixAux

    #Mueve una persona a una nueva posición
    def moverPersona(self, persona, positionx, positiony):

        if isinstance(persona, Persona) and self.validarMovimiento(positionx, positiony):

            tempx = persona.getPositionx()
            tempy = persona.getPositiony()

            persona.setPositions(positionx, positiony)
            self.matriz[positionx][positiony] = persona
            self.matriz[tempx][tempy] = 0



        else:
            ''''''
    #Valida si una posición es valida
    def validarMovimiento(self, positionx, positiony):

        if (positionx >= 0 and positionx < self.numFilas - 1) and (
                positiony >= 0 and positiony < self.numColumnas - 1):
            if (self.matriz[positionx][positiony] == 0):
                return True
        else:
            return False

    #realiza el cambio de posición, cada elemento tiene una probabilidad de 25% de moverse
    #se podra setear en futuras versiones
    def realizarIteracionMovimiento(self):

        for i in range(len(self.matriz) - 1):

            for j in range(len(self.matriz[i]) - 1):
                dado = random.randint(0, 4)

                if isinstance(self.matriz[i][j], Persona) and dado == 2:

                    valorPersona = self.matriz[i][j]

                    self.moverPersona(self.matriz[i][j], (valorPersona.getPositionx() + random.choice([-1, 1, 0])),
                                      (valorPersona.getPositiony() + random.choice([-1, 1, 0])))
                else:
                    '''pasa'''
    #Infecta el primer individuo de la poblacion
    def infectarIndividuo(self):

        if self.Origen==True:
            self.habitantes[random.randint(0, len(self.habitantes))-1].CambiarEstado(2)

    #entrega un individuo que puede viajar dependiendo de una probabilidad de viaje dadad por el usuario
    def EntregarIndividuo(self,IndiceViaje):

        habitante=None

        dado = random.randint(1, IndiceViaje)
        if dado == math.ceil(IndiceViaje/2) and len(self.habitantes) > 9:
            aviajar = random.randint(0, len(self.habitantes)-1)


            habitante = self.habitantes[aviajar]
            self.matriz[habitante.getPositionx()][habitante.getPositiony()] = 0
            self.habitantes.pop(aviajar)


        return habitante

    #Funcion que gestiona las muertes. esta puede desactivarse desde la interfaz
    def eliminarMuertos(self,TiempoMorir):
        #print("La lista tien tamaño " + str(len(self.habitantes)))
        rangex = len(self.habitantes)-1
        i = 0
        while i < rangex :

            if (self.habitantes[i].getMuere() ==     TiempoMorir) :
                self.matriz[self.habitantes[i].getPositionx()][self.habitantes[i].getPositiony()] = 0
                del self.habitantes[i]
                rangex = len(self.habitantes)-1
            else:
                if self.habitantes[i].getEstado() == 2 :
                    self.matriz[self.habitantes[i].getPositionx()][self.habitantes[i].getPositiony()].SumMuere()
            i+=1

    #Recibe un individuo proveniente de otra población
    def recibirIndividuo(self,individuo):


        if individuo != None and isinstance(individuo, Persona):



            for i in range(len(self.matriz) - 1):
                find = False

                for j in range(len(self.matriz[i]) - 1):


                    if  (self.matriz[i][j] == 0):
                        individuo.setPositions(i,j)
                        self.habitantes.append(individuo)
                        self.matriz[i][j]=individuo
                        #print("se recibio un individuo que se ubicara en: "+str(i)+" , "+str(j))
                        find = True
                        break
                    else:
                        '''pasa'''

                if find==True:
                    break
    #Imprime estado finales
    def ImprimirEstadosFinales(self):

        cadena=''
        for i in range(len(self.habitantes) - 1):
            cadena += '{:>4s}'.format(str(self.habitantes[i].getEstado()))


        print (cadena)

    #Propaga en virus a sus vecino es una vecindad de moore dependiendo de una propabilidad dada por el usurio
    def PropagacionVirus(self, indicePropagacion):

        for i in range(len(self.matriz) - 1):

            for j in range(len(self.matriz[i]) - 1):

                if isinstance(self.matriz[i][j],
                              Persona) and self.matriz[i][j].getEstado() == 2:
                    if isinstance(self.matriz[i + 1][j], Persona) and (i + 1) < self.numFilas and self.matriz[i + 1][
                        j].getEstado() == 1 and (i + 1)>=0:
                        dado = random.randint(1, indicePropagacion)
                        if dado == math.ceil(indicePropagacion/2):
                            self.matriz[i + 1][j].CambiarEstado(2)


                    if isinstance(self.matriz[i][j + 1], Persona) and (j + 1) < self.numColumnas and self.matriz[i][
                        j + 1].getEstado() == 1 and (j + 1)>=0:
                        dado = random.randint(1, indicePropagacion)
                        if dado == math.ceil(indicePropagacion/2):
                            self.matriz[i][j + 1].CambiarEstado(2)

                    if isinstance(self.matriz[i + 1][j + 1], Persona) and (i + 1) < self.numFilas and (
                            j + 1) < self.numColumnas and (i + 1) >= 0 and (j + 1)>=0 and self.matriz[i + 1][j + 1].getEstado() == 1:
                        dado = random.randint(1, indicePropagacion)
                        if dado == math.ceil(indicePropagacion/2):
                            self.matriz[i + 1][j + 1].CambiarEstado(2)


                    if isinstance(self.matriz[i - 1][j], Persona) and (i - 1) < self.numFilas and (i - 1) >= 0 and \
                            self.matriz[i - 1][j].getEstado() == 1:
                        dado = random.randint(1, indicePropagacion)
                        if dado == math.ceil(indicePropagacion/2):
                            self.matriz[i - 1][j].CambiarEstado(2)


                    if isinstance(self.matriz[i][j - 1], Persona) and (j - 1) < self.numColumnas and (j - 1) >= 0 and \
                            self.matriz[i][j - 1].getEstado() == 1:
                        dado = random.randint(1, indicePropagacion)
                        if dado == math.ceil(indicePropagacion/2):
                            self.matriz[i][j - 1].CambiarEstado(2)


                    if isinstance(self.matriz[i - 1][j - 1], Persona) and (i - 1) < self.numFilas and (
                            j - 1) < self.numColumnas and (i - 1) >= 0 and (j - 1) >= 0 and self.matriz[i - 1][j - 1].getEstado() == 1:
                        dado = random.randint(1, indicePropagacion)
                        if dado == math.ceil(indicePropagacion/2):
                            self.matriz[i - 1][j - 1].CambiarEstado(2)


                    if isinstance(self.matriz[i + 1][j - 1], Persona) and (i + 1) >= 0 and (j - 1)>=0 and(i + 1) < self.numFilas and (
                            j - 1) < self.numColumnas and self.matriz[i + 1][j - 1].getEstado() == 1:
                        dado = random.randint(1, indicePropagacion)
                        if dado == math.ceil(indicePropagacion/2):
                            self.matriz[i + 1][j - 1].CambiarEstado(2)


                    if isinstance(self.matriz[i - 1][j + 1], Persona) and (i - 1)>=0 and (j + 1)>=0 and (i - 1) < self.numFilas and (
                            j + 1) < self.numColumnas and self.matriz[i - 1][j + 1].getEstado() == 1:
                        dado = random.randint(1, indicePropagacion)
                        if dado == math.ceil(indicePropagacion/2):
                            self.matriz[i - 1][j + 1].CambiarEstado(2)

                else:
                    '''pasa'''
