from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from devopsproject import views
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm



# Create your views here.
def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			print("test")
			login(request, user)
			return redirect('showplot')
		else:
			print("test2")
			messages.success(request, ("There Was An Error Logging In, Try Again..."))	
			return redirect('login')	


	else:
		print("test3")
		return render(request, 'authenticate/login.html', {})

from django.shortcuts import render
from plotly_proj.models import Project
import pandas as pd
from plotly.offline import plot
import plotly.express as px

def index(request):
    qs = Project.objects.all()
    projects_data = [
        {
            'Project': x.name,
            'Start': x.start_date,
            'Finish': x.end_date,
            'Responsible': x.responsible.username
        } for x in qs
    ]

    df = pd.DataFrame(projects_data)

    fig = px.timeline(
        df, x_start="Start", x_end="Finish", y="Project", color="Responsible"
    )

    fig.update_yaxes(autorange="reversed")
    gantt_plot = plot(fig, output_type="div")
    context = {'plot_div': gantt_plot}
    return render(request, 'index.html', context)

def logout_user(request):
	logout(request)
	messages.success(request, ("You Were Logged Out!"))
	return redirect('home')

def register_user(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Registration Successful!"))
			return redirect('showplot')
	else:
		form = RegisterUserForm()

	return render(request, 'authenticate/register_user.html', {
		'form':form,
		})

def home(request):
	return render(request, 'authenticate/home.html', {})
 
