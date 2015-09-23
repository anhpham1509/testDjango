from django.shortcuts import render
from rango.models import Category, Page

# Create your views here.

#from django.http import HttpResponse
from django.shortcuts import render
from rango.forms import CatergoryForm, PageForm

def index(request):
    # Construct a dictionary to pass to the template engine as its context.

    # Note the key boldmessage is the same as {{ boldmessage }} in the template!

    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.

    category_list = Category.objects.order_by("-likes")[::]

    context_dict= {'boldmessage': "The bold text in the content",
                   'categories' : category_list}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'rango/index.html', context_dict)

def category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages

        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category

        context_dict['category_name_slug'] = category.slug

    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)

def about(request):
    context_dict= {'italicmessage': "The italic text in the content"}
    return render(request, 'rango/about.html', context_dict)

def add_category(request):
    if request.method == 'POST':
        form = CatergoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)
        else:
            print(form.errors)
    else:
        form = CatergoryForm()

    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()

                return category(request, category_name_slug)
        else:
            print (form.errors)
    else:
        form = PageForm()

    context_dict = {'form' : form,
                    'category' : cat,
                    'category_name_slug' : category_name_slug,
                    }
    return render(request, 'rango/add_page.html', context_dict)