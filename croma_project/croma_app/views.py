from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect, render

from .models import Product

# Create your views here.
def index_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    return redirect("login")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    context = {}
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not username or not email or not password or not confirm_password:
            context["error"] = "All fields are required."
            return render(request, "register.html", context)

        if password != confirm_password:
            context["error"] = "Passwords do not match."
            return render(request, "register.html", context)

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            login(request, user)
            messages.success(request, "Registration successful. Welcome to Croma.")
            return redirect("home")
        except IntegrityError:
            context["error"] = "Username already exists. Try a different username."

    return render(request, "register.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    context = {}
    next_url = request.GET.get("next", "")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        next_url = request.POST.get("next", "")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            if next_url:
                return redirect(next_url)
            return redirect("home")
        context["error"] = "Invalid username or password."

    context["next"] = next_url
    return render(request, "login.html", context)


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


@login_required
def home_view(request):
    return render(request, "home.html")


@login_required
def display_view(request):
    db = Product.objects.all()
    context = {"data": db}
    return render(request, "display.html", context)


@login_required
def insert_view(request):
    if request.method == "POST":
        p_id = request.POST.get("p_id")
        p_name = request.POST.get("p_name")
        category = request.POST.get("category")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")

        Product.objects.create(
            p_id=p_id,
            p_name=p_name,
            category=category,
            price=price,
            quantity=quantity,
        )
        messages.success(request, "Product inserted successfully.")
        return redirect("display")
    return render(request, "insert.html")


@login_required
def update_view(request, p_id):
    db = Product.objects.get(p_id=p_id)
    context = {"data": db}
    if request.method == "POST":
        p_name = request.POST.get("p_name")
        category = request.POST.get("category")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")

        db.p_name = p_name
        db.category = category
        db.price = price
        db.quantity = quantity
        db.save()
        messages.success(request, "Product updated successfully.")
        return redirect("display")
    return render(request, "update.html", context)


@login_required
def delete_view(request, p_id):
    db = Product.objects.get(p_id=p_id)
    deleted_name = db.p_name
    db.delete()
    messages.success(request, f"{deleted_name} deleted successfully.")
    return redirect("display")




