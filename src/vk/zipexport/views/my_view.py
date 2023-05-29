# -*- coding: utf-8 -*-

# from vk.zipexport import _
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IMyView(Interface):
    """Marker Interface for IMyView"""


@implementer(IMyView)
class MyView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('my_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()
