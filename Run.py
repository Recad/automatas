import sys
from main import *
from poblacion import *
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import threading

#Calse encargada del menejo grafico de la aplicación
class formulario(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.my_arraysp1 = []
        self.my_arraysp2 = []
        self.my_arraysp3 = []
        self.ui.pushButton.clicked.connect(self.lanzar)

        self.IndiceP1=self.ui.ind_pobla1.value()
        self.IndiceP2=self.ui.ind_pobla2.value()
        self.IndiceP3=self.ui.ind_pobla3.value()

    #Valida los datos de entrada
    def ValidarDatos(self):
        self.IndiceP1 = self.ui.ind_pobla1.value()
        self.IndiceP2 = self.ui.ind_pobla2.value()
        self.IndiceP3 = self.ui.ind_pobla3.value()

        self.IndicePropa1 = self.ui.ind_propa1.value()
        self.IndicePropa2 = self.ui.ind_propa2.value()
        self.IndicePropa3 = self.ui.ind_propa3.value()

        self.IndiceViaje1 =  self.ui.Indi_viaje1.value()
        self.IndiceViaje2 = self.ui.Indi_viaje2.value()
        self.IndiceViaje3 = self.ui.Indi_viaje3.value()

        self.Vistas = self.ui.spinVista.value()
        self.iteraciones = self.ui.spinIte.value()

        self.muertes = self.ui.spinMuerte.value()



        if ( (self.IndiceP1 > 0.0 and self.IndiceP2>0.0 and self.IndiceP3>0.0)
            and (self.IndicePropa1 > 0.0 and self.IndicePropa2>0.0 and self.IndicePropa3>0.0)
                and (self.IndiceViaje1 > 0.0 and self.IndiceViaje1>0.0 and self.IndiceViaje1>0.0)):

            if (self.Vistas >= (self.iteraciones)) or (self.muertes > self.iteraciones):
                return False

            else:
                return True
        else:
            return False

    #TRanforma un indice dado por el usuario en una probabilidd del sistema
    def DefProbabilidades(self, percentil):

        return math.floor((1/percentil)*100)

    #lanza la app
    def lanzar(self):

        if self.ValidarDatos():

            self.poblaci = Poblacion(True, "población 1")
            self.poblaci2 = Poblacion(False, "población 2")
            self.poblaci3 = Poblacion(False, "población 3")
            self.poblaci.poblar(self.DefProbabilidades(self.IndiceP1))
            self.poblaci2.poblar(self.DefProbabilidades(self.IndiceP2))
            self.poblaci3.poblar(self.DefProbabilidades(self.IndiceP3))
            self.poblaci.infectarIndividuo()
            self.ui.salidas.setText("")
            self.ui.salidas.setText("se han creado 3 poblaciones:!\n"+
                                    "poblacion 1 con un tamaño de:" + str(self.poblaci.numFilas) + " x " + str(
                self.poblaci.numColumnas) + "\n"+"poblacion 2 con un tamaño de:" + str(self.poblaci2.numFilas) +
                                    " x " + str(self.poblaci2.numColumnas) + "\n"+"poblacion 3 con un tamaño de:" +
                                    str(self.poblaci3.numFilas) + " x " + str(self.poblaci3.numColumnas) + "\n"+"simulacion terminada...:!\n")

            self.iterar()

            self.ImprimirMat(self.poblaci.name,self.my_arraysp1)
            self.ImprimirMat(self.poblaci2.name, self.my_arraysp2)
            self.ImprimirMat(self.poblaci3.name, self.my_arraysp3)


            self.LimpiarMats()
        else:
            self.ui.salidas.setText("")
            self.ui.salidas.setText("Error en los indices!\n las iteraciones deben ser mayores que las vistas")

    #realiza las acciones de las iteraciones
    def iterar(self):
        for i in range(0, self.iteraciones):
            #INicio de las iteraciones de movimiento
            self.poblaci.realizarIteracionMovimiento()
            self.poblaci2.realizarIteracionMovimiento()
            self.poblaci3.realizarIteracionMovimiento()
            #-----------------------------------------------------------------------------------------------------------



            #Inicio de la propagación
            self.poblaci.PropagacionVirus(self.DefProbabilidades(self.IndicePropa1))
            self.poblaci2.PropagacionVirus(self.DefProbabilidades(self.IndicePropa2))
            self.poblaci3.PropagacionVirus(self.DefProbabilidades(self.IndicePropa3))
            #-----------------------------------------------------------------------------------------------------------

            # Liminacion de muertos de las poblaciones
            if (self.muertes > 0):
                self.poblaci.eliminarMuertos(self.muertes)
                self.poblaci2.eliminarMuertos(self.muertes)
                self.poblaci3.eliminarMuertos(self.muertes)
            # -----------------------------------------------------------------------------------------------------------


            #Inicio de los posibles viajes entre poblaciones
            #Poblacion origen entregando viajeros
            self.poblaci2.recibirIndividuo(self.poblaci.EntregarIndividuo(self.DefProbabilidades(self.IndiceViaje1)))
            self.poblaci3.recibirIndividuo(self.poblaci.EntregarIndividuo(self.DefProbabilidades(self.IndiceViaje1)))
            #Poblacion 2 entregando viajeros
            #self.poblaci.recibirIndividuo(self.poblaci2.EntregarIndividuo(self.DefProbabilidades(self.IndiceViaje2)))
            self.poblaci3.recibirIndividuo(self.poblaci2.EntregarIndividuo(self.DefProbabilidades(self.IndiceViaje2)))
            #Poablación 3 entregando individuos
            self.poblaci2.recibirIndividuo(self.poblaci3.EntregarIndividuo(self.DefProbabilidades(self.IndiceViaje3)))
            #self.poblaci.recibirIndividuo(self.poblaci3.EntregarIndividuo(self.DefProbabilidades(self.IndiceViaje3)))

            if i % self.Vistas == 0:

                self.my_arraysp1.append(self.poblaci.PrintMatNice())
                self.my_arraysp2.append(self.poblaci2.PrintMatNice())
                self.my_arraysp3.append(self.poblaci3.PrintMatNice())

    #Limpia las matrices
    def LimpiarMats(self):
        self.my_arraysp1 = []
        self.my_arraysp2 = []
        self.my_arraysp3 = []

    #IMprime las matrices
    def ImprimirMat(self,name,array):


        cmap = ListedColormap(['White', 'Blue', 'Red'])
        contador = 0

        if len (array) % 2 != 0:
            array.append(array[len(array) - 1])

        if (len(array)==2):
            vali = 1
            valj = 2
            valori, valorj = vali, valj
            f, axarr = plt.subplots(valj, vali)

            f.subplots_adjust(hspace=0.4, wspace=0.4)
            for j in range(2):

                for i in range(valori):

                    axarr[j].set_title("T :" + str(contador * self.Vistas + self.Vistas))
                    axarr[j].imshow(array[contador], cmap=cmap, interpolation='nearest', vmin=0, vmax=2)

                    contador += 1

        else:
            vali = len(array) // 2
            valj = 2

            valori, valorj = vali, valj
            f, axarr = plt.subplots(valj, vali)

            f.subplots_adjust(hspace=0.4, wspace=0.4)
            for j in range(2):

                for i in range(valori):

                    axarr[j, i].set_title("T :" + str(contador * self.Vistas + self.Vistas))
                    axarr[j, i].imshow(array[contador], cmap=cmap, interpolation='nearest', vmin=0, vmax=2)

                    contador += 1


        manager = plt.get_current_fig_manager()
        manager.resize(*manager.window.maxsize())


        plt.savefig('Resultado ' + name + '.png')
        manager.canvas.set_window_title(name)
        plt.show()





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    myapp = formulario()
    myapp.show()
    sys.exit(app.exec_())

