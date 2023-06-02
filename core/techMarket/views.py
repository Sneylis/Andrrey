from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.http import HttpResponseRedirect
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
    uq = UserQueston.objects.filter(choice=None).count
    q = request.GET.get('q')

    if q == None:
        unit = Unit.objects.all().order_by('-id')
    else:
        unit = Unit.objects.filter(title__contains=q).order_by('-id')
    gr = Group.objects.all()
    paginator = Paginator(unit, 15)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'page_obj': page_obj,'group':gr,'Questions':uq})


def about(request):
    uq = UserQueston.objects.filter(choice=None).count
    gr = Group.objects.all()
    return render(request,'techMarket/about.html',{'group':gr,'Questions':uq})

def showCat(request,cat_id):
    gr = Group.objects.all()
    q = request.GET.get('q')
    uq = UserQueston.objects.filter(choice=None).count
    if q == None:
        unit = Unit.objects.filter(cat_id=cat_id).order_by('-id')
    else:
        unit = Unit.objects.filter(title__contains=q,cat_id=cat_id).order_by('-id')

    paginator = Paginator(unit, 15)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'group': gr,
        'Questions': uq
    }
    return render(request, 'techMarket/cat.html', context)

def SGroup(request, group_id):
    uq = UserQueston.objects.filter(choice=None).count
    gr = Group.objects.all()
    g = Group.objects.get(pk=group_id)
    cat = Category.objects.filter(group=g)
    unit = Unit.objects.filter(cat=cat)
    paginator = Paginator(unit, 15)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'group': gr,
        'Questions': uq
    }
    return render(request, 'index.html', context)

def register(request):
    if request.method == 'POST':
         form = RegisterUserForm(request.POST)
         with transaction.atomic():
             if form.is_valid():
                 user = form.save()
                 login(request,user)
                 return redirect('techMarket:index')
             else:
                 return render(request,'register.html',{'form':form})
    else:
        return render(request, 'register.html', {'form':RegisterUserForm()})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return redirect('techMarket:index')
            else:
                form.add_error(None, 'неверный логин или пароль')
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})
    else:
        return render(request, 'login.html', {'form': LoginForm()})


def user_link (request):
    gr = Group.objects.all()
    uq = UserQueston.objects.filter(choice=None).count
    q = UserQueston.objects.filter(user=request.user)
    return render(request,'techMarket/userPage.html',{'group': gr,
        'Questions':uq})

def showUnit(request,unit_id):
    uq = UserQueston.objects.filter(choice=None).count
    gr = Group.objects.all()
    unit = Unit.objects.get(pk=unit_id)
    context = {
        'unit': unit,
        'group': gr,
        'Questions':uq
    }
    return render(request, 'techMarket/Unit.html', context)
@permission_required('unit.unit',raise_exception=True)
def AddUnit(request):
    gr = Group.objects.all()
    uq = UserQueston.objects.filter(choice=None).count
    if request.method == 'POST':
        form = UnitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('techMarket:index')
    else:
        form = UnitForm()
    return render(request, 'techMarket/addUnit.html', {'form': form,'group': gr,'Questions':uq})

@permission_required('unit.delete_unit',raise_exception=True)
def delunit(request,unit_id):
    if request.user.has_perm('unit.add_Unit'):
        unit = Unit.objects.get(pk=unit_id)
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


@login_required(login_url='techMarket:login')
def GetQuestion(request,unit_id):
    gr = Group.objects.all()
    uq = UserQueston.objects.filter(choice=None).count

    u = Unit.objects.get(pk=unit_id)
    try:
        question = request.POST['questions']
        question = str(question)
        user_q = UserQueston(user=request.user,question=question,unit=u)
        user_q.save()
        message = 'вопрос успешно отправлен, сататуса вопроса выможете просмотреть в вкладке Мои Вопросы'
        return render(request,'techMarket/Unit.html',{'unit':u,'message':message,'group': gr,'Questions':uq})
    except:
        message = 'Заполните поля'
        return render(request,'techMarket/Unit.html',{'unit':u,'message':message,'group': gr,'Questions':uq})
@login_required(login_url='techMarket:login')
def ShUserQuestion(request):
    uq = UserQueston.objects.filter(choice=None).count
    q = UserQueston.objects.filter(user=request.user)
    g = Group.objects.all()
    paginator = Paginator(q, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'User_Questions.html', {'page_obj':page_obj,'group':g,'Questions':uq})

def GetAsnwer(request):
    uq = UserQueston.objects.filter(choice=None).count
    gr = Group.objects.all()
    u = UserQueston.objects.filter(choice=None)
    return render(request,'GetAnswer.html',{'questions':u,'group': gr,'Questions':uq})

def GetChiuce(request,pk):
    uq = UserQueston.objects.filter(choice=None).count
    q = UserQueston.objects.filter(user=request.user)
    p = UserQueston.objects.get(pk=pk)
    u = UserQueston.objects.filter(choice=None)
    try:
        choice = request.POST['choice']
        if choice != '' or choice !='' or choice == None:
            p.choice = choice
            p.save()
            return redirect('techMarket:AdminQuestion')
        else:
            message = 'пожалуйста заполните поле'
            return render(request, 'GetAnswer.html', {'questions': u, 'message': message,'group': gr,'Questions':uq})

    except:
        message = 'пожалуйста заполните поле'
        return render(request,'GetAnswer.html',{'questions':u,'message':message,'group': gr,'Questions':uq})
