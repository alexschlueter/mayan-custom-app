from django.apps import apps

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_multi_item
from mayan.apps.documents.signals import post_document_created

from .handlers import auto_categorize_document
from .links import link_language_multiple_edit

class AutoCategorizeApp(MayanAppConfig):
    name = 'mayan_custom_app'
    verbose_name = 'Auto-Categorize'

    def ready(self):
        super(AutoCategorizeApp, self).ready()
        
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        menu_multi_item.bind_links(
            links=(link_language_multiple_edit,), sources=(Document,)
        )



        # post_document_created.connect(
        #     auto_categorize_document,
        #     dispatch_uid='auto_categorize_document', sender=Document
        # )