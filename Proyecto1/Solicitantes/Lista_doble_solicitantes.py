import os
from Solicitantes.nodo import nodo_doble

class Lista_solicitantes:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamanio = 0

    def insertar(self, dato):
        nuevoNodo = nodo_doble(dato)
        if self.primero == None and self.ultimo == None:
            self.primero = nuevoNodo
            self.ultimo = nuevoNodo
            self.tamanio+=1
        else:
            self.ultimo.siguiente = nuevoNodo
            nuevoNodo.anterior = self.ultimo
            self.ultimo = nuevoNodo
            self.tamanio+=1

    def recorrer(self):
        actual = self.primero
        while actual != None:
            print(actual.dato)
            actual = actual.siguiente

    def buscar(self, valor):
        actual = self.primero
        while actual != None:
            if actual.dato.id == valor:
                return actual
            actual = actual.siguiente

    def iniciarSesion(self, user, password):
        actual = self.primero
        while actual != None:
            if user == actual.dato.id and password == actual.dato.password:
                return True
            actual = actual.siguiente
        return False

    def graficar(self):
        codigo_graphviz = ''
        codigo_graphviz += '''digraph G {
            rankdir=LR;
            node[shape=record, height=.1]
            '''
        numero_nodo = 1

        actual = self.primero

        while actual != None:
            codigo_graphviz += 'nodo' + str(numero_nodo) + '[label=\"{<f1>|' + str(actual.dato)+'|<f2>}\"];\n'
            numero_nodo+=1
            actual = actual.siguiente

        actual = self.primero
        contador_nodos = 1

        while actual.siguiente != None:
            codigo_graphviz += 'nodo' + str(contador_nodos) + ':f2 -> nodo' + str(contador_nodos+1) + ':f1;\n'
            codigo_graphviz += 'nodo' + str(contador_nodos+1) + ':f1 -> nodo' + str(contador_nodos) + ':f2;\n'
            contador_nodos+=1
            actual = actual.siguiente
        
        codigo_graphviz += '}'

        ruta_archivo_dot = "Proyecto1/codigosdot/ListaSolicitantes.dot"

        archivo_dot = open(ruta_archivo_dot,'w')
        archivo_dot.write(codigo_graphviz)
        archivo_dot.close()

        ruta_imagen = "Proyecto1/Reportes/ListaSolicitantes.png"

        comando = 'dot -Tpng '+ ruta_archivo_dot + ' -o ' + ruta_imagen
        os.system(comando)

        ruta_imagensvg = "Proyecto1/Reportes/ListaSolicitantes.svg"

        comandosvg = 'dot -Tsvg '+ ruta_archivo_dot + ' -o ' + ruta_imagensvg

        os.system(comandosvg)

        abrir_svg = os.path.abspath(ruta_imagensvg)
        os.startfile(abrir_svg)
