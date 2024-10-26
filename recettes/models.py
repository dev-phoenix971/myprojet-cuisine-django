from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, time, timedelta
from django.template.defaultfilters import slugify
from django.urls import reverse

User = get_user_model()


class RecetteCategory(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name="Titre")
    slug = models.SlugField(max_length=255, null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to="recettes", default= "defaultcategory.png")
    coverImageCat = models.ImageField(upload_to="recettes", default= "defaultcover.png")

    def __str__(self):
        return self.title

    def __str__(self):
        return self.slug



class Recettes(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Recette")
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    ingredients = models.TextField(blank=True, null=True)
    preparation = models.TextField(blank=True, null=True)
    tempsprepaAt = models.DurationField(default=timedelta())
    tempscuisAt = models.DurationField(default=timedelta())
    coverImage = models.ImageField(upload_to="recettes", default= "defaultcover.png")
    image = models.ImageField(upload_to="recettes", default= "defaultrecette.png")
    imagefondvideo = models.ImageField(upload_to="recettes", default= "defaultfond.jpg")
    video = models.FileField(upload_to="videos", max_length=300, default= "videos/defaultvideo.mp4", verbose_name="Video_recette")
    published = models.BooleanField(default=False, verbose_name="Publié")
    last_udated = models.DateTimeField(auto_now=True)
    createdAt = models.DateField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='recette_author')
    catrecette =  models.ForeignKey(RecetteCategory, on_delete=models.SET_NULL, null=True, blank=True)
    

    class Meta:
        ordering=('-published',)
    
    def __str__(self):
        return self.name

    def __str__(self):
        return self.slug
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class RecetteCategoryClient(models.Model):
    titleclient = models.CharField(max_length=255, unique=True, verbose_name="Titre_client")
    slug = models.SlugField(max_length=255, null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to="recettesclients", default= "defaultcategory.png")
    coverImageCat = models.ImageField(upload_to="recettesclients", default= "defaultcover.png")


    def __str__(self):
        return self.titleclient


    def __str__(self):
        return self.slug


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titleclient)
        super().save(*args, **kwargs)


class Recettesclients(models.Model):
    nameclient = models.CharField(max_length=255, unique=True, verbose_name="Recetteclient")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recetteclient_author')
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    ingredients = models.TextField(blank=True, null=True)
    preparation = models.TextField(blank=True, null=True)
    tempsprepaAt = models.DurationField(default=timedelta())
    tempscuisAt = models.DurationField(default=timedelta())
    coverImage = models.ImageField(upload_to="recettesclients", default= "defaultcover.png")
    image = models.ImageField(upload_to="recettesclients", default= "defaultrecette.png")
    imagefondvideo = models.ImageField(upload_to="recettesclients", default= "defaultfond.jpg")
    video = models.FileField(upload_to="videosclients", max_length=300, default= "videos/defaultvideo.mp4", verbose_name="Video_client")
    published = models.BooleanField(default=False, verbose_name="Publié")
    last_udated = models.DateTimeField(auto_now=True)
    createdAt = models.DateField(blank=True, null=True)
    category =  models.ForeignKey(RecetteCategoryClient, on_delete=models.SET_NULL, null=True, blank=True)
    


    class Meta:
        ordering=('-createdAt',)
    
    def __str__(self):
        return self.nameclient

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('recettes:recettesclient')


    @property
    def author_or_default(self):
        return self.author.username if self.author else "L'auteur inconnu"



class RecetteComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_comment')
    recette = models.ForeignKey(Recettes, on_delete=models.CASCADE, null=True, blank=True, related_name='recette_comment')
    recetteclient = models.ForeignKey(Recettesclients, on_delete=models.CASCADE, null=True, blank=True, related_name='recetteclient_comment')
    comment = models.TextField()
    createdAt = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(blank=True, null=True, default=0)


    class Meta:
        ordering=('-createdAt',)

    def __str__(self):
        return self.comment
    
    def __str__(self):
        return self.rating



class VideoLike(models.Model):
    recette = models.ForeignKey(Recettes, on_delete=models.CASCADE, related_name='liked_recette')
    recetteclient = models.ForeignKey(Recettesclients, on_delete=models.CASCADE, related_name='liked_recetteclient')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liker_recette')