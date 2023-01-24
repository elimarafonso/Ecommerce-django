from django.views.generic.base import TemplateView
from store.models import Product, Category


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.all().filter(is_available=True)
        return context


