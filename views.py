from django.shortcuts import render, redirect
from .forms import PromptForm
from genai import generate_code
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import History
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

def index(request):
    code = None
    error = None
    selected_model = 'gemini-1.5-flash'
    examples = [
        'a function to reverse a string',
        'a class for a simple calculator',
        'a function to check if a number is prime',
        'a script to read a CSV file and print its contents',
        'a decorator to time a function',
    ]
    if request.method == 'POST':
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            selected_model = form.cleaned_data['model']
            code = generate_code(prompt, selected_model)
            # Save to history
            History.objects.create(
                user=request.user if request.user.is_authenticated else None,
                prompt=prompt,
                model=selected_model,
                code=code
            )
        else:
            error = 'Please enter a valid prompt.'
    else:
        form = PromptForm()
    return render(request, 'frontend/index.html', {'form': form, 'code': code, 'error': error, 'examples': examples, 'selected_model': selected_model})

@login_required
def history(request):
    history_items = History.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'frontend/history.html', {'history_items': history_items})

@require_POST
@login_required
def mark_downloaded(request):
    latest = History.objects.filter(user=request.user).order_by('-created_at').first()
    if latest and not latest.downloaded:
        latest.downloaded = True
        latest.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'no_history'}, status=400)

@login_required
def clear_history(request):
    if request.method == 'POST':
        History.objects.filter(user=request.user).delete()
        return redirect('history')
    return redirect('history')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
