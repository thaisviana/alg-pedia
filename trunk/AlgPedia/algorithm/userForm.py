from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username','first_name','last_name','email','password')
		password_confirm = forms.CharField(max_length=30, widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		self.base_fields['password'].widget = forms.PasswordInput()
		super(UserForm, self).__init__(*args, **kwargs)
		
	def clean_username(self):
		if User.objects.filter(username=self.cleaned_data['username'],).count():
			raise forms.ValidationError('Duplicate user')
		return self.cleaned_data['username']

	def clean_email(self):
		if User.objects.filter(email=self.cleaned_data['email'],).count():
			raise forms.ValidationError('Duplicate user')

		return self.cleaned_data['email']

	def clean_password_confirm(self):
		if self.cleaned_data['password_confirm'] != self.data['password']:
			raise forms.ValidationError('Password does not match')

		return self.cleaned_data['password_confirm']

	def save(self, commit=True):
		user = super(UserForm, self).save(commit=False)

		user.set_password(self.cleaned_data['password'])
		if commit:
			user.save()

		return user