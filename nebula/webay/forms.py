from django import forms
from django.contrib.auth.models import User
from webay.models import UserProfile, Item


class UserForm(forms.ModelForm):
    confirm_pw = forms.CharField(widget=forms.PasswordInput(), label='Re-enter password')
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_pw = cleaned_data.get("confirm_pw")

        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError("Email address already in use, please try a different one.")
        if password != confirm_pw:
            raise forms.ValidationError("Passwords do not match, try again.")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    dob = forms.DateField(label='Date of Birth')

    class Meta:
        model = UserProfile
        fields = ('dob', 'address', 'mobile')


class ProfileImageForm(forms.ModelForm):
    profile_pic = forms.ImageField(label='Upload a profile picture')

    class Meta:
        model = UserProfile
        fields = ['profile_pic']


class ItemForm(forms.ModelForm):
    end_datetime = forms.DateTimeField(label='End Date/Time', input_formats=['%d/%m/%Y %H:%M:%S'])
    title = forms.CharField(label='Item Name')

    class Meta:
        model = Item
        fields = ('title', 'description', 'base_price', 'end_datetime')


class ItemImageForm(forms.ModelForm):
    item_pic = forms.ImageField(label='Upload a item picture')

    class Meta:
        model = Item
        fields = ['item_pic']
