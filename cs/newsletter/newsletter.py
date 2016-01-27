from plone.app.textfield import RichText
from five import grok
from plone.directives import dexterity
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
from cs.newsletter import MessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage
from cs.htmlmailer.mailer import create_html_mail
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName


# Interface class; used to define content-type schema.
class INewsletter(form.Schema, IImageScaleTraversable):
    """
    Newsletter
    """
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/newsletter.xml to define the content type
    # and add directives here as necessary.
    text = RichText(title=_(u'Newsletter text'),
        required=False,
        )

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.
class Newsletter(dexterity.Item):
    grok.implements(INewsletter)
    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# templates called newsletterview.pt .
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@view" appended unless specified otherwise
# using grok.name below.
# This will make this view the default view for your content-type

grok.templatedir('templates')

HTML_HEADER = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="en"><head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Bertsozale elkartearen boletina</title>
    <style>
    body{
        font-family: Arial, Helvetica, sans-serif;
    }
    a:hover {
        text-decoration: underline !important;
    }
    td.promocell p {
        color:#e4e4e4;
        font-size:16px;
        line-height:26px;
        font-family: Arial, Helvetica, sans-serif;
        margin-top:0;
        margin-bottom:0;
        padding-top:0;
        padding-bottom:0px;
        font-weight:normal;
    }
    td.contentblock h4 {
        color:#C54815 !important;
        font-size:16px;
        line-height:24px;
        font-family: Arial, Helvetica, sans-serif;
        margin-top:0;
        margin-bottom:10px;
        padding-top:0;
        padding-bottom:0;
        font-weight:normal;
    }
    td.contentblock h4 a {
        color: #C54815;
        text-decoration:none;
    }
    td.contentblock p {
        color:#333;
        font-size:14px;
        line-height:19px;
        font-family: Arial, Helvetica, sans-serif;
        margin-top:0;
        margin-bottom:12px;
        padding-top:0;
        padding-bottom:0;
        font-weight:normal;
    }
    td.contentblock p a {
        color:#C54815;
        text-decoration:none;
    }

    p.more {
        font-size: 11px !important;
    }

    p.place{
        text-transform: uppercase;
        font-weight: bold !important;
    }

    .agendaevent p, .agendaevent h4 {
        margin:0 !important;
    }

    @media only screen and (max-device-width: 480px) {
       div[class="header"] {
          font-size: 16px !important;
      }
      table[class="table"], td[class="cell"] {
          width: 300px !important;
      }
      table[class="promotable"], td[class="promocell"] {
          width: 325px !important;
      }
      td[class="footershow"] {
          width: 300px !important;
      }
      table[class="hide"], img[class="hide"], td[class="hide"] {
          display: none !important;
      }
      img[class="divider"] {
          height: 1px !important;
      }
      td[class="logocell"] {
        padding-top: 15px !important;
        padding-left: 15px !important;
        width: 300px !important;
    }
    img[id="screenshot"] {
      width: 325px !important;
      height: 127px !important;
  }
}
img[class="galleryimage"] {
  width: 53px !important;
  height: 53px !important;
}
p[class="reminder"] {
    font-size: 11px !important;
}


h4[class="secondary"] {
    line-height: 22px !important;
    margin-bottom: 5px !important;
    font-size: 18px !important;
}
}
</style>
</head>
<body topmargin="0" leftmargin="0" style="-webkit-font-smoothing: antialiased;width:100% !important;background:#e4e4e4;-webkit-text-size-adjust:none;" bgcolor="#e4e4e4" marginheight="0" marginwidth="0">

'''

HTML_FOOTER = ''' </body></html> '''


class NewsletterView(grok.View):
    grok.context(INewsletter)
    grok.name('view')
    grok.require('zope2.View')

    def update(self):
        self.request.set('disable_plone.rightcolumn', 1)


class NewsletterPreview(grok.View):
    grok.context(INewsletter)
    grok.name('preview')
    grok.require('zope2.View')

    def render(self):
        context = aq_inner(self.context)
        return HTML_HEADER + context.text.output + HTML_FOOTER


class NewsletterSendView(grok.View):
    grok.context(INewsletter)
    grok.name('send')
    grok.require('cmf.ModifyPortalContent')

    def update(self):
        if self.request.get('method', '') == 'POST':
            fr = self.request.get('from', 'libargutxi@gmail.com')
            to = self.request.get('to', 'libargutxi@gmail.com')
            cc = self.request.get('cc', [])
            subject = self.request.get('subject',
                'Newsletter subject')
            self.send(fr, to, cc, subject)

    def send(self, fr, to, cc, subject):
        context = aq_inner(self.context)

        data = HTML_HEADER + context.text.output + HTML_FOOTER
        mail = create_html_mail(subject,
                         data.decode('utf-8'),
                         from_addr=fr,
                         to_addr=to,
                         cc_addrs=cc)
        mailhost = getToolByName(context, 'MailHost')
        mailhost.send(mail.as_string())
        message = _('Bidalketa ondo egin da.')
        IStatusMessage(self.request).add(message)
        return self.request.response.redirect(context.absolute_url())