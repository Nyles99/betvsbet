
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from .forms import AddPostForm, UploadFileForm

from .models import Category, Tour, TagPost, UploadFiles

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить турнир", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'},
]





"""def index(request): #HttpRequest
    posts = Tour.published.all().select_related('cat')
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
        }
    return render(request, 'tour/index.html', context=data)"""


# def handle_uploaded_file(f):
#    with open(f"uploads/{f.name}", "wb+") as destination:
#        for chunk in f.chunks():
#            destination.write(chunk)


class TourHome(ListView):
    # model = Tour
    template_name = 'tour/index.html'
    context_object_name = 'posts'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
    }
    
    def get_queryset(self):
        return Tour.published.all().select_related('cat')
    
    
    """template_name = 'tour/index.html'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': Tour.published.all().select_related('cat'),
        'cat_selected': 0,
    }"""
    
    """def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = menu
        context['posts'] = Tour.published.all().select_related('cat')
        context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
        return context"""
    

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


def show_post(request, post_slug):
    post = get_object_or_404(Tour, slug=post_slug)
    
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'post': post,
        'cat_selected': 1,
        }
    
    return render(request, 'tour/post.html', data)

class ShowPost(DetailView):
    # model = Tour
    template_name = 'tour/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        return context
    
    def get_object(self, queryset=None):
        return get_object_or_404(Tour.published, slug=self.kwargs[self.slug_url_kwarg])


#def add_page(request):
#    if request.method == 'POST':    
#        form = AddPostForm(request.POST, request.FILES)
#        if form.is_valid():
#        # print()
#        #    try:
#        #        Tour.objects.create(**form.cleaned_data)
#        #        return redirect('home')
#        #    except:
#        #        form.add_error(None, "Ошибка создания турнира")"""
#            form.save()
#            return redirect('home')
#    else:
#        form = AddPostForm()

#    data = {
#        'menu': menu,
#        'title': 'Добавление турнира',
#        'form': form
        
#    }
#    return render(request, 'tour/addpage.html', data)


class AddPage(View):
    def get(self, request):
        form = AddPostForm()
        data = {
        'menu': menu,
        'title': 'Добавление турнира',
        'form': form
        
        }
        return render(request, 'tour/addpage.html', data)
    
    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        
        data = {
            'menu': menu,
            'title': 'Добавление турнира',
            'form': form
            
        }
        return render(request, 'tour/addpage.html', data)


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


class TourCategory(ListView):
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

# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Tour.Status.PUBLISHED).select_related('cat')
#     
#     data = {
#         'title': f"Тег: {tag.tag}",
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#         }
#     
#     return render(request, 'tour/index.html', data)


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
