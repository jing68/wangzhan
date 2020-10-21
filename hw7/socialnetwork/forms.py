from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from socialnetwork.models import Profile,Post
from django.forms import ModelForm, Textarea,TextInput

MAX_UPLOAD_SIZE = 2500000

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20)
    password = forms.CharField(max_length = 200, widget = forms.PasswordInput())
    print("hello3")

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()
        print("hello4")
        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        
        if not user:
            raise forms.ValidationError("Invalid username/password")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

class RegistrationForm(forms.Form):
    username   = forms.CharField(max_length = 20)
    password  = forms.CharField(max_length = 200, 
                                 label='Password', 
                                 widget = forms.PasswordInput())
    confirm_password  = forms.CharField(max_length = 200, 
                                 label='Confirm Password',  
                                 widget = forms.PasswordInput())
    email      = forms.CharField(max_length=50, 
                                 label='E-mail',
                                 widget = forms.EmailInput())                            
    first_name = forms.CharField(max_length=20,label='First Name')
    last_name  = forms.CharField(max_length=20, label='Last Name')
    
   

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username

class GlobalForm(forms.ModelForm):
    class Meta:
        model=Post
        fields = {'post_input_text'}
        widgets={'post_input_text':TextInput(attrs={'size':'40'})}
        labels = {'post_input_text':'New Post'}
    def clean_post_input_text(self):
        post_input_text = self.cleaned_data['post_input_text']
        if not post_input_text:
            raise forms.ValidationError('You must enter text')
        return post_input_text


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields= ('bio_input_text','Profile_Picture')
        widgets = {'bio_input_text':Textarea(attrs={'cols': 40, 'rows': 3})}
        labels = {'bio_input_text':""}

    def clean_Profile_Picture(self):
        Profile_Picture = self.cleaned_data['Profile_Picture']
        if not Profile_Picture or not hasattr(Profile_Picture, 'content_type'):
            raise forms.ValidationError('You must upload a picture')
        if not Profile_Picture:
            raise forms.ValidationError('You must upload a picture')
        if not Profile_Picture.content_type or not Profile_Picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if Profile_Picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return Profile_Picture
