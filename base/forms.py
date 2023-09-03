from django.forms import ModelForm
from .models import Room, User # classes from model.py
from django.contrib.auth.forms import UserCreationForm # Customized UserForm

# . represents current directory

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
	class Meta:
		model = Room
		fields = '__all__' # all the fields in the model
		exclude = ['host', 'participants'] # exclude these fields

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']