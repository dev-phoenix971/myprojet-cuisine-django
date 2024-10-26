from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from tinymce.compressor import gzip_compressor
from recettes.models import RecetteCategory, Recettes
from django.db.models import Q
from django.db.models import Count
import json
import random


def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    recette = Recettes.objects.filter(
        Q(catrecette__id__icontains=q) |
        Q(name__icontains=q) |
        Q(ingredients__icontains=q)
    )
    recette = Recettes.objects.all()
    
    all_recette =list(Recettes.objects.all())
    recent_recettes = random.sample(all_recette,4)

    category = RecetteCategory.objects.all()

    context = {'recette': recette, 'category': category, 'recent_recettes': recent_recettes,}
    return render(request, "index.html", context)


def flatpages_link_list(request):
    """
    Returns a HttpResponse whose content is a Javascript file representing a
    list of links to flatpages.
    """
    from django.contrib.flatpages.models import FlatPage

    link_list = [(page.title, page.url) for page in FlatPage.objects.all()]
    return render_to_link_list(link_list)


def compressor(request):
    """
    Returns a GZip-compressed response.
    """
    return gzip_compressor(request)


def render_to_link_list(link_list):
    """
    Returns a HttpResponse whose content is a Javascript file representing a
    list of links suitable for use wit the TinyMCE external_link_list_url
    configuration option. The link_list parameter must be a list of 2-tuples.
    """
    return render_to_js_vardef("tinyMCELinkList", link_list)


def render_to_image_list(image_list):
    """
    Returns a HttpResponse whose content is a Javascript file representing a
    list of images suitable for use wit the TinyMCE external_image_list_url
    configuration option. The image_list parameter must be a list of 2-tuples.
    """
    return render_to_js_vardef("tinyMCEImageList", image_list)


def render_to_js_vardef(var_name, var_value):
    output = f"var {var_name} = {json.dumps(var_value)};"
    return HttpResponse(output, content_type="application/x-javascript")


def filebrowser(request):
    try:
        fb_url = request.build_absolute_uri(reverse("fb_browse"))
    except Exception:
        fb_url = request.build_absolute_uri(reverse("filebrowser:fb_browse"))

    return render(
        request,
        "tinymce/filebrowser.js",
        {"fb_url": fb_url},
        content_type="application/javascript",
    )