from django.shortcuts import render

# Create your views here.
def index(request):
    """View function for home page of site."""
    context = {
        'num_books': "num_books",
        'num_instances': "num_instances",
        'num_instances_available': "num_instances_available",
        'num_authors': "num_authors",
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)