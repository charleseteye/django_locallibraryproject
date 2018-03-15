from django.shortcuts import render
from .models import Book,Author,BookInstance,Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.http import  HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
import datetime

from .forms import RenewBookForm


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request,pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('catalog:all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})
    

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
           
    
