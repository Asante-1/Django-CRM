from django import forms
from .models import Lead,Agent,Category, FollowUpModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = {
           'first_name',
            'last_name',
            'age',
            'agent',
            'description',
            'phone_number',
            'email',
            'profile_pictures',
            'category'
        }

        def clean_email(self):
            email = self.cleaned_data.get('email')
            qs = Lead.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("Email already exist.")
            return email


class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)


class CustomerCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = {
            "username",
        }

        def clean_username(self):
            username = self.cleaned_data.get('username')
            qs = User.objects.filter(username=username)
            if qs.exists():
                raise forms.ValidationError("username already exist")

class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.filter(organization=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields['agent'].queryset = agents

class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = {
            'category',
        }

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'name',
        )

class FollowupModelForm(forms.ModelForm):
    class Meta:
        model = FollowUpModel
        fields = {
            'notes',
            'file',
        }