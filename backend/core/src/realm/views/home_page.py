from django.views.generic import TemplateView


class HomePageTemplateView(TemplateView):
    template_name = 'home/home_page.html'
