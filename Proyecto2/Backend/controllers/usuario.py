import os
import re
import xml.etree.ElementTree as ET

from flask import Blueprint, request, jsonify
from model.solicitante import Solicitante
from model.imagen_modelo import Imagen_M
from controllers.imagen import	leerXML_Imagenes

Usuario = Blueprint('usuarios', __name__)

@Usuario.route('/admin/cargarUsuarios', methods=['POST'])
def cargarUsuarios():
    usuarios = leerXML()
    try:
        regex_correo = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        regex_id = r'^IPC-\w+$'
        regex_numero = r'^\d{8}$'

        xml_usuarios = request.data.decode('UTF-8')
        if xml_usuarios == '':
            return jsonify({
                'message': 'El archivo XML no es válido', 
                'status': 200
            }), 200
        else:
            root = ET.fromstring(xml_usuarios)
            for usuario in root:
                id = usuario.attrib['id']

                if re.match(regex_id, id) is None:
                    print(id + " - ID no válido")
                    continue

                password = usuario.attrib['pwd']
                if buscarUsuario(usuarios, id):
                    continue
                nombre = ''
                correo = ''
                numero = ''
                direccion = ''
                perfil = ''
                for caracteristica in usuario:
                    match caracteristica.tag:
                        case 'NombreCompleto':
                            nombre = caracteristica.text
                        case 'CorreoElectronico':
                            correo = caracteristica.text
                        case 'NumeroTelefono':
                            numero = caracteristica.text
                        case 'Direccion':
                            direccion = caracteristica.text
                        case 'perfil':
                            perfil = caracteristica.text

                if re.match(regex_correo, correo) is None:
                    print(correo + " - correo no válido")
                    continue

                if re.match(regex_numero, numero) is None:
                    print(numero + " - número no válido")
                    continue

                nuevoUsuario = Solicitante(id, password, nombre, correo, numero, direccion, perfil)
                usuarios.append(nuevoUsuario)

            escribirXML(usuarios)
            return jsonify({
                "document": "Read",
                "status": 200
            }), 200
    except:
        return jsonify({
            "message": "Internal server error",
            "status": 500
        }), 500
    
@Usuario.route('/usuarios', methods=['GET'])
def getUsuarios():
    retorno = []
    if os.path.exists('database/usuarios.xml'):
        usuarios = leerXML()
        for usuario in usuarios:
            retorno.append({
                'id': usuario.id,
                'nombre': usuario.nombre,
                'correo': usuario.correo,
                'telefono': usuario.telefono,
                'direccion': usuario.direccion,
                'perfil': usuario.perfil
            })
        return jsonify({
            'users': retorno,
            'status': 200
        })
    else:
        return jsonify({
            'users': None,
            'message': "No existen usuarios en el sistema",
            'status': 400
        })
    
@Usuario.route('/usuarios/xml', methods=['GET'])
def getUsuariosXML():
    try:
        lista_imagenes = leerXML_Imagenes()
        lista_usuarios = leerXML()
        tree = ET.Element('solicitantes')

        for usuario in lista_usuarios:
            usuario: Solicitante
            #Recorremos la lista de imágenes y vemos cuáles ha agregado o editado el usuario
            imagenes_usuario = []
            for imagen in lista_imagenes:
                imagen: Imagen_M
                if imagen.id_usuario == usuario.id:
                    imagenes_usuario.append(imagen)

            #2. Creamos un elemento usuario
            usuario_xml = ET.SubElement(tree, 'solicitante', id=usuario.id, pwd=usuario.password)
            #3. Creamos los elementos hijos
            nombre = ET.SubElement(usuario_xml, 'NombreCompleto')
            nombre.text = usuario.nombre
            
            correo = ET.SubElement(usuario_xml, 'CorreoElectronico')
            correo.text = usuario.correo
            telefono = ET.SubElement(usuario_xml, 'NumeroTelefono')
            telefono.text = usuario.telefono
            direccion = ET.SubElement(usuario_xml, 'Direccion')
            direccion.text = usuario.direccion
            perfil = ET.SubElement(usuario_xml, 'perfil')
            perfil.text = usuario.perfil
            
            #lista de imagenes de cada usuario
            imagenes = ET.SubElement(usuario_xml, 'imagenes')

            for imagen_user in imagenes_usuario:
                nueva_imagen = ET.SubElement(imagenes, 'imagen', id=str(imagen_user.id), editado=str(imagen_user.editado))
                nombre = ET.SubElement(nueva_imagen, 'nombre')
                nombre.text = imagen_user.nombre

        ET.indent(tree, space='\t', level=0)
        xml_str = ET.tostring(tree, encoding='UTF-8', xml_declaration=True).decode("UTF-8")
        return jsonify({
            "users": xml_str,
            "status": 200
        }), 200
    except:
        return jsonify({
            "message": "Internal server error",
            "status": 500
        }), 500


@Usuario.route('/login', methods=['POST'])
def login():
    '''
    json de entrada:
    {
        user: id del usuario, 
        password: contraseña del usuario
    }
    '''
    usuarios = leerXML()
    user = request.json['user']
    password = request.json['password']

    if user == 'AdminIPC' and password == 'ARTIPC2':
        return jsonify({
            'accepted': True,
            'rol': 1,
            'status': 200
        }), 200

    if buscarUsuario(usuarios, user, password):
        return jsonify({
            'accepted': True,
            'rol': 2,
            'status': 200
        }), 200
    else:
        return jsonify({
            'accepted': False,
            'rol': 0,
            'status': 400
        }), 400
    
@Usuario.route('/usuarios/estadistica/editadas', methods=['GET'])
def editadas():
    try:
        #se carga la lista de imagenes
        lista_imagenes = leerXML_Imagenes()

        #se crea una lista de diccionarios { "id": id_del_usuario, "cantidad": cantidad_de_imagenes}
        lista_ids_usuarios = []
        #se crea una lista que va a registrar todos los id's que han cargado o editado imágenes
        lista_ids = []
        for imagen in lista_imagenes:
            imagen: Imagen_M
            if imagen.id_usuario in lista_ids: #se verifica que no se repitan los id's
                continue
            else:
                lista_ids.append(imagen.id_usuario)
                lista_ids_usuarios.append({"id": imagen.id_usuario, "cantidad": 0}) #se crea el diccionario con cantidad 0 inicial
            
        for dict in lista_ids_usuarios: #se recorre la lista de diccionarios
            for imagen in lista_imagenes: #se recorre la lista de imágenes para comparar cuantas ha cargado el usuario
                if imagen.id_usuario == dict['id'] and imagen.editado == True: 
                    dict['cantidad'] += 1

        #se crea otra lista en orden descendente según la cantidad de imágenes cargadas
        ordenados = sorted(lista_ids_usuarios, key=lambda x:x['cantidad'], reverse=True)

        return jsonify({
            "top": ordenados, 
            "status": 200
        }), 200
    except:
        return jsonify({
            "status": 500,
            "message": "Internal server error"
        }), 500


@Usuario.route('/usuarios/estadistica/cargadas', methods=['GET'])
def cargadas():
    try:
        #se carga la lista de imagenes
        lista_imagenes = leerXML_Imagenes()

        #se crea una lista de diccionarios { "id": id_del_usuario, "cantidad": cantidad_de_imagenes}
        lista_ids_usuarios = []
        #se crea una lista que va a registrar todos los id's que han cargado o editado imágenes
        lista_ids = []
        for imagen in lista_imagenes:
            imagen: Imagen_M
            if imagen.id_usuario in lista_ids: #se verifica que no se repitan los id's
                continue
            else:
                lista_ids.append(imagen.id_usuario)
                lista_ids_usuarios.append({"id": imagen.id_usuario, "cantidad": 0}) #se crea el diccionario con cantidad 0 inicial
            
        for dict in lista_ids_usuarios: #se recorre la lista de diccionarios
            for imagen in lista_imagenes: #se recorre la lista de imágenes para comparar cuantas ha cargado el usuario
                if imagen.id_usuario == dict['id'] and imagen.editado == False: 
                    dict['cantidad'] += 1

        #se crea otra lista en orden descendente según la cantidad de imágenes cargadas
        ordenados = sorted(lista_ids_usuarios, key=lambda x:x['cantidad'], reverse=True)

        return jsonify({
            "top": ordenados[0:3], 
            "status": 200
        }), 200
    except:
        return jsonify({
            "status": 500,
            "message": "Internal server error"
        }), 500

#FUNCIÓN QUE ESCRIBE LOS DATOS EN EL ARCHIVO XML Y LO GUARDA COMO BASE DE DATOS
def escribirXML(lista_usuarios): #SE LE PASA UNA LISTA, QUE ES LA QUE SE OBTIENE AL CARGAR UN XML CON NUEVOS USUARIOS
    #SI EL ARCHIVO XML EXISTE, SE ELIMINA
    if os.path.exists('database/usuarios.xml'):
        os.remove('database/usuarios.xml')

    #SE CREA LA RAIZ DEL XML QUE SE VA A ESCRIBIR
    root = ET.Element('solicitantes')

    #SE CREAN TODOS LOS USUARIOS
    for usuario in lista_usuarios:
        solicitante = ET.SubElement(root, 'solicitante', id=usuario.id, pwd=usuario.password)

        nombre = ET.SubElement(solicitante, 'NombreCompleto')
        nombre.text = usuario.nombre

        correo = ET.SubElement(solicitante, 'CorreoElectronico')
        correo.text = usuario.correo

        telefono = ET.SubElement(solicitante, 'NumeroTelefono')
        telefono.text = usuario.telefono

        direccion = ET.SubElement(solicitante, 'Direccion')
        direccion.text = usuario.direccion

        perfil = ET.SubElement(solicitante, 'perfil')
        perfil.text = usuario.perfil
    
    #SE CREA EL ARBOL
    root = ET.ElementTree(root)
    ET.indent(root, space='\t', level=0)
    root.write('database/usuarios.xml', encoding='utf-8', xml_declaration=True)

#ESTA FUNCIÓN SIRVE PARA LEER EL ARCHIVO XML DE BASE DE DATOS
def leerXML():
    if not os.path.exists('database/usuarios.xml'):
        return []
    
    lista_usuarios = []
    arbol = ET.parse('database/usuarios.xml')
    raiz = arbol.getroot()
    if raiz.tag == 'solicitantes':
        for usuario in raiz:
            id = usuario.attrib['id']
            password = usuario.attrib['pwd']
            nombre = ''
            correo = ''
            numero = ''
            direccion = ''
            perfil = ''
            for caracteristica in usuario:
                match caracteristica.tag:
                    case 'NombreCompleto':
                        nombre = caracteristica.text
                    case 'CorreoElectronico':
                        correo = caracteristica.text
                    case 'NumeroTelefono':
                        numero = caracteristica.text
                    case 'Direccion':
                        direccion = caracteristica.text
                    case 'perfil':
                        perfil = caracteristica.text
            nuevoUsuario = Solicitante(id, password, nombre, correo, numero, direccion, perfil)
            lista_usuarios.append(nuevoUsuario)
        
        return lista_usuarios

#FUNCIÓN PARA BUSCAR UN USUARIO EN UNA LISTA POR ID O PARA HACER LOGIN
def buscarUsuario(usuarios, id, pwd=None):
    if pwd == None:
        for user in usuarios:
            if user.id == id:
                return True
        return False
    else:
        for user in usuarios:
            if user.id == id and user.password == pwd:
                return True
        return False
