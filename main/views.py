import logging
from .decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .models import Users, OffsetProject, Contribution  
from .forms import UserForm
from django.contrib import messages

# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def login_page(request):
    if 'user_id' in request.session:
        return redirect('dashboard')  # Redirect to dashboard if already logged in

    next_url = request.GET.get('next', 'index')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Users.objects.get(email=email, password=password)
            request.session['user_id'] = user.id
            request.session['role'] = user.role
            messages.success(request, 'Login Successful!')
            logger.info(f'User {email} logged in successfully.')

            return redirect(next_url)
        except Users.DoesNotExist:
            messages.error(request, 'Invalid Email or Password')
            logger.warning(f'Failed login attempt for email: {email}')

    return render(request, 'main/login.html', {'next': next_url})

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        if not Users.objects.filter(email=email).exists():
            Users.objects.create(email=email, password=password, role=role)
            messages.success(request, 'Signup Successful! Please Login.')
            return redirect('login')
        else:
            messages.error(request, 'Email Already Exists')
            return redirect('signup')

    return render(request, 'main/login.html')


@login_required
def dashboard(request):
    user = request.user
    
    context = {}

    if user.account_type == 'Individual':
        contributions = Contribution.objects.filter(user=user)
        total_amt_paid = contributions.aggregate(Sum('amount'))['amount__sum'] or 0
        invested_projects = contributions.values_list('project__title', flat=True).distinct()
        carbon_score = total_amt_paid // 100  # Simple logic (100 Rs = 1 Carbon Score)

        context['carbon_score'] = carbon_score
        context['total_amt_paid'] = total_amt_paid
        context['invested_in'] = invested_projects
        context['account_type'] = 'Individual'

    elif user.account_type == 'Organization':
        projects = ListProject.objects.filter(user=user)
        total_projects = projects.count()
        total_contribution = Contribution.objects.filter(project__in=projects).aggregate(Sum('amount'))['amount__sum'] or 0

        context['total_projects'] = total_projects
        context['total_contribution'] = total_contribution
        context['projects_listed'] = projects
        context['account_type'] = 'Organization'

    return render(request, 'dashboard.html', context)


def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('/')  # Redirect to homepage or any URL after logout



def toknowmore(request):
    return render(request, 'main/toknowmore.html')


def offset(request):
    return render(request, 'main/offset.html')

def tips(request):
    return render(request, 'main/tips.html')

def user_list(request):
    users = Users.objects.all()
    return render(request, 'main/user_list.html', {'users': users})

def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'main/user_form.html', {'form': form})

def user_update(request, id):
    user = Users.objects.get(id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'main/user_form.html', {'form': form})

@login_required
def calculator(request):
    if request.method == "GET":
        return render(request, 'main/calculator.html')  # Correct template path
    elif request.method == "POST":
        try:
            # Collect data from form
            electricity = int(request.POST.get("electricity", 0))
            yearly_driving = int(request.POST.get("yearlyDriving", 0))
            fuel_type = request.POST.get("fuelType", "none")
            waste_amount = int(request.POST.get("wasteAmount", 0))
            diet_type = request.POST.get("dietType", "vegetarian")
            water_usage = int(request.POST.get("waterUsage", 0))
            electronics = request.POST.get("electronics", "rarely")
            solar_panels = request.POST.get("solarPanels", "no")
            vacations = request.POST.get("vacations", "yearly")

            # Carbon calculations (Modify formulas as needed)
            energy_emission = electricity * 0.4
            transport_emission = yearly_driving * (2.3 if fuel_type in ["petrol", "diesel"] else 0.5)
            waste_emission = waste_amount * 0.1
            food_emission = 2.0 if diet_type == "nonVegetarian" else 1.2 if diet_type == "vegetarian" else 0.8
            water_emission = water_usage * 0.01
            goods_emission = 2 if electronics == "yearly" else 1 if electronics == "2years" else 0.5
            renewable_emission = -1 if solar_panels in ["highProduction", "lowProduction"] else 0
            lifestyle_emission = 2 if vacations == "yearly" else 1

            # Calculate Total Carbon Footprint
            total_emission = (
                energy_emission + transport_emission + waste_emission +
                food_emission + water_emission + goods_emission +
                renewable_emission + lifestyle_emission
            ) / 1000

            if total_emission <= 2:
                 remark = "Excellent 🌿 - You are an Eco Hero!"
            elif 2 < total_emission / 1000 <= 4:
                 remark = "Good 😊 - But still, you can reduce your footprint!"
            elif 4 < total_emission / 1000 <= 6:
                 remark = "Moderate ⚠️ - Try to adopt greener habits!"
            else:
                remark = "Very High 🔥 - Immediate action needed! Plant trees, Save Energy, Go Solar!"


            # Return JSON response
            return JsonResponse({
                 "carbon_emission": round(total_emission, 2),
                 "energy": energy_emission,
                 "transport": transport_emission,
                 "waste": waste_emission,
                 "food": food_emission,
                 "water": water_emission,
                 "goods": goods_emission,
                 "renewable": renewable_emission,
                 "lifestyle": lifestyle_emission,
                 "remark": remark  # 👈 This will return the remark
                 })


        except Exception as e:
            print("Error:", e)  # Print error in terminal
            return JsonResponse({"error": "Something went wrong!"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

def offset_projects(request):
    return render(request, 'main/offset.html')

@login_required
def list_project(request):
    categories = OffsetProject.CATEGORY_CHOICES  # ✅ Fetch project choices here
    print("Session Data:", request.session.items())  # Debug Statement ✅
    
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        location = request.POST.get('location')
        amount = request.POST.get('amount')
        duration = request.POST.get('duration')
        contact_email = request.POST.get('contact_email')

        if project_name and amount:
            OffsetProject.objects.create(
                project_name=project_name,
                description=description,
                category=category,
                location=location,
                target_amount=int(amount),
                duration=duration,
                contact_email=contact_email
            )
            messages.success(request, 'Project Listed Successfully!')
            return redirect('marketplace')  # Redirect to marketplace instead of my_projects
        else:
            messages.error(request, 'Please fill all fields!')
    
    return render(request, 'main/list_project.html', {'categories': categories})

@login_required
def contribute(request):
    projects = OffsetProject.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        project = OffsetProject.objects.get(id=request.POST['project'])
        amount = request.POST['amount']
        payment = request.POST['payment']

        Contribution.objects.create(
            name=name,
            email=email,
            project=project,
            amount=amount,
            payment=payment
        )
        messages.success(request, "Thank you for your contribution!")
        return redirect('marketplace')

    return render(request, 'main/contribution.html', {'projects': projects})

def marketplace(request):
    category = request.GET.get('category')
    if category:
        projects = OffsetProject.objects.filter(category=category)
    else:
        projects = OffsetProject.objects.all()
    categories = OffsetProject.CATEGORY_CHOICES
    return render(request, 'main/marketplace.html', {'projects': projects, 'categories': categories})

def contribution(request):
    projects = OffsetProject.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        project = OffsetProject.objects.get(id=request.POST['project'])
        amount = request.POST['amount']
        payment = request.POST['payment']

        Contribution.objects.create(
            name=name,
            email=email,
            project=project,
            amount=amount,
            payment=payment
        )
        messages.success(request, "Thank you for your contribution!")
        return redirect('marketplace')

    return render(request, 'main/contribution.html', {'projects': projects})
