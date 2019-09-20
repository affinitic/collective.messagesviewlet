# -*- coding: utf-8 -*-

from collective.messagesviewlet import HAS_PLONE_5
from plone import api
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import interfaces as Plone
from utils import _
from utils import add_message
from zope.interface import implementer


FOLDER = "messages-config"


def post_install(context):
    """Post install script."""
    if context.readDataFile('collectivemessagesviewlet_default.txt') is None:
        return
    language_tool = api.portal.get_tool('portal_languages')
    langs = language_tool.supported_langs
    for lang in langs:
        site = context.getSite().get(lang, context.getSite())
        if not site.get(FOLDER):
            types = getToolByName(site, 'portal_types')
            types.getTypeInfo('MessagesConfig').global_allow = True
            behavior = ISelectableConstrainTypes(site)
            list_addable_type = behavior.getImmediatelyAddableTypes()
            if "MessagesConfig" not in list_addable_type:
                list_addable_type.append("MessagesConfig")
            set_addable_types(site, list_addable_type)
            container = api.content.create(site,
                                           "MessagesConfig",
                                           id=FOLDER,
                                           title=_('Messages viewlet settings', context=site)
                                           )
            excl = IExcludeFromNavigation(container)
            excl.exclude_from_nav = True

            types.getTypeInfo('MessagesConfig').global_allow = False


@implementer(Plone.INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Do not show on Plone's list of installable profiles."""
        return [
            u'collective.messagesviewlet:install-base',
        ]


def add_default_messages(context):
    """ Add maintenance messages that can be activated when necessary """
    if context.readDataFile('collectivemessagesviewlet_messages.txt') is None:
        return
    resource = 'resource'
    if HAS_PLONE_5:
        resource = 'plone'
    site = context.getSite()
    add_message('maintenance-soon', _('maintenance_soon_tit', context=site), _('maintenance_soon_txt', context=site),
                msg_type='significant', can_hide=True, req_roles=['Authenticated'])
    add_message('maintenance-now', _('maintenance_now_tit', context=site), _('maintenance_now_txt', context=site),
                msg_type='warning', can_hide=False, req_roles=['Anonymous'])
    add_message('test-site', _('test_site_tit', context=site), _('test_site_txt', context=site),
                msg_type='warning', can_hide=False)
    add_message('browser-warning', _('bad_browser_tit', context=site),
                _('bad_browser_txt ${resource}', mapping={'resource': resource}, context=site),
                msg_type='warning', can_hide=False,
                tal_condition="python:'Firefox' not in context.REQUEST.get('HTTP_USER_AGENT')")
    add_message('browser-warning-ff-chrome', _('bad_browser_ff_chrome_tit', context=site),
                _('bad_browser_ff_chrome_txt ${resource}', mapping={'resource': resource}, context=site),
                msg_type='warning', can_hide=False,
                tal_condition="python: 'Firefox' not in context.REQUEST.get('HTTP_USER_AGENT') and "
                "'Chrome' not in context.REQUEST.get('HTTP_USER_AGENT')")


def set_addable_types(obj, types):
    """Set the allowed types on an object"""
    behavior = ISelectableConstrainTypes(obj)
    behavior.setConstrainTypesMode(1)
    behavior.setLocallyAllowedTypes(types)
    behavior.setImmediatelyAddableTypes(types)
