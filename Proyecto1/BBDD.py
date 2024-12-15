from Artistas.Lista_simple_artistas import Lista_artistas
from Solicitantes.Lista_doble_solicitantes import Lista_solicitantes
from Cola_de_solicitudes.Cola_solicitudes import Cola_solicitudes

class BBDD:
    usuario_en_sesion = ''
    listaArtistas = Lista_artistas()
    listaSolicitantes = Lista_solicitantes()
    colaSolicitudes = Cola_solicitudes()
