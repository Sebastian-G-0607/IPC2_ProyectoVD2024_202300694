import os
from Solicitantes.pila.nodo_pila_solicitante import nodo_pila_solicitante

class pila_solicitante:
    def __init__(self):
        self.cima = None
        self.tamanio = 0

    def __len__(self):
        return self.tamanio

    def push(self, dato):
        nuevoNodo = nodo_pila_solicitante(dato)
        if self.cima == None:
            self.cima = nuevoNodo
        else:
            nuevoNodo.siguiente = self.cima
            self.cima = nuevoNodo
        self.tamanio+=1
    
    def pop(self):
        if self.cima == None:
            return None
        else:
            eliminado = self.cima.dato
            self.cima = self.cima.siguiente
            self.tamanio-=1
            return eliminado
        
    def graficar(self, id_logueado):
        codigo_dot = ''
        codigo_dot += '''digraph G {
    rankdir=LR;
    node[shape=Mrecord];
    '''
        codigo_dot += 'Pila[xlabel=\"Pila\" label=\"'
        actual = self.cima
        while actual != None:
            if actual.siguiente != None:
                codigo_dot += str(actual.dato) + '|'
            else:
                codigo_dot += str(actual.dato)
            actual = actual.siguiente
        codigo_dot += '\"];\n'
        codigo_dot += '}'

        ruta_dot = "Proyecto1/codigosdot/Pila_" + id_logueado +  ".dot"

        archivo = open(ruta_dot,'w')
        archivo.write(codigo_dot)
        archivo.close()

        ruta_imagen = "Proyecto1/Reportes/Pila_" + id_logueado + '.png'

        comando = 'dot -Tpng '+ ruta_dot + ' -o ' + ruta_imagen
        os.system(comando)

        ruta_imagensvg = "Proyecto1/Reportes/Pila_" + id_logueado + '.svg'

        comandosvg = 'dot -Tsvg '+ ruta_dot + ' -o ' + ruta_imagensvg

        os.system(comandosvg)

        abrir_svg = os.path.abspath(ruta_imagensvg)
        os.startfile(abrir_svg)