from recettes.models import Recettes, RecetteCategory


recettes_category_all = RecetteCategory(title='All')


def get_category_and_recettes(recettecategory_title):
    recette = Recettes.objects.filter(catrecette=True)

    if recettecategory_title == recettes_category_all.slug:
        category = recettes_category_all

    else:
        try:
            category = RecetteCategory.objects.get(title__iexact=recettecategory_title)
        except RecetteCategory.DoesNotExit:
            category = RecetteCategory(title=recettecategory_title)
            recette = Recettes.objects.none()

    
    return category, recette