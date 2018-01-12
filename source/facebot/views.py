from django.views.generic.list import ListView
from django.views.generic import TemplateView

from facebot.models import FacePage, TimelineImage, PagePost


class Homepage(TemplateView):
    """
    Homepage with about text
    """

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        page = FacePage.objects.first()
        context = super().get_context_data(**kwargs)
        context['name'] = page.page_name
        context['page'] = page

        return context


class Album(ListView):
    """
    Paginated list of post images
    """

    model = TimelineImage
    context_object_name = 'photos'
    template_name = 'album.html'
    paginate_by = 24
    ordering = '-created_time'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = FacePage.objects.first().page_name

        return context


class PostList(ListView):
    """
    Paginated list of posts
    """

    model = PagePost
    template_name = 'post_list.html'
    paginate_by = 10
    context_object_name = 'post_list'
    ordering = '-created_time'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = FacePage.objects.first().page_name

        return context
