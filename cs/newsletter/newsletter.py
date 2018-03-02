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
from zope import schema


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
    text = schema.SourceText(title=_(u'Newsletter text'),
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
    <title>Newskampus</title>
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
    <body style="height: 100%;margin: 0;padding: 0;width: 100%;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <center>
            <table align="center" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;height: 100%;margin: 0;padding: 0;width: 100%;">
                <tr>
                    <td align="center" valign="top" id="bodyCell" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;height: 100%;margin: 0;padding: 0;width: 100%;">
                        <!-- BEGIN TEMPLATE // -->
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                            <tr>
                                <td align="center" valign="top" id="templateHeader" data-template-container="" style="background:#F7F7F7 url(" no-repeat="">
                                                <!--[if gte mso 9]>
                                                    <table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
                                                        <tr>
                                                            <td align="center" valign="top" width="600" style="width:600px;">
                                                <![endif]-->
                                                <table class="templateContainer" align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;max-width: 600px !important;">
                                                    <tr>
                                                        <td valign="top" class="headerContainer" style="background:transparent none no-repeat center/cover;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: transparent;background-image: none;background-repeat: no-repeat;background-position: center;background-size: cover;border-top: 0;border-bottom: 0;padding-top: 0;padding-bottom: 0;">
                                                            <table class="mcnImageBlock" border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width: 100%;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                <tbody class="mcnImageBlockOuter">
                                                                    <tr>
                                                                        <td valign="top" style="padding: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" class="mcnImageBlockInner">
                                                                            <table align="left" width="100%" border="0" cellpadding="0" cellspacing="0" class="mcnImageContentContainer" style="min-width: 100%;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td class="mcnImageContent" valign="top" style="padding-right: 9px;padding-left: 9px;padding-top: 0;padding-bottom: 0;text-align: center;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                                            <img class="mcnImage" align="center" alt="" src="https://euskampus.eus/newskampus.png" width="564" style="max-width: 1011px;padding-bottom: 0;display: inline !important;vertical-align: bottom;border: 0;height: auto;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;" />
                                                                                        </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </td>
                                                                    </tr>
                                                                    <!-- </tbody> -->
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                                <!--[if gte mso 9]>
                                            </td>
                                        </tr>
                                    </table>
                                    <![endif]-->
                                </td>
                            </tr>
'''

HTML_FOOTER = '''                         </table>
                        <!-- // END TEMPLATE -->
                    </td>
                </tr>
            </table>
        </center>
    </body>
</html> '''



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
        if context.image is None:
            return HTML_HEADER + context.text + HTML_FOOTER
        else:
            image_code_pre = '''<tr><td align="center" valign="top" id="templateHeader" data-template-container="" style="background:#F7F7F7 url(" no-repeat="">
                            <!--[if gte mso 9]>
                                <table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
                                    <tr>
                                        <td align="center" valign="top" width="600" style="width:600px;">
                            <![endif]-->
                            <table class="templateContainer" align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;max-width: 600px !important;">
                                <tr>
                                    <td valign="top" class="headerContainer" style="background:transparent none no-repeat center/cover;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: transparent;background-image: none;background-repeat: no-repeat;background-position: center;background-size: cover;border-top: 0;border-bottom: 0;padding-top: 0;padding-bottom: 0;">
                                        <table class="mcnImageBlock" border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width: 100%;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                            <tbody class="mcnImageBlockOuter">
                                                <tr>
                                                    <td valign="top" style="padding: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" class="mcnImageBlockInner">
                                                        <table align="left" width="100%" border="0" cellpadding="0" cellspacing="0" class="mcnImageContentContainer" style="min-width: 100%;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                            <tbody>
                                                                <tr>
                                                                    <td class="mcnImageContent" valign="top" style="padding-right: 9px;padding-left: 9px;padding-top: 0;padding-bottom: 0;text-align: center;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                        <img class="mcnImage" align="center" alt="" src="'''
            image_code_post = '''" width="564" style="max-width: 1011px;padding-bottom: 0;display: inline !important;vertical-align: bottom;border: 0;height: auto;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;" />
        </td>
    </tr>
</tbody>
</table>
</td>
</tr>
<!-- </tbody> -->
</tbody>
</table>
</td>
</tr>
</table>
<!--[if gte mso 9]>
</td>
</tr>
</table>
<![endif]-->
</td>'''
            image_url = context.absolute_url() + '/@@images/image/'
            return HTML_HEADER + image_code_pre + image_url + image_code_post + context.text + HTML_FOOTER


class NewsletterSendView(grok.View):
    grok.context(INewsletter)
    grok.name('send')
    grok.require('cmf.ModifyPortalContent')

    def update(self):
        if self.request.get('method', '') == 'POST':
            fr = self.request.get('from', 'nruiz@codesyntax.com')
            to = self.request.get('to', 'nruiz@codesyntax.com')
            cc = self.request.get('cc', [])
            subject = self.request.get('subject',
                'Newsletter subject')
            self.send(fr, to, cc, subject)

    def send(self, fr, to, cc, subject):
        context = aq_inner(self.context)

        data = HTML_HEADER + context.text + HTML_FOOTER
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
