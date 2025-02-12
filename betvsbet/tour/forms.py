from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError

from .models import Category, Tour


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789-"
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел"
        
    def __call__(self, value, *args, **kwds):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)

"""class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255,min_length=7,
                            label="Название турнира",
                            widget=forms.TextInput(attrs={'class': 'form-input'}),
                            error_messages={
                                'min_length': 'Сликом короткое название',
                                'required': 'Введите название турнира',
                            })
    slug = forms.SlugField(max_length=255, label="URL",
                           validators=[
                               MinLengthValidator(7, message='Минимум 7 символов'),
                               MaxLengthValidator(100)                               
                           ])
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label="Контент")
    is_published = forms.BooleanField(required=False, initial=True, label="Статус")
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),empty_label="Категория не выбрана", label="Категории")
    
    def clean_title(self):
        title = self.cleaned_data['title']
        ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789-"
        
        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError("Должны присутствовать только русские символы, дефис и пробел")"""
        

class AddPostForm(forms.ModelForm):        
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),empty_label="Категория не выбрана", label="Категории")
    
    class Meta:
        model = Tour
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels = {'slug': 'URL'}
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError("Длина больше 50 символов") 
        
        return title
    
    
class UploadFileForm(forms.Form):
    file = forms.ImageField(label='Файл')