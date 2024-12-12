import os
from Artistas.nodo_simple import nodo_simple

class Lista_artistas:
    def __init__(self):
        self.primero = None
        self.tamanio = 0

    def __len__(self):
        return self.tamanio
    
    def insertar(self, dato):
        nuevoNodo = nodo_simple(dato)
        if self.primero == None:
            self.primero = nuevoNodo
            self.tamanio+=1
        else:
            actual = self.primero
            while actual != None:
                if actual.dato.id == nuevoNodo.dato.id:
                    return
                if actual.siguiente == None:
                    actual.siguiente = nuevoNodo
                    self.tamanio+=1
                    break
                actual = actual.siguiente

    def buscar(self, valor):
        actual = self.primero
        while actual != None:
            if actual.dato.id == valor:
                return actual.dato
            actual = actual.siguiente
        return None
    
    def recorrer(self):
        actual = self.primero
        while actual != None:
            print(str(actual.dato))
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
            codigo_graphviz += 'nodo' + str(numero_nodo) + '[label=\"{' + str(actual.dato) + '|<f1>}\"];\n'
            numero_nodo+=1
            actual = actual.siguiente

        actual = self.primero
        numero_nodo = 1
        while actual.siguiente != None:
            codigo_graphviz += 'nodo' + str(numero_nodo) + ' -> nodo' + str(numero_nodo + 1) + ';\n'
            numero_nodo+=1
            actual = actual.siguiente
        
        codigo_graphviz += '}'

        ruta_archivo_dot = "Proyecto1/codigosdot/ListaArtistas.dot"

        archivo_dot = open(ruta_archivo_dot,'w')
        archivo_dot.write(codigo_graphviz)
        archivo_dot.close()

        ruta_imagen = "Proyecto1/Reportes/ListaArtistas.png"

        comando = 'dot -Tpng '+ ruta_archivo_dot + ' -o ' + ruta_imagen
        os.system(comando)

        ruta_imagensvg = "Proyecto1/Reportes/ListaArtistas.svg"

        comandosvg = 'dot -Tsvg '+ ruta_archivo_dot + ' -o ' + ruta_imagensvg

        os.system(comandosvg)

        abrir_svg = os.path.abspath(ruta_imagensvg)
        os.startfile(abrir_svg)



