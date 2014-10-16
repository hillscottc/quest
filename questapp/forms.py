from django import forms


class TestForm(forms.Form):
    test_txt = forms.CharField()
