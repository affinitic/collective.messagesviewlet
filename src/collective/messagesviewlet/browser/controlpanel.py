# -*- coding: utf-8 -*-

from plone import api
from Products.Five import BrowserView


class MessagesViewletSettings(BrowserView):
    def __call__(self):
        language_tool = api.portal.get_tool('portal_languages')
        langs = language_tool.supported_langs
        url = '{0}/messages-config'.format(api.portal.get().absolute_url())
        if len(langs) > 1:
            current_lang = api.portal.get_current_language()[:2]
            root = api.portal.get().get(current_lang)
            if root.get("messages-config"):
                url = '{0}/{1}/messages-config'.format(api.portal.get().absolute_url(), current_lang)

        self.request.RESPONSE.redirect(url)
