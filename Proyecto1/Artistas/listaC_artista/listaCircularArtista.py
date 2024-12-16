import os

from Artistas.listaC_artista.nodo_circular import Nodo

class ListaCircular:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamanio = 0

    def __len__(self):
        return self.tamanio
    
    def insertar(self, valor):
        nuevo = Nodo(valor)
        if self.primero == None and self.ultimo == None:
            self.primero = nuevo
            self.ultimo = nuevo
            self.ultimo.siguiente = self.primero
        else:
            self.ultimo.siguiente = nuevo
            self.ultimo = nuevo
            self.ultimo.siguiente = self.primero
        self.tamanio+=1

    def mostrar(self):
        contador = 0
        actual = self.primero
        while contador < self.tamanio:
            print(actual.valor)
            actual = actual.siguiente
            contador+=1
    
    def obtenerValor(self, id):
        contador = 0
        actual = self.primero
        while contador < self.tamanio:
            if actual.valor.id == id:
                return actual.valor
            actual = actual.siguiente
            contador+=1
        return None

    def graficar(self, id_logueado):
        codigo_dot = ''

        codigo_dot += '''digraph G {
    rankdir=LR;
    node[shape=record, height=.1]
'''
        contador_nodos = 0
        actual = self.primero
        while contador_nodos < self.tamanio:
            codigo_dot += 'nodo'+str(contador_nodos)+'[label=\"{'+str(actual.valor)+'|<f1>}\"];\n'
            actual = actual.siguiente
            contador_nodos+=1
        
        actual = self.primero
        contador_nodos = 0
        while contador_nodos < self.tamanio-1:
            codigo_dot += 'nodo'+str(contador_nodos)+' -> nodo'+str(contador_nodos+1)+';\n'
            actual = actual.siguiente
            contador_nodos+=1
        
        codigo_dot += 'nodo'+str(self.tamanio-1)+ ' -> nodo0[constraint=false];\n'

        codigo_dot += '}'

        ruta_dot = 'Proyecto1/codigosdot/Procesadas_' + id_logueado + '.dot'
        archivo = open(ruta_dot, 'w')
        archivo.write(codigo_dot)
        archivo.close()

        ruta_imagen = "Proyecto1/Reportes/Procesadas_" + id_logueado + '.png'

        comando = 'dot -Tpng '+ ruta_dot + ' -o ' + ruta_imagen
        os.system(comando)

        ruta_imagensvg = "Proyecto1/Reportes/Procesadas_" + id_logueado + '.svg'

        comandosvg = 'dot -Tsvg '+ ruta_dot + ' -o ' + ruta_imagensvg

        os.system(comandosvg)

        abrir_svg = os.path.abspath(ruta_imagensvg)
        os.startfile(abrir_svg)