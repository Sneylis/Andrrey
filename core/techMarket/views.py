from django.shortcuts import render,redirect
from .models import *
from django.core.paginator import Paginator
from .utils import DataMixin
from django.views.generic import CreateView
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import UpdateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView

# Create your views here.

def index(request):
    unit = Unit.objects.all()
    gr = Group.objects.all()
    paginator = Paginator(unit, 15)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'page_obj': page_obj,'group':gr})


def about(request):
    return render(request,'techMarket/about.html')

def showCat(request,cat_id):
    gr = Group.objects.all()
    unit = Unit.objects.filter(cat_id=cat_id)
    context = {
        'unit': unit,
        'group': gr,
    }
    return render(request, 'index.html', context)


class register(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('techMarket:login')

    def get_context_data(self,object_list=None,**kwargs):
        context=super().get_context_data(**kwargs)
        return dict(list(context.items()))

class login(DataMixin,LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy('techMarket:index')

def user_link (request):
    return render(request,'techMarket/userPage.html')

def showUnit(request,unit_id):
    gr = Group.objects.all()
    unit = Unit.objects.filter(pk=unit_id)
    context = {
        'unit': unit,
        'group': gr,
    }
    return render(request, 'techMarket/Unit.html', context)

def AddUnit(request):
    if request.method == 'POST':
        form = UnitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('techMarket:index')
    else:
        form = UnitForm()
    return render(request, 'techMarket/addUnit.html', {'form': form})


def delunit(request,unit_id):
    if request.user.has_perm('unit.add_Unit'):
        unit = Unit.objects.filter(pk=unit_id)
        try:
            unit.delete()
            return redirect('techMarket:index')
        except:
            message="delete wasn't successful"
        return render(request,'index.html',{'message':message})
    else:
        return reverse_lazy('techMarket:index')

class updunit(UpdateView):
    model = Unit
    template_name = 'techMarket/updUnit.html'
    success_url = '/'

    fields = ['title', 'about', 'characters', 'price', 'photo','cat']

class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):

    form_class = UserPasswordChangeForm
    template_name = 'user_password_change.html'
    success_message = 'Ваш пароль был успешно изменён!'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение пароля на сайте'
        return context


    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'slug': self.request.user.profile.slug})