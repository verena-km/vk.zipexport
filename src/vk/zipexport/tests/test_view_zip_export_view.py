# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from vk.zipexport.testing import VK_ZIPEXPORT_FUNCTIONAL_TESTING
from vk.zipexport.testing import VK_ZIPEXPORT_INTEGRATION_TESTING
from vk.zipexport.views.zip_export_view import IZipExportView
from zope.component import getMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = VK_ZIPEXPORT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        api.content.create(self.portal, "Folder", "other-folder")
        api.content.create(self.portal, "Document", "front-page")

    def test_zipexport_is_registered(self):
        view = getMultiAdapter(
            (self.portal["other-folder"], self.portal.REQUEST), name="zipexport"
        )
        self.assertTrue(IZipExportView.providedBy(view))

    def test_zipexport_not_matching_interface(self):
        view_found = True
        try:
            view = getMultiAdapter(
                (self.portal["front-page"], self.portal.REQUEST), name="zipexport"
            )
        except ComponentLookupError:
            view_found = False
        else:
            view_found = IZipExportView.providedBy(view)
        self.assertFalse(view_found)


class ViewsFunctionalTest(unittest.TestCase):

    layer = VK_ZIPEXPORT_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
