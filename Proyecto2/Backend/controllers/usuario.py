import os
import xml.etree.ElementTree as ET

from flask import Blueprint, request, jsonify
from model.solicitante import Solicitante

Usuario = Blueprint('usuarios', __name__)

@Usuario.route('/admin/cargarUsuarios', methods=['POST'])
def cargarUsuarios():
    usuarios = leerXML()
    try:
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
        lista_usuarios = leerXML()
        tree = ET.Element('solicitantes')
        for usuario in lista_usuarios:
            #2. Creamos un elemento usuario
            usuario_xml = ET.SubElement(tree, 'solicitante', id=usuario.id, pwd=usuario.pwd)
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
            # imagenes = ET.SubElement(usuario_xml, 'imagenes')
        
        ET.indent(tree, space='\t', level=0)
        xml_str = ET.tostring(tree, encoding='utf-8', xml_declaration=True)
        return xml_str
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
