from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator, MaxLengthValidator

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Tour.Status.PUBLISHED)


class Tour(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'
        
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug',
                            validators=[
                               MinLengthValidator(7, message='Минимум 7 символов'),
                               MaxLengthValidator(100)                               
                           ])
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default=None, blank=True, null=True, verbose_name='Фотография')
    content = models.TextField(blank=True, verbose_name='Правила турнира')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), 
                                       default=Status.DRAFT, verbose_name='Статус')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name='Теги')
    
    objects = models.Manager()
    published = PublishedManager()

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = "Турниры"
        verbose_name_plural = "Турниры"
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]
    
    
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Вид спорта')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    
    class Meta:
        verbose_name = "вид спорта"
        verbose_name_plural = "Виды спорта"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})
    

class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    
    def __str__(self):
        return self.tag
    
    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})
    

class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')
    