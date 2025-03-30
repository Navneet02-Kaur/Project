import logging
from .decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .models import Users, OffsetProject, Contribution  
from .forms import UserForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.utils import timezone  #Import timezone


# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def login_page(request):
    if 'user_id' in request.session:
        return redirect('dashboard')  # Redirect to dashboard if already logged in

    next_url = request.GET.get('next', 'dashboard')  # ✅ Default to dashboard

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = Users.objects.filter(email=email).first()

        if user and user.check_password(password):  # ✅ Fix: Check password correctly
            request.session['user_id'] = user.id
            request.session['role'] = user.role
            messages.success(request, 'Login Successful!')
            return redirect(next_url)

        messages.error(request, 'Invalid Email or Password')

    return render(request, 'main/login.html', {'next': next_url})



def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        if not Users.objects.filter(email=email).exists():
            hashed_password = make_password(password)  # ✅ Fix: Hash password before saving
            Users.objects.create(email=email, password=hashed_password, role=role)
            messages.success(request, 'Signup Successful! Please Login.')
            return redirect('login')
        else:
            messages.error(request, 'Email Already Exists')
            return redirect('signup')

    return render(request, 'main/login.html')


@login_required
def dashboard(request):
    user_id = request.session.get('user_id')
    role = request.session.get('role')

    if not user_id:
        return redirect('login')  

    user = Users.objects.get(id=user_id)

    # carbon_score = request.session.get('carbon_score', "Not Calculated Yet")

    carbon_score = request.session.get('carbon_score', "Not Calculated Yet")

    # print(f"DEBUG: Carbon Score retrieved in dashboard -> {carbon_score}")

    print("🟢 Carbon Score from Session:", carbon_score)


    # Default values
    carbon_score = None
    total_contribution = 0
    contributions = []
    projects = []
    total_funds = 0
    org_contributions = []

    if role == 'individual':
        contributions = Contribution.objects.filter(user_id=user.id)  
        total_contribution = sum(c.amount for c in contributions)  
        # carbon_score = user.profile.carbon_score if hasattr(user, 'profile') else 0
        carbon_score =  user.carbon_score  

    elif role == 'organization':
        projects = OffsetProject.objects.filter(contact_email=user.email)  
        total_funds = sum(p.target_amount for p in projects)

        # Fetch contributions for projects owned by this organization
        org_contributions = Contribution.objects.filter(project_name__in=projects.values_list('project_name', flat=True))

    context = {
        'user_email': user.email,
        'user_type': role,
        'carbon_score': carbon_score,
        'contributions': contributions,
        'total_contribution': total_contribution,
        'projects': projects,
        'total_funds': total_funds,
        'org_contributions': org_contributions,
    }

    return render(request, 'main/dashboard.html', context)


def toknowmore(request):
    return render(request, 'main/toknowmore.html')


def offset(request):
    return render(request, 'main/offset.html')

def tips(request):
    return render(request, 'main/tips.html')

# def user_list(request):
#     users = Users.objects.all()
#     return render(request, 'main/user_list.html', {'users': users})

# def user_create(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('user_list')
#     else:
#         form = UserForm()
#     return render(request, 'main/user_form.html', {'form': form})

# def user_update(request, id):
#     user = Users.objects.get(id=id)
#     if request.method == 'POST':
#         form = UserForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('user_list')
#     else:
#         form = UserForm(instance=user)
#     return render(request, 'main/user_form.html', {'form': form})


def tips(request):
    return render(request, 'main/tips.html')

def news(request):
    return render(request, 'main/news.html')

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
            )/1000
            carbon_score = round(total_emission, 2)

            

            # ✅ Store Carbon Score in the session
            request.session['carbon_score'] = carbon_score

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
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, "You must be logged in to contribute.")
        return redirect('login')

    user = Users.objects.get(id=user_id)

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        project_id = request.POST['project']
        amount = request.POST['amount']
        payment_mode = request.POST.get('payment_mode', 'UPI')

        project = OffsetProject.objects.get(id=project_id)

        Contribution.objects.create(
            user=user,
            project_name=project.project_name,
            amount=amount,
            payment_mode=payment_mode,
            date=timezone.now()  # ✅ FIXED: Now timezone is properly used
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

def logout_view(request):
    logout(request)  # Logs out user
    request.session.flush()  # Clears session data
    messages.success(request, "Logged out successfully!")
    return redirect('login')  # Redirect to login