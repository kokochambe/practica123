from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .forms import RegistrationForm


def home_view(request):
    """Главная страница системы"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/home.html')


def login_view(request):
    """Представление входа в систему"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    
    return render(request, 'accounts/login.html')


def register_view(request):
    """Представление регистрации нового пользователя"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, f'Регистрация успешна! Теперь вы можете войти как {user.username}')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации. Проверьте данные.')
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    """Представление выхода из системы"""
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('home')


@login_required
def dashboard_view(request):
    """Главная панель в зависимости от роли пользователя"""
    user = request.user
    
    context = {
        'user': user,
    }
    
    # Получаем статистику в зависимости от роли
    if user.is_admin:
        from equipment.models import Equipment
        from workorders.models import WorkOrder
        from inventory.models import SparePart
        
        context['total_equipment'] = Equipment.objects.count()
        context['active_equipment'] = Equipment.objects.filter(status='active').count()
        context['total_orders'] = WorkOrder.objects.count()
        context['new_orders'] = WorkOrder.objects.filter(status='new').count()
        context['in_progress_orders'] = WorkOrder.objects.filter(status='in_progress').count()
        context['total_parts'] = SparePart.objects.count()
        context['low_stock_parts'] = SparePart.objects.filter(current_stock__lt=models.F('min_stock')).count() if 'models' in dir() else SparePart.objects.filter(current_stock__lte=5).count()
        template = 'dashboards/admin.html'
        
    elif user.is_engineer:
        from equipment.models import Equipment
        from workorders.models import WorkOrder
        
        context['equipment_count'] = Equipment.objects.filter(workshop=user.department).count() if user.department else Equipment.objects.count()
        context['planned_orders'] = WorkOrder.objects.filter(order_type='planned', status__in=['new', 'assigned']).count()
        context['emergency_orders'] = WorkOrder.objects.filter(order_type='emergency', status__in=['new', 'assigned', 'in_progress']).count()
        template = 'dashboards/engineer.html'
        
    elif user.is_technician:
        from workorders.models import WorkOrder
        
        context['my_orders'] = WorkOrder.objects.filter(assigned_user=user).exclude(status='completed')
        context['completed_orders'] = WorkOrder.objects.filter(assigned_user=user, status='completed').count()
        template = 'dashboards/technician.html'
        
    elif user.is_storekeeper:
        from inventory.models import SparePart, PartRequest
        
        context['low_stock_parts'] = SparePart.objects.filter(current_stock__lte=models.F('min_stock')) if 'models' in dir() else SparePart.objects.filter(current_stock__lte=5)
        context['pending_requests'] = PartRequest.objects.filter(status='requested')
        template = 'dashboards/storekeeper.html'
        
    elif user.is_trainee:
        from equipment.models import Equipment
        from workorders.models import WorkOrder
        
        context['recent_orders'] = WorkOrder.objects.filter(status='completed')[:10]
        context['equipment_list'] = Equipment.objects.all()[:20]
        template = 'dashboards/trainee.html'
    else:
        template = 'dashboards/admin.html'
    
    return render(request, template, context)
