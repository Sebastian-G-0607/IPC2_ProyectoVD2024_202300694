import json
from django.shortcuts import render, redirect
import requests
from .forms import LoginForm, XMLForm
from django.http import HttpResponse

# Create your views here.

endpoint = "http://localhost:3000/"

global_c = {
    'contenido-xml': None,
    'binario': None
}

def login(request):
    return render(request, 'login.html')

def admin(request):
    return render(request, 'admin.html')

def adminCarga(request):
    return render(request, 'admin-carga.html')

def user(request):
    return render(request, 'user.html')

def IniciarSesion(request):
    try:
        if request.method == 'POST':
            info = LoginForm(request.POST)
            if info.is_valid():
                username = info.cleaned_data['username']
                password = info.cleaned_data['password']

                data = {
                    'user': username,
                    'password': password
                }

                json_data = json.dumps(data)
                headers = { 'Content-Type': 'application/json' }
                url = endpoint + 'login'
                response = requests.post(url, json_data, headers=headers)
                response_json = response.json()
                
                rol = int(response_json['rol'])
                aceptado = bool(response_json['accepted'])

                if rol == 1 and aceptado == True:
                    redireccion = redirect('admin')
                    redireccion.set_cookie('username', username)
                    return redireccion
                elif rol == 2 and aceptado == True:
                    redireccion = redirect('user')
                    redireccion.set_cookie('username', username)
                    return redireccion
                elif rol == 0 and aceptado == False:
                    return render(request, 'login.html')
                
            return render(request, 'login.html')
    except:
        return render(request, 'login.html')
    
def cargarXML(request):
    ctx = {
        'contenido': None
    }
    try:
        if request.method == 'POST':
            print(request.POST)
            print("*****")
            print(request.FILES)
            form = XMLForm(request.POST, request.FILES)
            print(form)
            if form.is_valid():
                archivo = request.FILES['archivo']
                xml = archivo.read()
                xml_decodificado = xml.decode('utf-8')
                global_c['binario'] = xml
                global_c['contenido-xml'] = xml_decodificado
                ctx['contenido'] = xml_decodificado
                return render(request, 'admin-carga.html', ctx)
            else:
                return render(request, 'admin-carga.html')
    except:
        return render(request, 'carga.html')
    
def enviarXML(request):
    try:
        if request.method == 'POST':
            xml = global_c['binario']
            if xml is None:
                return render(request, 'carga.html')
            url = endpoint + 'admin/cargarUsuarios'
            response = requests.post(url, data=xml)
            respuesta = response.json()
            print(respuesta)
            global_c['binario_xml'] = None
            global_c['contenido_archivo'] = None
            return render(request, 'admin-carga.html')
    except:
        return render(request, 'carga.html')
    
def adminVerUsuarios(request):
    ctx = {
        'usuarios': None
    }
    url = endpoint + 'usuarios'
    response = requests.get(url)
    data = response.json()
    ctx['usuarios'] = data['users']
    return render(request, 'admin-ver-usuarios.html', ctx)

def adminVerXML(request):
    ctx = {
        'usuarios': None
    }
    print("hola")
    url = endpoint + 'usuarios/xml'
    response = requests.get(url)
    print(response)
    data = response.json()
    print(data)
    # ctx['usuarios'] = data['usuarios']
    return render(request, 'admin-ver-xml.html', ctx)
