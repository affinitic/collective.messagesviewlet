# -*- coding: utf-8 -*-

from Acquisition import aq_parent
from DateTime import DateTime

from plone import api
from plone.app.layout.navigation.defaultpage import isDefaultPage
from plone.app.layout.viewlets import ViewletBase
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.behavior.talcondition.utils import evaluateExpressionFor


class MessagesViewlet(ViewletBase):
    """This viewlet displays all messages from this product."""
    render = ViewPageTemplateFile('./messagesviewlet.pt')

    def __init__(self, context, request, view, manager=None):
        super(MessagesViewlet, self).__init__(context, request, view, manager=manager)
        self.portal = api.portal.get()

    def getAllMessages(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        now = DateTime()
        brains = catalog.searchResults(portal_type=['Message'],
                                       start={'query': now, 'range': 'max'},
                                       end={'query': now, 'range': 'min'},
                                       sort_on='getObjPositionInParent')
        messages = []
        for brain in brains:
            if brain.location == 'homepage':
                # Test if context is PloneSite or its default page
                if not IPloneSiteRoot.providedBy(self.context) and \
                        not isDefaultPage(self.portal, self.context):
                    continue
            obj = brain.getObject()
            # By default, expression is evaluated with context = (obj or obj.context).
            # We define obj.context to viewlet context to evaluate expression on viewlet context display.
            obj.context = self.context
            if not evaluateExpressionFor(obj):
                continue
            messages.append(brain.getObject())

        return messages
