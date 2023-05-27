# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import vk.zipexport


class VkZipexportLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=vk.zipexport)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "vk.zipexport:default")


VK_ZIPEXPORT_FIXTURE = VkZipexportLayer()


VK_ZIPEXPORT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(VK_ZIPEXPORT_FIXTURE,),
    name="VkZipexportLayer:IntegrationTesting",
)


VK_ZIPEXPORT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VK_ZIPEXPORT_FIXTURE,),
    name="VkZipexportLayer:FunctionalTesting",
)


VK_ZIPEXPORT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        VK_ZIPEXPORT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="VkZipexportLayer:AcceptanceTesting",
)
