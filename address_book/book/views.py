"""
    Module name :- views
    Method(s) :- create_contact(), update_contact(), sigup(), login_user(), mark_star(),
    search_query()
    Classes :- ContactList, StarredList, ContactDetail, ContactDelete
"""

from typing import Any
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from book.models import Contact
from book.forms import UserForm, LoginForm


# Create your views here.
@login_required(login_url="login")
def create_contact(request):
    """
    Function to create a contact.
    """
    if request.method == "POST":
        name = request.POST["name"].lower()

        if Contact.objects.filter(name=name).exists():
            messages.info(request, "Contact already exists.")
            return redirect("all-contacts")

        contact = Contact.objects.create(
            user=request.user,
            name=name,
            email=",".join(request.POST.getlist("email", [])),
            phone_no=",".join(request.POST.getlist("phone")),
            address=",".join(request.POST.getlist("address", [])),
        )

        contact.save()
        return redirect("all-contacts")
    return render(request, "contacts.html")


@login_required(login_url="login")
def update_contact(request, pk):
    """
    Funcation to update a contact.
    """
    if request.method == "POST":
        contact = Contact.objects.get(pk=pk)

        contact.name = request.POST["name"]
        contact.email = request.POST.getlist("email", [])
        contact.phone_no = request.POST.getlist("phone", [])
        contact.address = request.POST.getlist("address", [])

        contact.save()
        return redirect(f"/contacts/{pk}/profile/")
    return render(request, "contacts.html")


def signup(request):
    """
    Function for user registration.
    """
    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data["username"].lower()
            user.set_password(form.cleaned_data["password"])
            user.save()

            messages.info(request, "User created")
            return redirect("login")

        messages.info(request, "Enter valid data.")
        return render(request, "signup.html", {"form": form})

    form = UserForm()
    return render(request, "signup.html", {"form": form})


def login_user(request):
    """
    Function for user login.
    """
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"].lower()
            password = form.cleaned_data["password"]

            if not User.objects.filter(username=username).exists():
                messages.info(request, "Incorrect Username")
                return redirect("login")

            user = authenticate(username=username, password=password)

            if user is None:
                messages.info(request, "Incorrect Password")
                return redirect("login")

            login(request, user)
            messages.info(request, "Successfully logged in")
            return redirect("all-contacts")

        messages.info(request, "Enter valid data")
        return render(request, "login.html", {"form": form})

    form = LoginForm()
    return render(request, "login.html", {"form": form})


@method_decorator(login_required(login_url="login"), name="dispatch")
class ContactList(ListView):
    """
    Class for contact list.
    """

    template_name = "contacts.html"
    paginate_by = 5
    context_object_name = "contacts"

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


@method_decorator(login_required(login_url="login"), name="dispatch")
class StarredList(ListView):
    """
    Class for starred contact list.
    """

    template_name = "starred.html"
    paginate_by = 5
    context_object_name = "contacts"

    def get_queryset(self):
        contacts = Contact.objects.filter(user=self.request.user, starred=True)
        return contacts


@method_decorator(login_required(login_url="login"), name="dispatch")
class ContactDetail(DetailView):
    """
    Class to provide details of a contact.
    """

    model = Contact
    context_object_name = "contact"
    template_name = "information.html"


@method_decorator(login_required(login_url="login"), name="dispatch")
def mark_star(request, pk):
    """
    Function to mark a contact starred or unstarred.
    """
    contact = Contact.objects.get(pk=pk)

    if contact.starred:
        contact.starred = False
    else:
        contact.starred = True

    contact.save()

    return redirect(f"/contacts/{pk}/profile/")


@method_decorator(login_required(login_url="login"), name="dispatch")
class ContactDelete(DeleteView):
    """
    Class to delete a contact.
    """

    model = Contact
    template_name = "contact_delete.html"
    success_url = "/contacts/all-contacts/"


@login_required(login_url="login")
def search_query(request):
    """
    Function to make search.
    """
    search = request.GET.get("search", "")

    contacts = Contact.objects.filter(
        Q(name__icontains=search)
        | Q(email__icontains=search)
        | Q(phone_no__icontains=search)
        | Q(address__icontains=search)
    )

    return render(
        request, "search_results.html", {"contacts": contacts, "query": search}
    )
