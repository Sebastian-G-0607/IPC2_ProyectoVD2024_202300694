import os
from Cola_de_solicitudes.nodo import nodo_cola

class Cola_solicitudes:
    def __init__(self):
        self.primero = None
        self.tamanio = 0

    def enqueue(self, dato):
        nuevoNodo = nodo_cola(dato)
        if self.primero == None:
            self.primero = nuevoNodo
        else:
            actual = self.primero
            while actual != None:
                if actual.siguiente == None:
                    actual.siguiente = nuevoNodo
                    break
                actual = actual.siguiente
        self.tamanio+=1

    def dequeue(self):
        if self.primero == None:
            return None
        else:
            eliminado = self.primero.dato
            self.primero = self.primero.siguiente
            self.tamanio-=1
            return eliminado

    def graficar(self):
        codigo_archivo_dot = ''
        codigo_archivo_dot +='''digraph G {
    rankdir="RL";
    label="Cola";
    node[shape=box];
    '''
        numero_nodo = 0
        actual = self.primero
        while actual != None:
            codigo_archivo_dot += 'nodo' + str(numero_nodo) + '[label=\"' + str(actual.dato) + '\"];\n'
            numero_nodo += 1
            actual = actual.siguiente

        numero_nodo = 0
        actual = self.primero
        while actual.siguiente != None:
            codigo_archivo_dot += 'nodo' + str(numero_nodo) + ' -> nodo' + str(numero_nodo+1) + ';\n'
            numero_nodo += 1
            actual = actual.siguiente
        
        codigo_archivo_dot += '}'

        ruta_archivo_dot = "Proyecto1/codigosdot/Cola.dot"
        archivo = open(ruta_archivo_dot,'w')
        archivo.write(codigo_archivo_dot)
        archivo.close()

        ruta_imagen = "Proyecto1/Reportes/Cola.png"

        comando = 'dot -Tpng '+ ruta_archivo_dot + ' -o ' + ruta_imagen
        os.system(comando)

        ruta_imagensvg = "Proyecto1/Reportes/Cola.svg"

        comandosvg = 'dot -Tsvg '+ ruta_archivo_dot + ' -o ' + ruta_imagensvg

        os.system(comandosvg)

        abrir_svg = os.path.abspath(ruta_imagensvg)
        os.startfile(abrir_svg)