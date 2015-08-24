# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.messagesviewlet


class CollectiveMessagesviewletLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.messagesviewlet)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.messagesviewlet:default')


COLLECTIVE_MESSAGESVIEWLET_FIXTURE = CollectiveMessagesviewletLayer()


COLLECTIVE_MESSAGESVIEWLET_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_MESSAGESVIEWLET_FIXTURE,),
    name='CollectiveMessagesviewletLayer:IntegrationTesting'
)


COLLECTIVE_MESSAGESVIEWLET_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_MESSAGESVIEWLET_FIXTURE,),
    name='CollectiveMessagesviewletLayer:FunctionalTesting'
)


COLLECTIVE_MESSAGESVIEWLET_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_MESSAGESVIEWLET_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveMessagesviewletLayer:AcceptanceTesting'
)