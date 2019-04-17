# -*- coding: utf-8 -*-
from collective.messagesviewlet.utils import get_messages_to_show
from plone import api
from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName


class LocalMessageViewlet(common.ViewletBase):

    index = ViewPageTemplateFile('local_message.pt')

    def get_messages(self):
        return get_messages_to_show(self.context)
        #catalog = getToolByName(self.context, 'portal_catalog')
        #results = catalog.searchResults(**{'portal_type': 'Message', 
        #    'review_state': 'activated'})
        #return results
