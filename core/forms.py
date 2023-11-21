from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm
from django import forms
from .models import Profile,Role,Post
from django.contrib.auth.models import User

class UserSiginForm(UserCreationForm):
	bio = forms.CharField(widget= forms.Textarea(attrs = {'rows':'5','class':'form-input','id':'bio'}))
	address = forms.CharField(widget= forms.Textarea(attrs = {'rows':3,'class':'form-input','id':'address'}))

	class Meta:
		model = User
		fields = UserCreationForm.Meta.fields + ('bio','address')
		widgets = {'username':forms.TextInput(attrs = {'class':'form-input'}),
				'password1':forms.PasswordInput(attrs = {'class':'form-input'})

		}


	def save(self,commit = True):
		user = super().save(commit = False)
		role = Role.objects.filter(name = 'User').first()
		address = self.cleaned_data['address']
		bio = self.cleaned_data['bio']

		profile = Profile(user=user,roles = role,address  = address,bio = bio)

		if commit:
			user.save()
			profile.save()

class UserLoginForm(AuthenticationForm):
	username = forms.CharField(widget= forms.TextInput(attrs = {'rows':'5','class':'form-input'}))
	password = forms.CharField(widget= forms.PasswordInput(attrs = {'rows':3,'class':'form-input'}))

	class Meta:
		model = User
		fields = ('username','password')
		widgets = {'username':forms.TextInput(attrs = {'class':'form-input'}),
				'password':forms.PasswordInput(attrs = {'class':'form-input'})

		}

class NewPosts(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title','body')
		widgets = {'body':forms.Textarea(attrs = {'rows':10,'id':'body'}),
		'title':forms.TextInput(attrs = {'id':'title'})}

class EditProfileForm(UserChangeForm):
	bio = forms.CharField()
	address = forms.CharField()
	class Meta:
		model = User
		fields = ('bio','address')
