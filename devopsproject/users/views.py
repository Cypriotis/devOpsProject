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

from django.shortcuts import render, redirect
from plotly_proj.models import Project
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models

class MyModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Other fields of your model
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

from django.contrib.auth.models import User

def create_project(request):
    if request.method == "POST":
        name = request.POST.get("name")
        start_date = datetime.strptime(request.POST.get("start_date"), "%Y-%m-%d").date()
        responsible_name = request.POST.get("responsible")
        
        try:
            user = User.objects.get(username=responsible_name)
            user_id = user.id
        except User.DoesNotExist:
            return None
        
        week_number = request.POST.get("week_number")
        end_date = datetime.strptime(request.POST.get("end_date"), "%Y-%m-%d").date()
        
        project_instance = Project(
            name=name,
            start_date=start_date,
            responsible=user,
            end_date=end_date
        )
        project_instance.save()

        return redirect("showplot")  # Redirect to a success page or any other desired URL

    return render(request, "authenticate/gantt_chart.html")

