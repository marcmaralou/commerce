from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import _get_queryset

def get_object_or_None(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.
    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.
    Note: Like with get(), a MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None

def index(request):
    products = Listing.objects.all()
    none = False
    if len(products) == 0:
        none = True
    return render(request, "auctions/active_listings.html", {"products": products, "none": none})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="/login")
def create_listing(request):
    if request.method == "POST":
        item = Listing()
        item.seller = request.user.username
        item.title = request.POST.get("title")
        item.description = request.POST.get("description")
        item.starting_bid = request.POST.get("starting_bid")
        item.category = request.POST.get("category")
        if request.POST.get('image_link'):
            item.image_link = request.POST.get('image_link')
        else:
            item.image_link = "https://www.aust-biosearch.com.au/wp-content/themes/titan/images/noimage.gif"
        item.save()
        products = Listing.objects.all()
        none = False
        if len(products) == 0:
            none = True
        return render(request, "auctions/active_listings.html", {"products": products, "none": none})
    else:
        return render(request, "auctions/create_listing.html")

def active_listings(request):
    products = Listing.objects.all()
    none = False
    if len(products) == 0:
        none = True
    return render(request, "auctions/active_listings.html", {"products": products, "none": none})

@login_required(login_url='/login')
def view_listing(request, product_id):
    comments = Comment.objects.filter(listingid=product_id)
    if request.method == "POST":
        item = Listing.objects.get(id=product_id)
        newbid = int(request.POST.get('newbid'))
        if item.starting_bid >= newbid:
            product = Listing.objects.get(id=product_id)
            return render(request, "auctions/view_listing.html", {
                "product": product,
                "message": "Your Bid should be higher than the Current one.",
                "msg_type": "danger",
                "comments": comments
            })
        else:
            item.starting_bid = newbid
            item.save()
            bidobj = Bid.objects.filter(listingid=product_id)
            if bidobj:
                bidobj.delete()
            obj = Bid()
            obj.user = request.user.username
            obj.title = item.title
            obj.listingid = product_id
            obj.bid = newbid
            obj.save()
            product = Listing.objects.get(id=product_id)
            return render(request, "auctions/view_listing.html", {
                "product": product,
                "message": "Your Bid is added.",
                "msg_type": "success",
                "comments": comments
            })
    else:
        product = Listing.objects.get(id=product_id)
        return render(request, "auctions/view_listing.html", {"product": product})

@login_required(login_url='/login')
def addtowatchlist(request, product_id):
    obj = Watchlist.objects.filter(listingid=product_id, user=request.user.username)
    comments = Comment.objects.filter(listingid=product_id)
    if obj:
        obj.delete()
        product = Listing.objects.get(id=product_id)
        added = Watchlist.objects.filter(listingid=product_id, user=request.user.username)
        return render(request, "auctions/view_listing.html", {"product": product, "added": added, "comments": comments})
    else:
        obj = Watchlist()
        obj.user = request.user.username
        obj.listingid = product_id
        obj.save()
        product = Listing.objects.get(id=product_id)
        added = Watchlist.objects.filter(listingid=product_id, user=request.user.username)
        return render(request, "auctions/view_listing.html", {"product": product, "added": added, "comments": comments})

@login_required(login_url='/login')
def closebid(request, product_id):
    winobj = Winner()
    listobj = Listing.objects.get(id=product_id)
    obj = get_object_or_None(Bid, listingid=product_id)
    if not obj:
        message = "Deleting Bid"
        msg_type = "danger"
    else:
        bidobj = Bid.objects.get(listingid=product_id)
        winobj.owner = request.user.username
        winobj.winner = bidobj.user
        winobj.listingid = product_id
        winobj.winprice = bidobj.bid
        winobj.title = bidobj.title
        winobj.save()
        message = "Bid Closed"
        msg_type = "success"
        bidobj.delete()
    if Watchlist.objects.filter(listingid=product_id):
        watchobj = Watchlist.objects.filter(listingid=product_id)
        watchobj.delete()
    if Comment.objects.filter(listingid=product_id):
        commentobj = Comment.objects.filter(listingid=product_id)
        commentobj.delete()
    listobj.delete()
    winners = Winner.objects.all()
    empty = False
    if len(winners) == 0:
        empty = True
    return render(request, "auctions/closedlisting.html", {
        "products": winners,
        "empty": empty,
        "message": message,
        "msg_type": msg_type})

@login_required(login_url='/login')
def closedlisting(request):
    winners = Winner.objects.all()
    empty = False
    if len(winners) == 0:
        empty = True
    return render(request, "auctions/closedlisting.html", {
        "products": winners,
        "empty": empty
    })

@login_required(login_url='/login')
def addcomment(request, product_id):
    obj = Comment()
    obj.comment = request.POST.get("comment")
    obj.user = request.user.username
    obj.listingid = product_id
    obj.save()
    print("displaying comments")
    comments = Comment.objects.filter(listingid=product_id)
    product = Listing.objects.get(id=product_id)
    added = Watchlist.objects.filter(
        listingid=product_id, user=request.user.username)
    return render(request, "auctions/viewlisting.html", {
        "product": product,
        "added": added,
        "comments": comments
    })

@login_required(login_url='/login')
def dashboard(request):
    winners = Winner.objects.filter(winner=request.user.username)
    lst = Watchlist.objects.filter(user=request.user.username)
    present = False
    prodlst = []
    i = 0
    if lst:
        present = True
        for item in lst:
            product = Listing.objects.get(id=item.listingid)
            prodlst.append(product)
    print(prodlst)
    return render(request, "auctions/dashboard.html", {
        "product_list": prodlst,
        "present": present,
        "products": winners
    })

@login_required(login_url='/login')
def categories(request):
    return render(request, "auctions/categories.html")

@login_required(login_url='/login')
def category(request, categ):
    categ_products = Listing.objects.filter(category=categ)
    empty = False
    if len(categ_products) == 0:
        empty = True
    return render(request, "auctions/category.html", {
        "categ": categ,
        "empty": empty,
        "products": categ_products
    })