from django.shortcuts import get_object_or_404, render
from .models import RecetteCategory, Recettes, RecetteComment, VideoLike
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import CommentForm

import random
from recettes import model_helpers


def recette_category(request, recettecategory_title=model_helpers.recettes_category_all.slug):
        categrecette = RecetteCategory.objects.all()   
        recette = Recettes.objects.all()
        category, recettes = model_helpers.get_category_and_recettes(recettecategory_title)
       
        

        return render(request, "recettes/recettecategory_list.html", {'categrecette': categrecette, 'recette': recette, 'recettes':recettes, 'category':category })



def recettes_list(request, recettecategory_slug=None):
    catrecette = None
    recettecat = RecetteCategory.objects.all()
    recettes = Recettes.objects.all()

    

    if recettecategory_slug:
        catrecette = get_object_or_404(RecetteCategory, slug=recettecategory_slug)
        recettes = recettes.filter(catrecette=catrecette)
        all_recette =list(Recettes.objects.all())
        recent_recettes = random.sample(all_recette,1)



    return render(request, 'recettes/recettes_list.html', {'catrecette': catrecette,
                                                          'recettes': recettes,
                                                          'recettecat': recettecat,
                                                          'recent_recettes': recent_recettes,
                                                          
                                                        })


def recettes_detail(request, recettes_slug):
    recettes = get_object_or_404(Recettes, slug=recettes_slug)
    commentrating = RecetteComment.objects.all()
    ratinglist = [0,1,2,3,4]
    recettes_same_Category = Recettes.objects.filter(catrecette=recettes.catrecette)
    like_recette = Recettes.objects.exclude(slug=recettes_slug)[:2]
    comment_form = CommentForm()

    

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.recette = recettes
            comment.save()
            return HttpResponseRedirect(reverse('recettes:recettesdetail', kwargs={'recettes_slug':recettes_slug}))


    return render(request, 'recettes/recettesdetail_list.html', {'recettes': recettes,
                                                                'recettes_same_Category' : recettes_same_Category,
                                                                'like_recette': like_recette,
                                                                'comment_form': comment_form,
                                                                'commentrating': commentrating,
                                                                'ratinglist': ratinglist,
                                                                })