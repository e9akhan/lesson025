from typing import Any
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from book.models import Contact
from book.forms import UserForm, LoginForm

# Create your views here.
def create_contact(request):
    if request.method == 'POST':

        name = request.POST['name'].lower()
        
        if Contact.objects.filter(name=name).exists():
            messages.info(request, 'Contact already exists.')
            return redirect('all-contacts')
        
        contact = Contact.objects.create(
            user=request.user,
            name = name,
            email = request.POST.getlist('email', []),
            phone_no = request.POST.getlist('phone'),
            address = request.POST.getlist('address', [])
        )

        contact.save()
        return redirect('all-contacts')
    return render(request, 'contacts.html')

def update_contact(request, pk):
    if request.method == 'POST':
        contact = Contact.objects.get(pk=pk)
        
        contact.name = request.POST['name']
        contact.email = request.POST.getlist('email', [])
        contact.phone_no = request.POST.getlist('phone', [])
        contact.address = request.POST.getlist('address', [])

        contact.save()
        return redirect(f'/contacts/{pk}/profile/')
    return render(request, 'contacts.html')

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username'].lower()
            user.set_password(form.cleaned_data['password'])
            user.save()

            messages.info(request, 'User created')
            return redirect('login')
        else:
            messages.info(request, 'Enter valid data.')
            return render(request, 'signup.html', {'form': form})
    
    form = UserForm()
    return render(request, 'signup.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username'].lower()
            password = form.cleaned_data['password']
            print(username, password)

            if not User.objects.filter(username=username).exists():
                messages.info(request, 'Incorrect Username')
                return redirect('login')

            user = authenticate(username=username, password=password)

            if user is None:
                messages.info(request, 'Incorrect Password')
                return redirect('login')
            
            login(request, user)
            messages.info(request, 'Successfully logged in')
            return redirect('all-contacts')
        else:
            messages.info(request, 'Enter valid data')
            return render(request, 'login.html', {'form': form})

    form = LoginForm()
    return render(request, 'login.html', {'form': form})

class ContactList(ListView):
    template_name = 'contacts.html'
    paginate_by = 5
    context_object_name = 'contacts'
    
    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


class StarredList(ListView):
    template_name = 'starred.html'
    paginate_by = 5
    context_object_name = 'contacts'

    def get_queryset(self, **kwargs: Any):
        contacts = Contact.objects.filter(user = self.request.user, starred = True)
        return contacts

class ContactDetail(DetailView):
    model = Contact
    context_object_name = 'contact'
    template_name = 'information.html'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)

        contact = Contact.objects.get(pk=self.kwargs['pk'])

        email_list = False
        phone_list = False

        if isinstance(contact.email, list):
            email_list = True

        if isinstance(contact.phone_no, list):
            phone_list = True

        context['email_list'] = email_list
        context['phone_list'] = phone_list

        return context
    
def mark_star(request, pk):
    contact = Contact.objects.get(pk=pk)

    if contact.starred:
        contact.starred = False
    else:
        contact.starred = True

    contact.save()

    return redirect(f'/contacts/{pk}/profile/')

class ContactDelete(DeleteView):
    model = Contact
    template_name = 'contact_delete.html'
    success_url = '/contacts/all-contacts/'

def search_query(request):
    search = request.GET.get('search', '')

    print(search)

    contacts = Contact.objects.filter(
        Q(name__icontains = search) |
        Q(email__icontains = search) |
        Q(phone_no__icontains = search) |
        Q(address__icontains = search)
    )

    return render(request, 'search_results.html', {'contacts': contacts, 'query': search})
