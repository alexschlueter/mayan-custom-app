from django.conf.urls import url

from .views import DocumentLanguageEditView

urlpatterns = [
    url(
        regex=r'^documents/multiple/language/edit/$',
        name='language_multiple_edit', view=DocumentLanguageEditView.as_view()
    )
]