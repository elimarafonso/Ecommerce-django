from category.models import Category

# FUNÇÃO QUE MOSTRA O MENU 'CATEGORIAS' E TODOS OS TEMPLATES
# É PRECISO DEFINIR ESTA FUNÃO NO settings.py no PROJETO
# NA ABA TEMPLATES "CONTEXT_PROCESSORS"

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)
