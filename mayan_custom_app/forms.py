from django import forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.utils import get_language, get_language_choices
from mayan.apps.documents.settings import setting_language

class DocumentLanguageForm(forms.Form):
    language = forms.ChoiceField(
        label=_('Language'),
        choices=get_language_choices(),
        initial=setting_language.value,
        widget=forms.Select(
            attrs={
                'class': 'select2'
            }
        )
    )