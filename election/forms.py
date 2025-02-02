from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Election, Position, Candidate, User, Vote

class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ['title', 'description', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'end_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['title', 'description']

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['user', 'position', 'bio', 'photo']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(role='candidate')

class StudentRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'student_id']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        if commit:
            user.save()
        return user

class VoteForm(forms.Form):
    def __init__(self, election, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for position in election.positions.all():
            candidates = position.candidates.all()
            self.fields[f'position_{position.id}'] = forms.ModelChoiceField(
                queryset=candidates,
                label=position.title,
                widget=forms.RadioSelect,
                required=True,
                error_messages={
                    'required': f'Please select a candidate for {position.title}'
                }
            ) 