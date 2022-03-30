from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from users.forms import UserRegisterForm, UserUpdateForm
from django.contrib import messages
from .models import Profile
#import login_required decorator for profile
from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account was created for {username}')
			form.save()
			return redirect('login')
	else:
		form = UserRegisterForm()
		return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
	return render(request, 'users/profile.html')


@login_required
def profile_edit(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		if u_form.is_valid():
			u_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('profile')

	else:
		u_form = UserUpdateForm(instance=request.user)

	context = {
	'u_form': u_form,
	}
	return render(request, 'users/profile_edit.html', context)
