import PIL.Image
from django.db import models
from django.contrib.auth import get_user_model
from tinymce import models as tinymce_models
from django.urls import reverse
from django.template.defaultfilters import slugify
from PIL import Image

User = get_user_model()



class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    blog_title = models.CharField(max_length=255, verbose_name="Put a Title")
    slug = models.SlugField(max_length=255, unique=True)
    blog_content = tinymce_models.HTMLField(verbose_name="What is on your mind?")
    blog_image = models.ImageField(upload_to='blog', default= "default.png", verbose_name="Blog_image")
    publish_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False, verbose_name="Publié")
    

    class Meta:
        ordering = ['-publish_date']
        verbose_name = "Article"

    def __str__(self):
        return self.blog_title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
        # img = PIL.Image.open(self.blog_image)
        # width, height = img.size
        # target_width = 600
        # h_coefficient = width/600
        # target_height = height/h_coefficient
        # img = img.resize((int(target_width), int(target_height)), PIL.Image.ANTIALIAS)
        # img.save(self.blog_image.path, quality=100)
        # img.close()
        # self.blog_image.close()

        img = Image.open(self.blog_image.path)
        if img.height > 300 or img.width > 300:
         output_size = (300, 300)
         img.thumbnail(output_size)
         img.save(self.blog_image.path)

    @property
    def author_or_default(self):
        return self.author.username if self.author else "L'auteur inconnu"

    def get_absolute_url(self):
        return reverse('blog:blog_list')
    


class BlogComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_blogcomment')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True, related_name='blog_blogcomment')
    comment = models.TextField()
    createdAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-createdAt']

    def __str__(self):
        return self.comment



class Likes(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='liked_blog')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liker_user')
    