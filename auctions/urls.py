from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("active_listings", views.active_listings, name="active_listings"),
    path("view_listing/<int:product_id>", views.view_listing, name="view_listing"),
    path("addtowatchlist/<int:product_id>", views.addtowatchlist, name="addtowatchlist"),
    path("closebid/<int:product_id>", views.closebid, name="closebid"),
    path("closedlisting", views.closedlisting, name="closedlisting"),
    path("addcomment/<int:product_id>", views.addcomment, name="addcomment"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("categories", views.categories, name="categories"),
    path("category/<str:categ>", views.category, name="category")
]
