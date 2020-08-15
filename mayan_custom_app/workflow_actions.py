import json
import logging

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.permissions import permission_document_properties_edit
from mayan.apps.document_states.classes import WorkflowAction
from mayan.apps.tags.permissions import permission_tag_attach
from mayan.apps.metadata.permissions import permission_document_metadata_add

logger = logging.getLogger(name=__name__)


class AttachMultipleTagsAction(WorkflowAction):
    fields = {
        'tags': {
            'label': _('Tags'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'Tags to attach to the document. Template which returns a '
                    'comma separated list of tags.'
                ), 'required': False
            }
        }
    }
    label = _('Attach multiple tags')
    widgets = {
        'tags': {
            'class': 'django.forms.widgets.Textarea', 'kwargs': {
                'attrs': {'rows': '10'},
            }
        }
    }
    permission = permission_tag_attach

    def execute(self, context):
        logging.info('attach tags pre %s', id(context['document']))
        tag_template = self.form_data.get('tags')
        Tag = apps.get_model(app_label='tags', model_name='Tag')
        context['tags'] = Tag.objects.all()
        if tag_template:
            new_tags = self.render_field(field_name='tags', context=context)
            new_tags = [tag.strip() for tag in new_tags.split(',')]
            new_tags = [tag for tag in new_tags if tag]

            logger.debug('tag_model: %s', Tag)
            for tag_label in new_tags:
                logger.debug('tag_label: %s', tag_label)
                try:
                    tag_obj = Tag.objects.get(label=tag_label)
                except Tag.DoesNotExist:
                    tag_obj = Tag.objects.create(label=tag_label)
                logger.debug('tag_obj: %s', tag_obj)
                tag_obj.attach_to(document=context['document'])

class UpdateDependentTagsAction(WorkflowAction):
    fields = {
        'dependencies': {
            'label': _('Tags'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'Tag dependencies: if document has tag, add other dependent tags.'
                    'Template which returns json of the form {tag1: [dependent_tag1, dependent_tag], tag2: ...}'
                ), 'required': True
            }
        }
    }
    label = _('Update dependent tags')
    widgets = {
        'dependencies': {
            'class': 'django.forms.widgets.Textarea', 'kwargs': {
                'attrs': {'rows': '10'},
            }
        }
    }
    permission = permission_tag_attach

    def execute(self, context):
        dependency_str = self.render_field(field_name='dependencies', context=context)
        dependencies = json.loads(dependency_str)
        logging.debug('dependencies: %s', dependencies)

        Tag = apps.get_model(app_label='tags', model_name='Tag')
        DocumentTag = apps.get_model(app_label='tags', model_name='DocumentTag')
        modified = True
        while modified:
            modified = False
            logging.debug('dis: %s', [k for k,v in dependencies.items()])
            for tag_label, dependent_tags in dependencies.items():
                logging.debug('label: %s', tag_label)
                logging.debug('dep: %s', dependent_tags)
                logging.debug('doc %s', context['document'])
                current_tags = DocumentTag.objects.filter(documents=context['document'])
                logging.debug('ct: %s', current_tags)
                if current_tags.filter(label=tag_label).exists():
                    logging.debug('cte')
                    for dep_tag_label in dependent_tags:
                        logging.debug('dpe %s', dep_tag_label)
                        dep_tag_obj = Tag.objects.get(label=dep_tag_label)
                        logging.debug('dpo %s', dep_tag_obj)
                        if not current_tags.filter(pk=dep_tag_obj.pk).exists():
                            logging.debug('not')
                            dep_tag_obj.attach_to(document=context['document'])
                            modified = True

class AddMetadataAction(WorkflowAction):
    fields = {
        'metadata_type': {
            'label': _('Metadata Type'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'Template for the metadata type.'
                ), 'required': True
            }
        },
        'value': {
            'label': _('Value'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'Template for the value to store in the metadata type field.'
                ), 'required': True
            }
        }
    }
    label = _('Add metadata')
    widgets = {
        'metadata_type': {
            'class': 'django.forms.widgets.Textarea', 'kwargs': {
                'attrs': {'rows': '10'},
            }
        },
        'value': {
            'class': 'django.forms.widgets.Textarea', 'kwargs': {
                'attrs': {'rows': '10'},
            }
        }
    }
    permission = permission_document_metadata_add

    def execute(self, context):
        logging.info('add meta pre %s', id(context['document']))
        metadata_type_str = self.render_field(field_name='metadata_type', context=context)
        value = self.render_field(field_name='value', context=context)

        MetadataType = apps.get_model(app_label='metadata', model_name='MetadataType')
        metadata_type = MetadataType.objects.get(name=metadata_type_str)
        DocumentMetadata = apps.get_model(app_label='metadata', model_name='DocumentMetadata')
        DocumentMetadata.objects.update_or_create(defaults={'value': value}, document=context['document'], metadata_type=metadata_type)
        d = context['document']
        # d.refresh_from_db()
        logger.info('add meta exe end %s', d)

class ChangeDocumentTypeAction(WorkflowAction):
    fields = {
        'document_type': {
            'label': _('New document type'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'Template for the new document type.'
                ), 'required': True
            }
        }
    }
    label = _('Change document type')
    widgets = {
        'document_type': {
            'class': 'django.forms.widgets.Textarea', 'kwargs': {
                'attrs': {'rows': '10'},
            }
        }
    }
    permission = permission_document_properties_edit

    def execute(self, context):
        logger.info('ch doc t pre %s', id(context['document']))
        DocumentType = apps.get_model(app_label='documents', model_name='DocumentType')
        new_type_str = self.render_field(field_name='document_type', context=context)
        new_type = DocumentType.objects.get(label=new_type_str)
        context['document'].set_document_type(new_type)



    # def get_form_schema(self, request):
    #     user = request.user
    #     logger.debug('user: %s', user)

    #     queryset = AccessControlList.objects.restrict_queryset(
    #         permission=self.permission, queryset=Tag.objects.all(),
    #         user=user
    #     )

    #     self.fields['tags']['kwargs']['queryset'] = queryset

    #     return {
    #         'fields': self.fields,
    #         'media': self.media,
    #         'widgets': self.widgets
    #     }