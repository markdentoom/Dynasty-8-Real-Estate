from django.shortcuts import render, get_object_or_404
from .models import Listing
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices


# Create your views here.
def index(request):
    listings = Listing.objects.order_by('-price').filter(is_published=True)
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context = {
        'listings': paged_listings,
    }
    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    context = {
        'listing': listing,
    }
    return render(request, 'listings/listing.html', context)


def search(request):
    queryset_list = Listing.objects.order_by('-list_date')
    # Tip for future self: the search results are visible in the website URL after searching something. The results are
    # based on the name argument in the HTML, e.g: <select name="state" class="form-control">

    # find homes if 'keywords' in description
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:  # only filter if there's a search query entered
            queryset_list = queryset_list.filter(description__icontains=keywords)

    # find exact city match
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    # find exact state match
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # find less or equal to searched number of bedrooms
    if 'bedroom' in request.GET:
        bedroom = request.GET['bedroom']
        if bedroom:
            queryset_list = queryset_list.filter(bedroom__lte=bedroom)

    # find less or equal to searched price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'price_choices': price_choices,
        'bedroom_choices': bedroom_choices,
        'state_choices': state_choices,
        'listings': queryset_list,
        'values': request.GET,  # In order to keep results after searching something, add this to CharFields and e.g:
        # value="{{values.keywords}}" to the HTML inputs. If you have an option menu, add an if statement like this to
        # the HTML instead: <option value="{{key}}" {%if key == values.bedroom%} selected {%endif%}>{{value}}</option>
    }

    return render(request, 'listings/search.html', context)
