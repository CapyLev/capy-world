from django.views.generic import TemplateView


class LandingPageTemplateView(TemplateView):
    template_name = 'landing_page.html'
