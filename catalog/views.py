from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from . import views


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()
    
    num_genres = Genre.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres' : num_genres,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
    def get_queryset(self):
        return Book.objects.all()[:5] # Get 5 books containing the title war
  

class BookDetailView(generic.DetailView):
    model = Book
    def book_detail_view(request, primary_key):
        # try:
        #     book = Book.objects.get(pk=primary_key)
        # except Book.DoesNotExist:
        #     raise Http404('Book does not exist')
    
        # return render(request, 'catalog/book_detail.html', context={'book': book})
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, 'book_detail.html', context={'book': book})

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2
    # tmplate_name = 'author_list.html'
    def get_queryset(self):
        return Author.objects.all()[:5]

class AuthorDetailView(generic.DetailView):
    model = Author
    def author_detail_view(request, primary_key):
        author = get_object_or_404(Author, pk=primary_key)
        return render(request,'author_detail.html',context={'author': author})       

# class MyView(PermissionRequiredMixin, View):
#     permission_required = 'catalog.can_mark_returned'
#     # Or multiple permissions
#     permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
#     # Note that 'catalog.can_edit' is just an example
#     # the catalog application doesn't have such permission!

# class MyView(LoginRequiredMixin, View):
#     login_url = '/login/'
#     redirect_field_name = 'redirect_to'


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksByStaffListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_staff.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.all().filter(status__exact='o').order_by('due_back')

