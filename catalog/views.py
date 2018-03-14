from django.shortcuts import render
from .models import Book,Author,BookInstance,Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

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
    
     # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    

    num_genres=Genre.objects.count()  # The 'all()' is implied by default.
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'catalog/index.html',
        context={'num_books':num_books,
                 'num_visits':num_visits,
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
    
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
    
class AllBorrowedBooksListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """
    model = BookInstance
    template_name ='catalog/all_borrowed_books.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
           
    
