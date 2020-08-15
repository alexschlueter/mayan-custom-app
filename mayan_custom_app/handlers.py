import logging
from pathlib import PurePath

from django.apps import apps

logger = logging.getLogger(__name__)

def auto_categorize_document(sender, instance, **kwargs):
    pass
    # logger.debug('instance: %s', instance)
    # name = PurePath(instance.label).stem
    # logger.debug('name: %s', name)
    # main_parts = [part.strip() for part in name.split('-')]
    # logger.debug('main_parts: %s', main_parts)
    # tags = main_parts[2].split(' ')
    # logger.debug('tags: %s', tags)
    # tag_model = apps.get_model(app_label='tags', model_name='Tag')
    # for tag_label in tags:
    #     logger.debug('tag_label: %s', tag_label)
    #     logger.debug('tag_model: %s', tag_model)
    #     try:
    #         tag_obj = tag_model.objects.get(label=tag_label)
    #     except tag_model.DoesNotExist:
    #         tag_obj = tag_model.objects.create(label=tag_label)
    #     logger.debug('tag_obj: %s', tag_obj)
    #     tag_obj.attach_to(instance)

    # if instance.document_type.label == 'Brief':
    #     MetadataType = apps.get_model(app_label='metadata', model_name='MetadataType')
    #     corresp_type = MetadataType.objects.get(name='correspondent')
    #     DocumentMetadata = apps.get_model(app_label='metadata', model_name='DocumentMetadata')
    #     corresp_val = main_parts[1]
    #     doc_meta = DocumentMetadata(document=instance, metadata_type=corresp_type, value=corresp_val)
    #     doc_meta.save()
