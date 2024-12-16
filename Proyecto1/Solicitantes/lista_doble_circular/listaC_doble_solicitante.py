from Solicitantes.lista_doble_circular.nodo_doble_solicitante import nodo_doble
import os

class Lista_doble_circular:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamanio = 0

    def __len__(self):
        return self.tamanio
    
    def getPrimero(self):
        return self.primero
    
    def insertar(self, dato):
        nuevo = nodo_doble(dato)

        if self.primero == None and self.ultimo == None:
            self.primero = nuevo
            self.ultimo = nuevo
            self.ultimo.siguiente = self.primero
            self.primero.anterior = self.ultimo
        else:
            self.ultimo.siguiente = nuevo
            nuevo.anterior = self.ultimo
            self.ultimo = nuevo
            self.ultimo.siguiente = self.primero
            self.primero.anterior = self.ultimo
        self.tamanio+= 1
    
    def mostrar(self):
        contador = 0
        actual = self.primero
        while contador < self.tamanio:
            print(actual.dato)
            actual = actual.siguiente
            contador+= 1
    
    def obtenerSiguiente(self,id):
        actual = self.primero
        contador = 0
        while contador < self.tamanio:
            if actual.dato.id == id:
                return actual.siguiente.dato
            actual = actual.siguiente
            contador+= 1
    
    def obtenerAnterior(self, id):
        actual = self.primero
        contador = 0
        while contador < self.tamanio:
            if actual.dato.id == id:
                return actual.anterior.dato
            actual = actual.siguiente
            contador+= 1
        
    def graficar(self, id_logueado):
        codigo_dot = ''
        codigo_dot += '''digraph G {
    rankdir=LR;
    node[shape=record, height=.1]
    '''
        actual = self.primero
        numero_nodo = 0
        while numero_nodo < self.tamanio:
            codigo_dot += 'nodo' + str(numero_nodo) + '[label=\"{<f1>|' + str(actual.dato) + '|<f2>}\"];\n'
            actual = actual.siguiente
            numero_nodo+=1

        numero_nodo = 0
        actual = self.primero
        while numero_nodo < self.tamanio-1:
            codigo_dot += 'nodo' + str(numero_nodo) + ':f2 -> nodo' + str(numero_nodo+1) + ':f1[dir=both];\n'
            actual = actual.siguiente
            numero_nodo+=1
        
        codigo_dot += 'nodo0:f1 -> nodo' + str(self.tamanio-1) + ':f2 [dir=both constraint=false];\n'

        codigo_dot += '}'

        ruta_dot = 'Proyecto1/codigosdot/Lista_Doble_' + id_logueado + '.dot'

        archivo = open(ruta_dot,'w')
        archivo.write(codigo_dot)
        archivo.close()

        ruta_imagen = 'Proyecto1/Reportes/Lista_Doble_' + id_logueado + '.png'
        comando = 'dot -Tpng '+ ruta_dot + ' -o '+ ruta_imagen
        os.system(comando)

        ruta_imagensvg = "Proyecto1/Reportes/Lista_Doble_" + id_logueado + '.svg'

        comandosvg = 'dot -Tsvg '+ ruta_dot + ' -o ' + ruta_imagensvg

        os.system(comandosvg)

        abrir_svg = os.path.abspath(ruta_imagensvg)
        os.startfile(abrir_svg)