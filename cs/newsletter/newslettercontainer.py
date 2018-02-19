from Acquisition import aq_inner
from plone.app.contentlisting.interfaces import IContentListing
from zope.annotation.interfaces import IAnnotations
from DateTime import DateTime
from zope.site.hooks import getSite
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from five import grok
from plone.directives import dexterity
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
from cs.newsletter import MessageFactory as _
from plone.app.textfield.value import RichTextValue
from plone.i18n.normalizer import idnormalizer


# Interface class; used to define content-type schema.
class INewsletterContainer(form.Schema, IImageScaleTraversable):
    """
    NewsletterContainer
    """
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/newslettercontainer.xml to define the content type
    # and add directives here as necessary.


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.
class NewsletterContainer(dexterity.Container):
    grok.implements(INewsletterContainer)
    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# templates called newslettercontainerview.pt .
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@view" appended unless specified otherwise
# using grok.name below.
# This will make this view the default view for your content-type
grok.templatedir('templates')


class NewsletterContainerView(grok.View):
    grok.context(INewsletterContainer)
    grok.require('zope2.View')
    grok.name('view')

    def get_bulletins(self):
        context = aq_inner(self.context)
        brains = context.getFolderContents(dict(portal_type='Bulletin'))
        return IContentListing(brains)


class NewsletterPrepareView(grok.View):
    grok.context(INewsletterContainer)
    grok.name('prepare')
    grok.require('cmf.ModifyPortalContent')

    html = u''
    _temp = ViewPageTemplateFile('templates/newsletter.pt')

    def update(self):
        self.request.set('disable_plone.rightcolumn', 1)
        if self.request.get('method', '') == 'POST':
            bulletin = self.save()
            message = _('Gorde da eskatutako elementuak dituen buletina. Hemen bere edukia')
            IStatusMessage(self.request).add(message)
            return self.request.response.redirect(bulletin.absolute_url())

    def get_newsitems(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        brains = catalog(portal_type='News Item',
                         review_state='published',
                         sort_on='effective',
                         sort_order='reverse',

                         )
        return IContentListing(brains)

    def get_events(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        date_range_query = {'query': DateTime(),
            'range': 'min'
        }
        brains = catalog(portal_type='Event',
                         review_state='published',
                         sort_on='start',
                         end=date_range_query,
                         )
        return IContentListing(brains)

    def save(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        newsitems = []
        for newsitem in self.request.get('newsitems', []):
            items = catalog(id=newsitem, portal_type='News Item')
            if items:
                newsitems.append(items[0].getObject())
        events = []
        site = getSite()
        for event in self.request.get('events', []):
            items = catalog(id=event, portal_type='Event')
            if items:
                events.append(items[0].getObject())
        subject = u'Newskampus {0}'.format(DateTime().strftime('%Y-%m-%d-%H%M%S'))
        subject_title = u'Newskampus {0}'.format(DateTime().strftime('%Y-%m-%d'))
        date = DateTime().strftime('%Y-%m-%d')
        toLocalizedTime = context.restrictedTraverse('@@plone').toLocalizedTime
        html = self._temp(self.request,
            **dict(newsitems=newsitems,
                events=events,
                subject=subject,
                date=date,
                toLocalizedTime=toLocalizedTime))

        id = idnormalizer.normalize(subject)
        buletin = context.invokeFactory(id=id,
                                        title=subject_title,
                                        type_name='Newsletter'
                    )
        buletin_object = context.get(buletin)
        buletin_object.text = RichTextValue(html, 'text/html', 'text/html')
        return buletin_object
