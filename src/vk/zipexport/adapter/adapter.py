from zope.component import adapter
from zope.interface import implementer
from plone.app.contenttypes.interfaces import IFile, IDocument
from zope.interface import Interface
from vk.zipexport.interfaces import IExportAdapter

@implementer(IExportAdapter)
@adapter(Interface)
class ItemExportAdapter(object):

    def __init__(self, context):
        self.context = context

    def get_fun(self):
        return("Im a Content")

@implementer(IExportAdapter)
@adapter(IFile)
class FileExportAdapter(ItemExportAdapter):

    def get_fun(self):
        return("Im a File")

@implementer(IExportAdapter)
@adapter(IDocument)
class DocumentExportAdapter(ItemExportAdapter):

    def get_fun(self):
        return("Im a Document")