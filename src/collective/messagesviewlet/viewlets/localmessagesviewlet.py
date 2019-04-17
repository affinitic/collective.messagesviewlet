# -*- coding: utf-8 -*-
from collective.messagesviewlet.utils import get_messages_to_show
from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class LocalMessagesViewlet(common.ViewletBase):

    index = ViewPageTemplateFile('localmessagesviewlet.pt')

    def getAllMessages(self):
        return get_messages_to_show(self.context)
