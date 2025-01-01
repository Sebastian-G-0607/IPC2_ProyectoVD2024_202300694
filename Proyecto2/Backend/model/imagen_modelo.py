class Imagen_M:
    def __init__(self, id, id_usuario, nombre, pixeles, base_64=None):
        self.id = id
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.pixeles = pixeles
        self.editado = False
        self.base_64 = base_64
