from .models import Categoria

def get_ancestors(self):
    """
    Retorna uma lista com todas as categorias ancestrais (pais) da categoria atual.
    """
    ancestors = []
    parent = self.pai
    while parent is not None:
        ancestors.append(parent)
        parent = parent.pai
    return ancestors

def get_descendentes(categoria):
    """
    Retorna uma lista com todas as categorias descendentes (filhas) da categoria atual.
    """
    descendentes = []

    def recursive_get_descendentes(categoria):
        children = Categoria.objects.filter(pai=categoria)
        for child in children:
            descendentes.append(child)
            recursive_get_descendentes(child)

    recursive_get_descendentes(categoria)
    return descendentes

