from django import forms

MODEL_CHOICES = [
    ('gemini-1.5-flash', 'Gemini 1.5 Flash'),
]

class PromptForm(forms.Form):
    prompt = forms.CharField(
        label='Describe your code you want :',
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'e.g., a function to reverse a string'}),
        max_length=500,
        required=True
    )
    model = forms.ChoiceField(
        label='Model',
        choices=MODEL_CHOICES,
        widget=forms.RadioSelect,
        initial='gemini-1.5-flash',
        required=True
    ) 