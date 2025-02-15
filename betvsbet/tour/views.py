
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView
from django.core.paginator import Paginator

from .utils import DataMixin

from .forms import AddPostForm, UploadFileForm

from .models import Category, Tour, TagPost, UploadFiles


class TourHome(DataMixin, ListView):
    # model = Tour
    template_name = 'tour/index.html'
    context_object_name = 'posts'
    title_page = "Главная страница"
    cat_selected = 0
   
    def get_queryset(self):
        return Tour.published.all().select_related('cat')
    

def about(request):
    contact_list = Tour.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tour/about.html',
                  {'title': 'О сайте', 'page_obj': page_obj})


class ShowPost(DataMixin, DetailView):
    template_name = 'tour/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)
    
    def get_object(self, queryset=None):
        return get_object_or_404(Tour.published, slug=self.kwargs[self.slug_url_kwarg])

        
class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'tour/addpage.html'
    title_page = 'Добавление турнира'
    
    
class UpdatePage(DataMixin, UpdateView):
    
    model = Tour
    fields = ['title', 'content','photo', 'is_published', 'cat']
    template_name = 'tour/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование турнира'
    

def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse(f'Авторизация')


class TourCategory(DataMixin, ListView):
    template_name = 'tour/index.html'
    context_object_name ='posts'
    allow_empty = False
    
    def get_queryset(self):
        return Tour.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.pk,
                                      )     


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class TagPostList(DataMixin, ListView):
    template_name = 'tour/index.html'
    context_object_name ='posts'
    allow_empty = False
      
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title = 'Тег:' + tag.tag)
        
    
    def get_queryset(self):
        return Tour.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')
