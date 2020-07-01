from django import forms


CHOICES = (
    (True, 'Private'),
    (False, 'Public'),
)


class PostForm(forms.Form):

    text = forms.CharField(min_length=3, max_length=256, widget=forms.Textarea)
    isPrivate = forms.ChoiceField(choices=CHOICES)

    def clean(self):
        data = self.cleaned_data
        data['isPrivate'] = True if data['isPrivate'] == 'True' else False
        return data
