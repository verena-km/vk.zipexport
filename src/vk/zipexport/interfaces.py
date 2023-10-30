# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IVkZipexportLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IExportAdapter(Interface):
    """Kommentar noch ergänzen"""


    def get_metadata_dict(self):
        """returns a dictionary with metadata"""

    def get_metadata_string(self, dict):
        """returns a string with the metadata"""

    def get_files_for_zip(self):
        """returns a list of dicts with filename and content"""        

    def get_content_for_zip(self, meta):
        """returns a list of dicts with filename and content"""