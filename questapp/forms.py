from django import forms


class ClueSearchForm(forms.Form):
    search_txt = forms.CharField(required=False)


