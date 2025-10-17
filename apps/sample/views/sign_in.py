from django import forms
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib import messages


class SignInForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter your password'
        })
    )
    remember = forms.BooleanField(
        label='Remember me',
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'rounded border-gray-300 text-blue-600 focus:ring-blue-500',
            },
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password.")
            if not user.is_active:
                raise forms.ValidationError("This account is inactive.")
            cleaned_data['user'] = user
        
        return cleaned_data


class SignInView(FormView):
    template_name = 'sign_in.html'
    form_class = SignInForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.cleaned_data['user']
        remember = form.cleaned_data.get('remember', False)
        
        # Log the user in
        login(self.request, user)
        
        # Set session expiry based on remember me checkbox
        self.request.session.set_expiry(60 * 60 * 24 * 30 if remember else 0)  # 30 days

        messages.success(self.request, f'Welcome back, {user.username}!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data if needed
        return context
