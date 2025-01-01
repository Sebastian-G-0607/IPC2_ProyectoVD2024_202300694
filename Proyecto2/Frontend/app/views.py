import json
from django.shortcuts import render, redirect
import requests
from .forms import LoginForm, XMLForm, TextForm
from django.http import HttpResponse
import plotly.graph_objects as go
import plotly.offline as pyo

# Create your views here.

endpoint = "http://localhost:3000/"

global_c = {
    'contenido-xml': None,
    'binario': None
}

def login(request):
    return render(request, 'login.html')

def cerrarSesion(request):
    response = redirect('login')
    response.delete_cookie('username')
    return response

def admin(request):
    return render(request, 'admin.html')

def adminCarga(request):
    return render(request, 'admin-carga.html')

def adminEstadisticas(request):
    return render(request, 'admin-estadisticas.html')

def user(request):
    return render(request, 'user.html')

def userAyuda(request):
    return render(request, 'user-ayuda.html')

def userCrearImg(request):
    return render(request, 'user-crear-imagen.html')

def userEditarImg(request):
    return render(request, 'user-editar-imagen.html')

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
        return render(request, 'admin-carga.html')
    
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
        return render(request, 'admin-carga.html')
    
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
    url = endpoint + 'usuarios/xml'
    response = requests.get(url)
    data = response.json()
    print(data)
    ctx['usuarios'] = data['users']
    return render(request, 'admin-ver-xml.html', ctx)

def adminVerEstadisticas(request):
    ctx = {
        'plot_div': None,
        'plot_div2': None
    }
    url = endpoint + 'usuarios/estadistica/editadas'
    response = requests.get(url)

    data = response.json()

    usuarios = []
    cantidad_imagenes = []

    for dato in data['top']:
        usuarios.append(dato['id'])
        cantidad_imagenes.append(dato['cantidad'])
    
    trace = go.Bar(
        y=cantidad_imagenes,
        x=usuarios
    )

    layout = go.Layout(
        title='Cantidad de imagenes editadas por usuario',
        xaxis={
            'title': 'Usuarios',
        },
        yaxis={
            'title': 'Cantidad de imagenes',
        }
    )

    fig = go.Figure(data=[trace], layout=layout)
    ctx['plot_div'] = pyo.plot(fig, include_plotlyjs=False, output_type='div')

    #******
    url2 = endpoint + 'usuarios/estadistica/cargadas'
    response2 = requests.get(url2)

    data2 = response2.json()

    usuarios2 = []
    cantidad_imagenes2 = []

    for dato in data2['top']:
        usuarios2.append(dato['id'])
        cantidad_imagenes2.append(dato['cantidad'])
    
    trace2 = go.Bar(
        y=cantidad_imagenes2,
        x=usuarios2
    )

    layout2 = go.Layout(
        title='Cantidad de imagenes cargadas por usuario',
        xaxis={
            'title': 'Usuarios',
        },
        yaxis={
            'title': 'Cantidad de imagenes',
        }
    )

    fig2 = go.Figure(data=[trace2], layout=layout2)
    ctx['plot_div2'] = pyo.plot(fig2, include_plotlyjs=False, output_type='div')

    return render(request, 'admin-estadisticas.html', ctx)

def userCargarXMLImagen(request):
    ctx = {
        'contenido': None
    }
    try:
        if request.method == 'POST':
            form = XMLForm(request.POST, request.FILES)
            if form.is_valid():
                archivo = request.FILES['archivo']
                xml = archivo.read()
                xml_decdificado = xml.decode('utf-8')
                global_c['binario'] = xml
                global_c['contenido-xml'] = xml_decdificado
                ctx['contenido'] = xml_decdificado
                return render(request, 'user-crear-imagen.html', ctx)
    except:
        return render(request, 'user-crear-imagen.html')

def enviarXMLImagen(request):
    ctx = {
        'contenido': None,
        'imagen': None
    }
    try:
        if request.method == 'POST':
            xml = global_c['binario']
            if xml is None:
                return render(request, 'user-crear-imagen.html')
            
            id_user = request.COOKIES.get('username')
            url = endpoint + 'imagenes/carga/'+id_user
            respuesta = requests.post(url, data=xml)
            retorno = respuesta.json()

            ctx['contenido'] = global_c['contenido-xml']
            ctx['imagen'] = retorno['matriz']

            global_c['binario'] = None
            global_c['contenido-xml'] = None
            return render(request, 'user-crear-imagen.html', ctx)
    except:
        return render(request, 'user-crear-imagen.html',ctx)
    
def EditarImagenMatriz(request):
    ctx = {
        'imagen1': None,
        'imagen2': None
    }

    try:
        if request.method == 'POST':
            form = TextForm(request.POST)
            if form.is_valid():
                action = request.POST.get('action')
                textid = form.cleaned_data['textid']
                filtro = 0

                if action == 'grayscale':
                    filtro = 1
                elif action == 'sepia':
                    filtro = 2

                data = {
                    'id': textid,
                    'filtro': filtro
                }

                id_user = request.COOKIES.get('username')
                url = endpoint + 'imagenes/editar/' + id_user
                json_data = json.dumps(data)

                headers = {
                    'Content-Type':'application/json'
                }
                response = requests.post(url, data=json_data, headers=headers)

                respuesta = response.json()

                ctx['imagen1'] = respuesta['matriz1']
                ctx['imagen2'] = respuesta['matriz2']
                return render(request, 'user-editar-imagen.html',ctx)
    except:
        return render(request, 'user-editar-imagen.html')
    
def userVerImagenes(request):
    ctx = {
        'imagenes': None
    }
    url = endpoint + 'imagenes'
    response = requests.get(url)
    data = response.json()
    if data['status'] == 200:
        ctx['imagenes'] = data['imagenes']
        return render(request, 'user-ver-galeria.html', ctx)
    elif data['status'] == 500:
        return render(request, 'user-ver-galeria.html', ctx)
