from plone.app.contenttypes.interfaces import ICollection
from plone.app.contenttypes.interfaces import IDocument
from plone.app.contenttypes.interfaces import IEvent
from plone.app.contenttypes.interfaces import IFile
from plone.app.contenttypes.interfaces import IFolder
from plone.app.contenttypes.interfaces import IImage
from plone.app.contenttypes.interfaces import ILink
from plone.app.contenttypes.interfaces import INewsItem
from vk.zipexport.interfaces import IExportAdapter
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
import imghdr
wiki = True
try:
    from rh.wiki.interfaces import IWikiPage
except ImportError:
    print("Wiki Modul not installed")
    wiki = False



@implementer(IExportAdapter)
@adapter(Interface)
class ItemExportAdapter(object):
    def __init__(self, context):
        self.context = context

    def get_metadata_dict(self):
        attributes = vars(self.context)

        metadata_dict = {
            key: attributes.get(key, None)
            for key in [
                "id",
                "title",
                "description",
                "creation_date",
                "modification_date",
                "effective_date",
                "expiration_date",
                "portal_type",
                "subject",
                "creators",
                "contributors",
                "allow_discussion",
                "exclude_from_nav",
            ]
        }

        metadata_dict["path"] = self.context.absolute_url_path()
        metadata_dict["creator"] = self.context.Creator()
        metadata_dict["local_roles"] = self.context.get_local_roles()
        metadata_dict["owner_tuple"] = self.context.getOwnerTuple()  # wozu?
        # TODO Workflow (workflow id, review history)
        # Placeful Workflow

        return metadata_dict

    def get_metadata_string(self, dict):
        filecontent = ""
        for k, v in dict.items():
            filecontent = filecontent + k + ": " + str(v) + "\n"
        return filecontent

    def get_content_for_zip(self, meta = True):
        files = self.get_files_for_zip()
        if meta:
            files.append(
                {
                "content": self.get_metadata_string(self.get_metadata_dict()),
                "filename": f"{self.context.id}_meta.txt",
                "timestamp": self.context.modification_date 

                }
            )
        return files
    
    def get_files_for_zip(self):
        return []


@implementer(IExportAdapter)
@adapter(IFile)
class FileExportAdapter(ItemExportAdapter):
    def get_metadata_dict(self):
        metadata_dict = super().get_metadata_dict()
        # wir verwenden den filename als Dateiname
        # Achtung: es ist möglich, dass mehrere Dateien den gleichen Dateiname haben
        # Es werden beide ins zipfile aufgenommen.
        metadata_dict["filename"] = self.context.file.filename
        metadata_dict["filesize"] = self.context.file.size
        return metadata_dict

    def get_files_for_zip(self):

        return [{
            "filename": self.context.file.filename,
            "content": self.context.file.data,
            "timestamp": self.context.modification_date          
        }]

@implementer(IExportAdapter)
@adapter(IImage)
class ImageExportAdapter(ItemExportAdapter):
    def get_metadata_dict(self):
        metadata_dict = super().get_metadata_dict()
        # wir verwenden den filename als Dateiname
        # Achtung: es ist möglich, dass mehrere Dateien den gleichen Dateiname haben
        # Es werden beide ins zipfile aufgenommen.
        metadata_dict["filename"] = self.context.image.filename
        metadata_dict["filesize"] = self.context.image.size        
        return metadata_dict

    def get_files_for_zip(self):

        return [{
            "filename": self.context.image.filename,
            "content": self.context.image.data,
            "timestamp": self.context.modification_date                 
        }]


@implementer(IExportAdapter)
@adapter(IDocument)
class DocumentExportAdapter(ItemExportAdapter):
    def get_metadata_dict(self):
        metadata_dict = super().get_metadata_dict()
        metadata_dict["table_of_contents"] = self.context.table_of_contents
        # text field can be empty (None)
        if self.context.text:
            metadata_dict["text"] = self.context.text.output
            metadata_dict["rawtext"] = self.context.text.raw
        return metadata_dict

    def get_files_for_zip(self):
        # We create a html string containing heading, description and content
        heading = self.context.title
        description = self.context.description
        # text field can be empty (None)
        if self.context.text:
            content = self.context.text.output
        else:
            content =""

        html_content = create_html(heading, description, content)

        return  [{
                "filename": self.context.id + ".html",
                "content": html_content,
                "timestamp": self.context.modification_date                     
            }]


@implementer(IExportAdapter)
@adapter(INewsItem)
class NewsItemExportAdapter(ItemExportAdapter):
    def get_metadata_dict(self):
        metadata_dict = super().get_metadata_dict()
        # text field can be empty (None)
        if self.context.text:        
            metadata_dict["text"] = self.context.text.output
            metadata_dict["rawtext"] = self.context.text.raw
        metadata_dict["image_caption"] = self.context.image_caption
        return metadata_dict


    def get_files_for_zip(self):

        # We create a html string containing heading, description and content
        heading = self.context.title
        description = self.context.description
        # text field can be empty (None)
        if self.context.text:
            content = self.context.text.output
        else:
            content =""

        html_content = create_html(heading, description, content)

        news_html_dict = {
            "filename": self.context.id + ".html",
            "content": html_content,
            "timestamp": self.context.modification_date                 
        }
        if self.context.image:
            # damit man sieht, zu welchem News Item das Bild gehört, stellen wird dessen id voran.
            if self.context.image.filename:
                filename = self.context.id+"_"+self.context.image.filename
            # in old News Items filename is "None" - we create one from id
            else:            
                img_type = img_type = imghdr.what('',self.context.image.data) # get file type
                if img_type == 'jpeg':
                    suffix = 'jpg'
                else:
                    suffix = img_type

                filename = self.context.id + "_img."+suffix
            #print(filename)

            news_image_dict = {
                "filename": filename,
                "content": self.context.image.data,
                "timestamp": self.context.modification_date                     
            }
            return [news_html_dict, news_image_dict]
        
        else:
            return[news_html_dict]


@implementer(IExportAdapter)
@adapter(IFolder)
class FolderExportAdapter(ItemExportAdapter):
    def get_metadata_dict(self):
        metadata_dict = super().get_metadata_dict()
        metadata_dict["nextPreviousEnabled"] = self.context.nextPreviousEnabled
        metadata_dict["layout"] = self.context.getLayout()
        metadata_dict["defaultpage"] = self.context.getDefaultPage()

        # TODO: Placeful-Workflow-Richtlinie

        return metadata_dict


@implementer(IExportAdapter)
@adapter(ILink)
class LinkExportAdapter(ItemExportAdapter):
    def get_metadata_dict(self):
        metadata_dict = super().get_metadata_dict()
        metadata_dict["remoteUrl"] = self.context.remoteUrl

        return metadata_dict

@implementer(IExportAdapter)
@adapter(IEvent)
class EventExportAdapter(ItemExportAdapter):
    pass


@implementer(IExportAdapter)
@adapter(ICollection)
class CollectionExportAdapter(ItemExportAdapter):
    pass

## Löschen, wenn wiki nicht mehr genutzt wird
if wiki:
    @implementer(IExportAdapter)
    @adapter(IWikiPage)
    class WikiExportAdapter(ItemExportAdapter):
        def get_metadata_dict(self):
            metadata_dict = super().get_metadata_dict()
            # text field can be empty (None)
            if self.context.text:
                metadata_dict["text"] = self.context.text.output
                metadata_dict["rawtext"] = self.context.text.raw
            return metadata_dict

        def get_files_for_zip(self):
            # We create a html string containing heading, description and content
            heading = self.context.title
            description = self.context.description
            # text field can be empty (None)
            if self.context.text:
                content = self.context.text.output
            else:
                content =""

            html_content = create_html(heading, description, content)

            return  [{
                    "filename": self.context.id + ".html",
                    "content": html_content,
                    "timestamp": self.context.modification_date                     
                }]




def create_html(heading, description, content):
    html = f"""
<!DOCTYPE html>    
<html>
  <head>
    <title>{heading}</title>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  </head>
  <body>
    <h1>{heading}</h1>
    <p>{description}</p>
    {content}
  </body>
</html>"""
    return html