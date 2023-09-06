from zope.component import adapter
from zope.interface import implementer
from plone.app.contenttypes.interfaces import IFile, IDocument, IFolder, IImage, ILink, INewsItem, ICollection, IEvent
from zope.interface import Interface
from vk.zipexport.interfaces import IExportAdapter

@implementer(IExportAdapter)
@adapter(Interface)
class ItemExportAdapter(object):

    def __init__(self, context):
        self.context = context

    def get_metadata_dict(self):
        attributes = vars(self.context)

        metadata_dict = {key: attributes.get(key,None) for key in [
            "id", "title", "description",
            "creation_date", "modification_date", "effective_date", "expiration_date",
            "portal_type", "subject",
            "creators", "contributors",
            "allow_discussion", "exclude_from_nav",
        ]}

        metadata_dict['path'] = self.context.absolute_url_path()
        metadata_dict['creator'] = self.context.Creator()
        metadata_dict['local_roles'] = self.context.get_local_roles()
        metadata_dict['owner_tuple'] = self.context.getOwnerTuple() # wozu?
        # TODO Workflow (workflow id, review history)
        # Placeful Workflow

        return metadata_dict

    def get_metadata_string(self, dict):
        filecontent = ""
        for k, v in dict.items():
            filecontent = filecontent + k + ": " + str(v) + "\n"
        return filecontent

    def get_content_for_zip(self):
        return([{'content': self.get_metadata_string(self.get_metadata_dict()),'filename':f'{self.context.id}.meta'}])

@implementer(IExportAdapter)
@adapter(IFile)
class FileExportAdapter(ItemExportAdapter):

    def get_content_for_zip(self):
        file_dict = {'filename': self.context.file.filename, 'content': self.context.file.data }
        list = super().get_content_for_zip()
        list.append(file_dict)
        return list

@implementer(IExportAdapter)
@adapter(IImage)
class ImageExportAdapter(ItemExportAdapter):

    def get_content_for_zip(self):
        img_dict = {'filename': self.context.image.filename, 'content': self.context.image.data }
        list = super().get_content_for_zip()
        list.append(img_dict)
        return list

@implementer(IExportAdapter)
@adapter(IDocument)
class DocumentExportAdapter(ItemExportAdapter):

    def get_metadata_dict(self):
        metadata_dict = super().get_metadata_dict()
        metadata_dict['table_of_contents'] = self.context.table_of_contents
        # text field can be empty (None)
        if self.context.text:
            metadata_dict['text'] = self.context.text.output
            metadata_dict['rawtext'] = self.context.text.raw
        return metadata_dict

    def get_content_for_zip(self):
        list = super().get_content_for_zip()
        if self.context.text:
            # wir speichern den Inhalt als HTML-File
            doc_dict = {'filename': self.context.id +".html", 'content': self.context.text.output }
            list.append(doc_dict)
        return list


@implementer(IExportAdapter)
@adapter(INewsItem)
class NewsItemExportAdapter(ItemExportAdapter):
    def get_metadata_dict(self):
        metadata_dict = super().get_metadata_dict()
        metadata_dict['text'] = self.context.text.output
        metadata_dict['rawtext'] = self.context.text.raw
        metadata_dict['image_caption'] = self.context.image_caption
        return metadata_dict

    def get_content_for_zip(self):
        # wir speichern den Inhalt als HTML-File
        news_html_dict = {'filename': self.context.id +".html", 'content': self.context.text.output }
        news_image_dict = {'filename': self.context.image.filename, 'content': self.context.image.data }
        list = super().get_content_for_zip()
        list.append(news_html_dict)
        list.append(news_image_dict)
        return list


@implementer(IExportAdapter)
@adapter(IFolder)
class FolderExportAdapter(ItemExportAdapter):

    def get_metadata_dict(self):
        metadata_dict = super().get_metadata_dict()
        metadata_dict['nextPreviousEnabled'] = self.context.nextPreviousEnabled
        metadata_dict['layout'] = self.context.getLayout()
        metadata_dict['defaultpage'] = self.context.getDefaultPage()

        # TODO: Placeful-Workflow-Richtlinie

        return metadata_dict


@implementer(IExportAdapter)
@adapter(ILink)
class LinkExportAdapter(ItemExportAdapter):
    pass

@implementer(IExportAdapter)
@adapter(IEvent)
class EventExportAdapter(ItemExportAdapter):
    pass

@implementer(IExportAdapter)
@adapter(ICollection)
class CollectionExportAdapter(ItemExportAdapter):
    pass
