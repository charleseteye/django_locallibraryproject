from django.shortcuts import render
from .models import Book,Author,BookInstance,Genre
from django.views import generic

# Create your views here.

def index(request):
    """
    View function for home page of site.
    """
    #Generate counts for home page of site
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()
    num_genres=Genre.objects.count()  # The 'all()' is implied by default.
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'catalog/index.html',
        context={'num_books':num_books,
                 'num_genres':num_genres,
                 'num_instances':num_instances,
                 'num_instances_available':num_instances_available,
                 'num_authors':num_authors},
    )
    
class BookListView(generic.ListView):
    model=Book
    template_name = 'catalog/book_list.html'
      # Specify your own template name/location
    paginate_by=5

class BookDetailView(generic.DetailView):
    model=Book
    template_name = 'catalog/book_detail.html' 
    
class AuthorListView(generic.ListView):
    model=Author
    template_name = 'catalog/author_list.html'
      # Specify your own template name/location
    paginate_by=5

class AuthorDetailView(generic.DetailView):
    model=Author
    template_name = 'catalog/author_detail.html' 
       
    
