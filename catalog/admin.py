from django.contrib import admin
from .models import Author,Genre,Book,BookInstance,Language


# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)


# Register your models here.

#Define the adminclass

class BookInline(admin.TabularInline):
    model=Book
    
    
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines=[BookInline]



#Register the admin class with the associated model
admin.site.register(Author,AuthorAdmin)

#Register the admin classes for book using decorator

@admin.register(BookInstance)
class  BookInstanceAdmin(admin.ModelAdmin):
    list_display=('id','book','status','borrower','due_back')
    # list_filter = ('status', 'due_back')

    fieldsets= (
        ('Book Instance', {'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )
    
    
     
class BookInstanceInline(admin.TabularInline):
    model=BookInstance 

    
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines=[BookInstanceInline]
    


