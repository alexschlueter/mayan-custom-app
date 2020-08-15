from furl import furl
import logging

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.template import RequestContext
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _, ungettext

from mayan.apps.common.generics import MultipleObjectFormActionView
from mayan.apps.common.utils import convert_to_id_list
from mayan.apps.documents.models import Document
from mayan.apps.documents.permissions import permission_document_properties_edit
from mayan.apps.documents.icons import icon_document_edit
# from mayan.apps.documents.settings import setting_language

from .links import link_language_multiple_edit
from .forms import DocumentLanguageForm

logger = logging.getLogger(name=__name__)

class DocumentLanguageEditView(MultipleObjectFormActionView):
    form_class = DocumentLanguageForm
    model = Document
    object_permission = permission_document_properties_edit
    pk_url_kwarg = 'document_id'
    success_message = _(
        'Language edit request performed on %(count)d document'
    )
    success_message_plural = _(
        'Language edit request performed on %(count)d documents'
    )

    def get_extra_context(self):
        queryset = self.object_list

        id_list = ','.join(
            map(
                force_text, queryset.values_list('pk', flat=True)
            )
        )

        # if queryset.count() == 1:
        #     no_results_main_link = link_language_edit.resolve(
        #         context=RequestContext(
        #             request=self.request, dict_={'object': queryset.first()}
        #         )
        #     )
        # else:
        no_results_main_link = link_language_multiple_edit.resolve(
            context=RequestContext(request=self.request)
        )
        no_results_main_link.url = '{}?id_list={}'.format(
            no_results_main_link.url, id_list
        )

        result = {
            # 'form_display_mode_table': True,
            # 'no_results_icon': icon_document_edit,
            # 'no_results_main_link': no_results_main_link,
            # 'no_results_text': _('Change the language for these documents.'),
            # 'no_results_title': _('There is no language to edit'),
            'submit_icon_class': icon_document_edit,
            'submit_label': _('Change'),
            'title': ungettext(
                'Change document language',
                'Change document languages',
                queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _(
                        'Change language for document: %s'
                    ) % queryset.first()
                }
            )

        return result

    # def get_initial(self):
    #     return {'language': setting_language.value}

    # def get_post_object_action_url(self):
    #     # if self.action_count == 1:
    #     #     return reverse(
    #     #         viewname='metadata:metadata_view', kwargs={
    #     #             'document_id': self.action_id_list[0]
    #     #         }
    #     #     )
    #     # elif self.action_count > 1:
    #     url = furl(
    #         path=reverse(
    #             viewname='mayan_custom_app:language_multiple_edit'
    #         ), args={
    #             'id_list': convert_to_id_list(items=self.action_id_list)
    #         }
    #     )
    #     return url.tostr()

    def object_action(self, form, instance):
        logger.debug('Post action form %s inst %s', form, instance)
        logger.debug('lang %s', form.cleaned_data['language'])
        instance.language = form.cleaned_data['language']
        try:
            instance.save()
        except Exception as error:
            logger.debug('execption')
            if settings.DEBUG:
                raise
            else:
                if isinstance(error, ValidationError):
                    exception_message = ', '.join(error.messages)
                else:
                    exception_message = force_text(error)

                logger.debug('message')
                messages.error(
                    message=_(
                        'Error changing language for document: '
                        '%(document)s; %(exception)s.'
                    ) % {
                        'document': instance,
                        'exception': exception_message
                    }, request=self.request
                )
        else:
            logger.debug('success')
            messages.success(
                message=_(
                    'Language for document %s changed successfully.'
                ) % instance, request=self.request
            )
