from django.forms import ModelForm
from .models import Room 
from django.contrib.auth.models import User # 直接使用内置User类

# . represents current directory

class RoomForm(ModelForm):
	class Meta:
		model = Room
		fields = '__all__' # all the fields in the model
		exclude = ['host', 'participants'] # exclude these fields

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']