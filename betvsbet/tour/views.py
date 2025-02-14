
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from betvsbet.tour.utils import DataMixin

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
    if request.method == 'POST':
         
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'tour/about.html',
                  {'title': 'О сайте', 'menu': menu, 'form': form})


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

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Tour.published.filter(cat_id=category.pk).select_related('cat')
    data = {
        'title': f'Вид спорта: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
        }
    return render(request, 'tour/index.html', data)


class TourCategory(DataMixin, ListView):
    template_name = 'tour/index.html'
    context_object_name ='posts'
    allow_empty = False
    
    def get_queryset(self):
        return Tour.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        
        context['cat_selected'] = cat.pk
        return context
    
    


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class TagPostList(ListView):
    template_name = 'tour/index.html'
    context_object_name ='posts'
    allow_empty = False
      
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Тег:' + tag.tag
        context['menu'] = menu
        context['cat_selected'] = None
        return context
    
    def get_queryset(self):
        return Tour.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')
