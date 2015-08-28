
## Integrantes
# Rodrigo Castro 14092
# Hugo Noriega 14097
# Hoja de Trabajo #5

## importacion de librerias
from SimPy.Simulation import *
import simpy
from random import uniform
import random


# Clase ejecucion 
class Ejecucion(Process):
    # Inicializacion de proceso
    # Y cantidad de instrucciones
    
    def __init__(self,id):
        Process.__init__(self)
        self.cantInstrucciones=random.randrange(1,10)
        self.id=id
        
    #Obtiene la ram temporal
        ## Parametro la capacidad que tiene la RAM
    def ramTemporal(self,totalRam): 
        yield put, self, memoriaActual, totalRam

    
   ## PARAMETROS:
	## tiempo procesador= tiempo ejecucion de intruscciones
	## cantidadRAM -- cantidad de RAm solicitada por proceso
	## tiempoLlegada -- llegada de procesos 
    def Procesar(self,cantidadRam, tiempoProcesador,tiempoLlegada):
        # Se calcula tiempo llegado con el intervalo


        
        yield hold,self,tiempoLlegada # Se espera a que sea el tiempo de llegada
        print "%5.1f %s a llegado a estado New, solicita %d ram y  %d instrucciones" %(now(),self.id, cantidadRam, self.cantInstrucciones )
        ## SE consume memoria RAM
        yield get, self, memoriaActual, cantidadRam # Se solicita memoria RAM
        print "%5.1f %s ha ingreasado a estado READY" %(now(),self.id)
                
        while (self.cantInstrucciones > 0): # Este ciclo sigue mientras haya instrucciones
            
             #se solicita espacio en el CPU
            yield request,self,cpuActual
           
            
            if(self.cantInstrucciones < tiempoProcesador): # Si hay menos instrucciones de las que se pueden hacer por unidad de tiempo.
                yield hold,self,0.5 # El tiempo de corrida es menor
                self.cantInstrucciones = 0
            else: # Si no, se espera una unidad de tiempo y se reducen la cantidad de instrucciones.
                yield hold,self,1
                self.cantInstrucciones = self.cantInstrucciones - tiempoProcesador
            yield release,self,cpuActual # Se libera espacio en el CPU

            print "%5.1f %s ha ingresado a estado RUNNING " %(now(),self.id)
            
           
                
            
            
        yield put, self, memoriaActual, cantidadRam # Cuando ya no hay instrucciones, se libera la memoria RAM y se termina el proceso.
        print "%5.1f %s HA SALIDO DE EJECUCION" %(now(),self.id)
        # Se calcula el tiempo que el proceso tardo en ejectarse.
        tiempoTotal = now() - tiempoProcesador
        wt.observe(tiempoTotal) 
        
wt=Monitor()
initialize()
#Variables que definen el funcionamiento del programa.
cantProcesos = 25
cores = 1
totalRam = 100
#Intervalo con el cual llegan instrucciones
interval = 5
tiempoEjecucion = 3 # instrucciones por unidad de tiempo

#Se crean el CPU y la memoria RAM, el primero es una cola y el segundo es un contenedor.
cpuActual=Resource(capacity=cores,qType=FIFO)
memoriaActual=Level(capacity=totalRam)

# Se crea este proceso solo para fijar la cantidad inicial de memoria RAM.
a=Ejecucion(id="Proceso #  "+ str(0))
activate(a,a.ramTemporal(totalRam))



for i in range(cantProcesos):
    e=Ejecucion(id="---Proceso # "+ str(i+1)) # Se crea el proceso con su nombre
    #al activar cada proceso, se indica tiempo para llegar (Araiving)
    #y la cantidad de memoria que necesita (RAM)
    activate(e,e.Procesar(cantidadRam=random.randint(1,10), tiempoProcesador = tiempoEjecucion,tiempoLlegada = random.expovariate(1.0 / interval)))
simulate(until=1000)

# Se obtiene la media y la varianza
print "Tiempo total en el procesador: \tmean = %5.1f, \n\t\tvariance=%2d"%(wt.mean(),wt.var()) 

