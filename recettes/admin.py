from django.contrib import admin

from recettes.models import RecetteCategory, RecetteCategoryClient, Recettes, RecetteComment, Recettesclients, VideoLike


class RecetteCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "image", "coverImageCat")
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(RecetteCategory, RecetteCategoryAdmin)

class RecetteAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "image", "video", "published", "last_udated", "createdAt", "author", "catrecette",)
    fieldsets = (
        ('Général', {
            
            "fields": ("name", "slug", "author", "catrecette", "coverImage", "tempsprepaAt", "tempscuisAt",
    "image", "imagefondvideo","video", "published", "createdAt"
                
            ),
        }),
        ('Contenu de l\'article', {
            "fields": ("description", "ingredients", "preparation",
                
            ),
        }),
    )
    
    prepopulated_fields = {"slug": ("name",)}

    def apercu_preparation(self, recette):
        text = recette.preparation[:40]
        if len(recette.preparation) > 40:
            return '{}...'.format(text)
        else:
            return text
    
    apercu_preparation.short_description = 'Aperçu de la préparation'
    

admin.site.register(Recettes, RecetteAdmin)


admin.site.register(Recettesclients)


admin.site.register(RecetteCategoryClient)


admin.site.register(RecetteComment)


admin.site.register(VideoLike)