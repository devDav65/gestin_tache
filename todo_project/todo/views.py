from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Task 
from .forms import TaskForm

# Create your views here
@login_required(login_url="login_user")
def list_task (request):
    user = request.user
    tasks = Task.objects.filter(proprio=request.user).order_by('date_creation')

    total_tasks = tasks.count()
    completeds_tasks = tasks.filter(completed = True).count()
    pending_tasks = tasks.filter(completed = False).count()

    query = request.GET.get("recherche")
    if query :
        tasks = tasks.filter(titre__icontains=query)
    

    context = {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completeds_tasks,
        'pending_tasks': pending_tasks,
        'query':query,
    }
    return render(request, 'todo/task.html', context)

@login_required(login_url="login_user")
def list_create(request):
    form = TaskForm(request.POST or None)
    if form.is_valid(): 
        task = form.save(commit=False)
        task.proprio = request.user
        task.save()
        return redirect('list_task')
    return render(request, 'todo/form.html',{'form':form})


@login_required(login_url="login_user")
def completed_task(request, id):
    task = get_object_or_404(Task, id=id,proprio=request.user)
    task.completed = True
    task.save()
    return redirect('list_task')

@login_required(login_url="login_user")
def nocompleted_task(request, id):
    task = get_object_or_404(Task, id=id,proprio=request.user)
    task.completed = False
    task.save()
    return redirect('list_task')




@login_required(login_url="login_user")
def list_update(request, id):
    task = get_object_or_404(Task,id=id,proprio=request.user)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid(): 
        form.save()
        return redirect('list_task')
    
    context ={
        'form': form,
        'task': task,
    }
    return render(request,'todo/update.html',context)


@login_required(login_url="login_user")
def delete_task(request, id):
    task = get_object_or_404(Task, id=id,proprio=request.user)
    if request.method=='POST':
        task.delete()
        return redirect('list_task')
    return render (request, 'todo/confirmdelate.html',{'task':task})

def signin_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, "Les mots de passes ne sont pas identiques")
        elif User.objects.filter(username=username).exists():
            messages.error(request,"Cet nom d'utilisateur est deja utiliser")
        elif User.objects.filter(email=email).exists():
            messages.error(request,"Cet email est deja utilise")
        else:
            user = User.objects.create_user(
                username = username,
                email = email,
                password=password1,
                first_name = first_name,
                last_name = last_name
                )
            return redirect("login_user")
        
    return render(request,'todo/signin.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('list_task')
        else:
            messages.info(request,"Indentifiant ou mot de passe incorrect")
    return render(request, 'todo/login.html')

def logout_user(request):
    logout(request)
    return redirect('login_user') 

def profil(request):
    user = request.user
    tasks = Task.objects.filter(proprio=request.user).order_by('date_creation')


    completed_tasks = tasks.filter(completed = True).count()
    en_cours = tasks.count()
    


    context = {
        'user':user,
        'tasks':tasks,
        'completed_tasks':completed_tasks,
        'en_cours':en_cours

    }    
        

    return render(request,'todo/profil.html',context)


def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "❌ Les mots de passe ne correspondent pas.")
            return redirect('change_password')
        if not request.user.check_password(old_password):
            messages.error(request, "❌ L'ancien mot de passe est incorrect.")
            return redirect('change_password')
        
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)

        messages.success(request, "✅ Mot de passe changé avec succès !")
        return redirect('profil')
    
    return render(request, 'todo/change_password.html')

def update_profil(request):

    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')

        user = request.user
        user.first_name = prenom
        user.last_name = nom
        user.email = email
        user.save()

        messages.success(request, "✅ Profil mis à jour avec succès !")
        return redirect('profil')
    
    return render(request, 'todo/update_profil.html')
