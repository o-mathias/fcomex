from django.shortcuts import render


# Create your views here.

def dash_view(request, template_name="dash.html", **kwargs):
    from . import app

    context = {}

    
    return render(request, template_name=template_name, context=context)
