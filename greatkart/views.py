from django.views.generic.base import TemplateView
from store.models import Product
from accounts.models import AccessLocation



class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):


        # pega o ip da pessoa e salva algumas informações
        try:
            ip = self.request.META.get('REMOTE_ADDR')
            AccessLocation.addAccess(ip)
        except:
            pass
        #

        context = super(HomeView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.all().filter(is_available=True)
        return context


