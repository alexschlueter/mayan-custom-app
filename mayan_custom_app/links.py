from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

link_language_multiple_edit = Link(
    icon_class_path='mayan.apps.documents.icons.icon_document_edit',
    text=_('Change language'), view='mayan_custom_app:language_multiple_edit'
)