from django.shortcuts import render
from .models import Autor
# Create your views here.
def index(request):
    """View function for home page of site."""
    count = Autor.objects.all().count()

    context = {
        'autor_count': count,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)