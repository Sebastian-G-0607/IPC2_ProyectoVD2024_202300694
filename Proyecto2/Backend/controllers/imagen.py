import os
import xml.etree.ElementTree as ET

from flask import Blueprint, request, jsonify
from model.pixel import Pixel
from model.imagen_modelo import Imagen_M
from model.Matriz_dispersa.Matriz_dispersa import MatrizDispersa

Imagen = Blueprint('imagenes', __name__)

@Imagen.route('/imagenes/carga/<string:id_usuario>', methods=['POST'])
def cargaImagen(id_usuario):
    
    lista_imagenes = leerXML_Imagenes()

    try:
        xml_entrada = request.data.decode('utf-8')
        if xml_entrada == '':
            return jsonify({
                'message': 'Archivo vacío',
                'status': 400
            }), 400

        root = ET.fromstring(xml_entrada)
        matriz_imagen = MatrizDispersa()
        nombre = ''
        pixeles = []
        id = len(lista_imagenes) + 1
        for hijo in root:
            if hijo.tag == 'nombre':
                nombre = hijo.text
            elif hijo.tag == 'diseño':
                for pixel in hijo:
                    fila = int(pixel.attrib['fila'])
                    columna = int(pixel.attrib['col'])
                    color = pixel.text
                    matriz_imagen.insertar(fila,columna,color)
                    nuevo_pixel = Pixel(fila,columna,color)
                    pixeles.append(nuevo_pixel)
        nueva_imagen = Imagen_M(id, id_usuario, nombre, pixeles, matriz_imagen.graficar())
        lista_imagenes.append(nueva_imagen)
        crearXML(lista_imagenes)
        crearXMLbase64(leerXML_base64(), nueva_imagen)

        return jsonify({
            'message': 'Imagen cargada correctamente',
            'matriz': nueva_imagen.base_64,
            'status': 200
            }), 200
    
    except:
        return jsonify({
            'message': 'Error al cargar la imagen',
            'status': 404
        }), 404
    
@Imagen.route('/imagenes', methods=['GET'])
def listar_imagenes():
    try:
        #se lee el archivo de la base de datos
        tree = ET.parse('database/base64.xml')
        root = tree.getroot()
        #se crea una lista que va a almacenar diccionarios con las imágenes
        lista_base64 = []
        '''
        {
            "id": id de la imagen, 
            "nombre": nombre de la imagen, 
            "id_usuario": id del usuario que cargó o editó la imagen,
            "imagen": base 64 de la imagen
        }
        '''

        for imagen in root:
            id = imagen.attrib['id']
            id_usuario = imagen.attrib['id_usuario']
            nombre = ''
            base_64 = ''
            for atrib in imagen:
                if atrib.tag == 'nombre':
                    nombre = atrib.text
                elif atrib.tag == 'base64':
                    base_64 = atrib.text
            lista_base64.append({"id": id, "nombre": nombre, "id_usuario": id_usuario, "imagen": base_64})

        return jsonify({
            "imagenes": lista_base64,
            "status": 200
        })
    except:
        return jsonify({
            'message': 'Internal server error',
            'status': 500
        }), 500

@Imagen.route('/imagenes/editar/<string:id_usuario>', methods=['POST'])
def editarImagen(id_usuario):
    lista_imagenes = leerXML_Imagenes()

    '''
    JSON DE ENTRADA
    {
        'id': id de la imagen,
        'filtro': 1 para escala de grises/2 para tonalidad sepia
    }
    '''

    id = int(request.json['id'])
    filtro = int(request.json['filtro'])
    imagenActual = None

    for imagen in lista_imagenes:
        if imagen.id == id:
            imagenActual = imagen
            break

    if imagenActual is None:
        return jsonify({
            'mensaje':'Imagen no encontrada',
            'status':404
            }),404
    
    nuevos_pixeles = []
    matriz1 = MatrizDispersa()
    matriz2 = MatrizDispersa()
    nombre_editado = ''
    for pixel in imagenActual.pixeles:
        pixel:Pixel
        matriz1.insertar(pixel.fila, pixel.columna, pixel.color)

        if filtro == 1:
            rgb_pixel = hexadecimal_a_RGB(pixel.color)
            rgb_escala_grises = RGB_a_escalaGrises(rgb_pixel)
            nuevo_color = RGB_a_hexadecimal(rgb_escala_grises)
            matriz2.insertar(pixel.fila, pixel.columna, nuevo_color)
            nuevo_pixel = Pixel(pixel.fila, pixel.columna, nuevo_color)
            nuevos_pixeles.append(nuevo_pixel)
            nombre_editado = ' - Escala de grises'
        elif filtro == 2:
            rgb_pixel = hexadecimal_a_RGB(pixel.color)
            rgb_sepia = RGB_a_sepia(rgb_pixel)
            nuevo_color = RGB_a_hexadecimal(rgb_sepia)
            matriz2.insertar(pixel.fila, pixel.columna, nuevo_color)
            nuevo_pixel = Pixel(pixel.fila, pixel.columna, nuevo_color)
            nuevos_pixeles.append(nuevo_pixel)
            nombre_editado = ' - Tonalidad Sepia'
    
    id = len(lista_imagenes) + 1
    nueva_imagen = Imagen_M(id,id_usuario, imagenActual.nombre + nombre_editado, nuevos_pixeles)
    nueva_imagen.editado = True
    nueva_imagen.base_64 = matriz2.graficar()
    lista_imagenes.append(nueva_imagen)
    crearXML(lista_imagenes)
    crearXMLbase64(leerXML_base64(), nueva_imagen)

    return jsonify({
        'mensaje': 'Imagen editada correctamente',
        'matriz1': matriz1.graficar(),
        'matriz2': nueva_imagen.base_64,
        'status': 201
    }), 201

def hexadecimal_a_RGB(hex_color):
    hex_color = hex_color.lstrip('#')
    red = int(hex_color[0:2], 16)
    green = int(hex_color[2:4], 16)
    blue = int(hex_color[4:6], 16)

    return (red, green, blue)

def RGB_a_escalaGrises(rgb_color):

    red, green, blue = rgb_color

    gris = 0.2989*red + 0.5870*green + 0.1140*blue

    gris = round(gris)

    return (gris, gris, gris)

def RGB_a_sepia(rgb_color):

    red,green, blue = rgb_color

    new_red = 0.393*red + 0.769*green + 0.189*blue
    new_green = 0.349*red + 0.686*green + 0.168*blue
    new_blue = 0.272*red + 0.534*green + 0.131*blue

    new_red = round(new_red)
    new_green = round(new_green)
    new_blue = round(new_blue)

    return (new_red, new_green, new_blue)

def RGB_a_hexadecimal(rgb_color):

    return "#{:02X}{:02X}{:02X}".format(rgb_color[0], rgb_color[1], rgb_color[2])

def crearXML(imagenes):
    if os.path.exists('database/imagenes.xml'):
        os.remove('database/imagenes.xml')

    tree = ET.Element('imagenes')
    for imagen in imagenes:
        editado = 0
        if imagen.editado == True:
            editado = 1
        imagen_xml = ET.SubElement(tree, 'imagen', id=str(imagen.id), id_usuario=str(imagen.id_usuario), editado=str(editado))
        nombre_xml = ET.SubElement(imagen_xml, 'nombre')
        nombre_xml.text = imagen.nombre
        disenio_xml = ET.SubElement(imagen_xml, 'diseño')
        for pixel in imagen.pixeles:
            pixel:Pixel
            pixel_xml = ET.SubElement(disenio_xml, 'pixel', fila=str(pixel.fila), col=str(pixel.columna))
            pixel_xml.text = pixel.color
    
    tree = ET.ElementTree(tree)

    ET.indent(tree, space='\t', level=0)

    tree.write('database/imagenes.xml', encoding='utf-8', xml_declaration=True)

def crearXMLbase64(lista_imagenes, nueva_imagen): #se le pasa como parámetro la lista de objetos imágenes
    #Se agrega la nueva imagen a la lista
    lista_imagenes.append(nueva_imagen)
    #se crea el árbol
    tree = ET.Element('imagenes')
    for imagen in lista_imagenes:
        imagen: Imagen_M
        imagen_64 = ET.SubElement(tree, 'imagen', id=str(imagen.id), id_usuario=str(imagen.id_usuario))
        nombre_64 = ET.SubElement(imagen_64, 'nombre')
        nombre_64.text = imagen.nombre
        texto_base64 = ET.SubElement(imagen_64, 'base64')
        texto_base64.text = imagen.base_64

    tree = ET.ElementTree(tree)

    ET.indent(tree, space='\t', level=0)

    tree.write('database/base64.xml', encoding='utf-8', xml_declaration=True)


def leerXML_base64():
    if not os.path.exists('database/base64.xml'):
        return []
    
    #creamos una lista de imagenes
    imagenes = []

    tree = ET.parse('database/base64.xml')
    root = tree.getroot()
    for imagen in root:
        id = int(imagen.attrib['id'])
        id_usuario = imagen.attrib['id_usuario']
        nombre = ''
        base_64 = ''
        for atributo in imagen:
            if atributo.tag == 'nombre':
                nombre = atributo.text
            elif atributo.tag == 'base64':
                base_64 = atributo.text
        
        nueva_imagen = Imagen_M(id,id_usuario, nombre, None, base_64)
        imagenes.append(nueva_imagen)
    
    return imagenes   

def leerXML_Imagenes():
    if not os.path.exists('database/imagenes.xml'):
        return []
    
    #creamos una lista de imagenes
    imagenes = []

    tree = ET.parse('database/imagenes.xml')
    root = tree.getroot()
    for imagen in root:
        id = int(imagen.attrib['id'])
        id_usuario = imagen.attrib['id_usuario']
        editado = imagen.attrib['editado']
        if editado == '1':
            editado = True
        elif editado == '0':
            editado = False
        nombre = ''
        pixeles = []
        for hijo in imagen:
            if hijo.tag == 'nombre':
                nombre = hijo.text
            elif hijo.tag == 'diseño':
                for pixel in hijo:
                    fila = int(pixel.attrib['fila'])
                    columna = int(pixel.attrib['col'])
                    color = pixel.text
                    nuevo_pixel = Pixel(fila,columna,color)
                    pixeles.append(nuevo_pixel)
        
        nueva_imagen = Imagen_M(id,id_usuario, nombre, pixeles)
        nueva_imagen.editado = editado
        imagenes.append(nueva_imagen)
    
    return imagenes