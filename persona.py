#! /usr/bin/env python3
import random, math
class Persona(object):
    '''Clase de los automatas celulares'''
    #Es estado es si esta infectados o sanos
    #las posicion dentro de la matrix esta dada por x y y


    def __init__(self, estado,positionx,positiony,muere):
        self.__estado = estado
        self.__positionx = positionx
        self.__positiony = positiony
        self.__muere = muere


    def CambiarEstado(self, nuevoEstado):
        self.__estado=nuevoEstado

    def setMuere(self,muere):
        self.__muere=muere

    def getMuere(self):
        return self.__muere

    def SumMuere(self):
        self.__muere+=1

    def setPositions(self,positionx,positiony):
        self.__positionx = positionx
        self.__positiony = positiony

    def getPositionx(self):

        return self.__positionx

    def getPositiony(self):
        return self.__positiony

    def getEstado(self):
        return self.__estado




