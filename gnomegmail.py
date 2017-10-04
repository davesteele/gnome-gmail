#!/usr/bin/python3 -tt
#
# Copyright 2011-2014 David Steele <dsteele@gmail.com>
# This file is part of gnome-gmail
# Available under the terms of the GNU General Public License version 2
# or later
#
""" gnome-gmail
This script accepts an argument of a mailto url, and calls up an appropriate
GMail web page to handle the directive. It is intended to support GMail as a
GNOME Preferred Email application """

import sys
import webbrowser
import os
import os.path
import re
import textwrap
import locale
import gettext
import string
import json
import mimetypes
import random
import time
import subprocess
import shlex
import unicodedata
import argparse
from contextlib import contextmanager

from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from six.moves import urllib
from six.moves.configparser import SafeConfigParser

import gi
from gi.repository import Gio       # noqa

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk       # noqa

gi.require_version('Secret', '1')
from gi.repository import Secret    # noqa

gi.require_version('Notify', '0.7')
from gi.repository import Notify    # noqa

gi.require_version('Wnck', '3.0')
from gi.repository import Wnck      # noqa

try:
    locale.setlocale(locale.LC_ALL, '')
except locale.Error:
    locale.setlocale(locale.LC_CTYPE, "en_US.UTF-8")

gettext.textdomain("gnome-gmail")
_ = gettext.gettext

try:
    environ = os.environ['XDG_CURRENT_DESKTOP']
    environ = environ.split(':')[-1]
except:
    environ = 'GNOME'

config = None


class GGError(Exception):
    """ Gnome Gmail exception """
    def __init__(self, value):
        self.value = value
        super(GGError, self).__init__()

    def __str__(self):
        return repr(self.value)


@contextmanager
def nullfd(fd):
    saveout = os.dup(fd)
    os.close(fd)
    os.open(os.devnull, os.O_RDWR)
    try:
        yield
    finally:
        os.dup2(saveout, fd)


def set_as_default_mailer():
    if environ in ['GNOME', 'Unity']:
        for app in Gio.app_info_get_all_for_type("x-scheme-handler/mailto"):
            if app.get_id() == "gnome-gmail.desktop":
                app.set_as_default_for_type("x-scheme-handler/mailto")
    elif environ == 'KDE':
        cfgpath = os.path.expanduser('~/.kde/share/config/emaildefaults')
        with open(cfgpath, 'r') as cfp:
            cfglines = cfp.readlines()

        cfglines = [x for x in cfglines if 'EmailClient' not in x]

        outlines = []
        for line in cfglines:
            outlines.append(line)
            if 'PROFILE_Default' in line:
                outlines.append("EmailClient[$e]=/usr/bin/gnome-gmail %u\n")

        with open(cfgpath, 'w') as cfp:
            cfp.writelines(outlines)


def is_default_mailer():
    returnvalue = True

    if environ in ['GNOME', 'Unity']:
        mailer = Gio.app_info_get_default_for_type(
                    "x-scheme-handler/mailto",
                    True
                 )
        try:
            returnvalue = mailer.get_id() == "gnome-gmail.desktop"
        except AttributeError:
            pass
    elif environ == 'KDE':
        cfgpath = os.path.expanduser('~/.kde/share/config/emaildefaults')
        with open(cfgpath, 'r') as cfp:
            returnvalue = 'gnome-gmail' in cfp.read()

    return returnvalue


def browser():
    cmd = "xdg-settings get default-web-browser"
    brsr_name = subprocess.check_output(
        cmd.split(), universal_newlines=True).strip()

    browser = webbrowser.get()

    for candidate in webbrowser._tryorder:
        if candidate in brsr_name:
            browser = webbrowser.get(using=candidate)

    return customize_browser(browser)


def customize_browser(browser):

    argmap = {
        'Chrome': '--app=%s',
        'Konqueror': '',
        'Mozilla': '-new-window %s',
        'Galeon': '',
        'Opera': '',
        'Grail': '',
    }

    replace_args = config.get_str('browser_options')

    if replace_args:
        browser.remote_args = shlex.split(replace_args)
    else:
        try:
            std_args = argmap[type(browser).__name__]

            if std_args:
                browser.remote_args = shlex.split(std_args)

        except KeyError:
            pass

    return browser


class GMOauth():
    """oauth mechanism per
          https://developers.google.com/accounts/docs/OAuth2InstalledApp
        example at
          https://github.com/google/gmail-oauth2-tools/blob/master/python/oauth2.py
        Eg:
          (access, refresh) = GMOauth().generate_tokens( "user@gmail.com" )
    """

    def __init__(self):
        self.auth_endpoint = "https://accounts.google.com/o/oauth2/auth"
        self.token_endpoint = "https://accounts.google.com/o/oauth2/token"
        self.scope = "https://www.googleapis.com/auth/gmail.compose"
        self.client_id = "284739582412.apps.googleusercontent.com"
        self.client_secret = "EVt3cQrYlI_hZIt2McsPeqSp"

    def get_code(self, login_hint):
        s = string.ascii_letters + string.digits
        state = ''.join(random.sample(s, 10))

        args = {
                    "response_type": "code",
                    "client_id": self.client_id,
                    "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
                    "prompt": "consent",
                    "scope": self.scope,
                    "state": state,
                    "login_hint": login_hint,
               }

        code_url = "%s?%s" % (self.auth_endpoint, urllib.parse.urlencode(args))

        with nullfd(1), nullfd(2):
            browser().open(code_url, 1, True)

        now = time.time()

        while time.time() - now < 120:
            Gtk.main_iteration()
            screen = Wnck.Screen.get_default()
            if screen is None:  # Possible in non-X11, e.g. Wayland
                raise GGError(_("Could not access default screen"))
            screen.force_update()

            for win in screen.get_windows():
                m = re.search("state=%s.code=([^ ]+)" % state, win.get_name())
                if m:
                    win.close(time.time())

                    return m.group(1)

        raise GGError(_("Timeout getting OAuth authentication"))

    def get_token_dict(self, code):

        args = {
                    "code": code,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
                    "grant_type": "authorization_code",
               }

        try:
            token_page = urllib.request.urlopen(
                self.token_endpoint,
                urllib.parse.urlencode(args).encode("utf-8"))
        except urllib.error.HTTPError as e:
            token_page = e

        return(json.loads(token_page.read().decode("utf-8")))

    def get_access_from_refresh(self, refresh_token):

        args = {
             "refresh_token": refresh_token,
             "client_id": self.client_id,
             "client_secret": self.client_secret,
             "grant_type": "refresh_token",
          }

        try:
            token_page = urllib.request.urlopen(
                self.token_endpoint,
                urllib.parse.urlencode(args).encode("utf-8"))
        except urllib.error.HTTPError as e:
            token_page = e
        token_dict = json.loads(token_page.read().decode("utf-8"))

        if "access_token" in token_dict:
            return(token_dict["access_token"])
        else:
            return(None)

    def generate_tokens(self, login, refresh_token=None):
        """Generate an access token/refresh token pair for 'login' email
           account, using an optional refresh token.
           If refresh is not possible, the caller will be prompted for
           authentication via an internal browser window."""

        if refresh_token:
            access_token = self.get_access_from_refresh(refresh_token)
            if access_token:
                return((access_token, refresh_token))

        code = self.get_code(login)

        token_dict = self.get_token_dict(code)

        try:
            return((token_dict["access_token"], token_dict["refresh_token"]))
        except:
            # todo - replace with a GG exception
            return((None, None))

    def access_iter(self, access, refresh, login):
        if access:
            yield (access, refresh)

        if refresh:
            yield (self.get_access_from_refresh(refresh), refresh)

        yield self.generate_tokens(login)


class GMailAPI():
    """ Handle mailto URLs that include 'attach' fields by uploading the
    messages using the GMail API """

    def __init__(self, mail_dict):
        self.mail_dict = mail_dict

    def form_message(self):
        """ Form an RFC822 message, with an appropriate MIME attachment """

        msg = MIMEMultipart()

        for header in ("To", "Cc", "Bcc", "Subject",
                       "References", "In-Reply-To"):
            if header.lower() in self.mail_dict:
                msg[header] = self.mail_dict[header.lower()][0]

        try:
            fname = os.path.split(self.mail_dict["attach"][0])[1]

            if "subject" not in self.mail_dict:
                msg["Subject"] = _("Sending %s") % fname
        except KeyError:
            pass

        """ prepare preamble to be ascii encoded: bug #29 """
        """ normalization """
        preamble = unicodedata.normalize('NFKD', u"%s" % str(_("Mime message attached")))
        """ stripping of what is still ascii incompatible """
        preamble = preamble.encode('ascii', 'ignore').decode('ascii')
        msg.preamble = preamble

        try:
            body = self.mail_dict['body'][0]

            mimebody = MIMEMultipart('alternative')
            mimebody.attach(MIMEText(body))
            mimebody.attach(MIMEText(self.body2html(), 'html'))

            msg.attach(mimebody)

        except KeyError:
            pass

        try:
            for filename in self.mail_dict['attach']:
                attachment = self.file2mime(filename)
                msg.attach(attachment)
        except KeyError:
            pass

        self.message_text = msg.as_string()

    def file2mime(self, filename):
        if(filename.find("file://") == 0):
            filename = filename[7:]

        filepath = urllib.parse.urlsplit(filename).path

        if not os.path.isfile(filepath):
            raise GGError(_("File not found - %s") % filepath)

        ctype, encoding = mimetypes.guess_type(filepath)

        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'

        maintype, subtype = ctype.split('/', 1)

        with open(filepath, 'r' if maintype == 'text' else 'rb') as fp:
            attach_data = fp.read()

        if maintype == 'text':
            attachment = MIMEText(attach_data, _subtype=subtype)
        elif maintype == 'image':
            attachment = MIMEImage(attach_data, _subtype=subtype)
        elif maintype == 'audio':
            attachment = MIMEAudio(attach_data, _subtype=subtype)
        else:
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(attach_data)
            encoders.encode_base64(attachment)

        attachment.add_header(
                        'Content-Disposition', 'attachment',
                        filename=os.path.split(filename)[1]
        )

        return(attachment)

    def _convert_links(self, text):
        schemes = [
            'http', 'https', 'ftp', 'mailto',
            'about', 'chrome', 'bitcoin', 'callto', 'file', 'geo', 'git',
            'gtalk', 'irc', 'magnet', 'market', 'skype', 'ssh', 'webcal',
            'xmpp',
        ]
        rgx = "(?P<url>(%s):[^ \\),]+[^ \\)\\],\\.'\"])" % '|'.join(schemes)
        substr = '<a href="\\g<url>">\\g<url></a>'

        text = re.sub(rgx, substr, text)

        return text

    def body2html(self):

        htmlbody = self.mail_dict['body'][0]

#        htmlbody = htmlbody.replace('&', '&amp;')
        htmlbody = re.sub('>', '&gt;', htmlbody)
        htmlbody = re.sub('<', '&lt;', htmlbody)
        htmlbody = re.sub('\t', '&emsp;', htmlbody)

        htmlbody = self._convert_links(htmlbody)

        while "  " in htmlbody:
            htmlbody = re.sub("  ", "&nbsp; ", htmlbody)

        while "&nbsp; &nbsp;" in htmlbody:
            htmlbody = re.sub("&nbsp; &nbsp;", "&nbsp;&nbsp;&nbsp;", htmlbody)

        htmlbody = re.sub("\n", "<br>\n", htmlbody)

        htmlhdr = "<html>\n<head>\n</head>\n<body>\n"
        htmltail = "\n</body>\n</html>"
        htmltext = htmlhdr + htmlbody + htmltail

        return htmltext

    def _has_attachment(self):

        return('attach' in self.mail_dict)

    def _has_body(self):
        return('body' in self.mail_dict)

    def needs_api(self):

        return self._has_attachment() or self._has_body()

    def upload_mail(self, user, access_token):
        """ transfer the message to GMail Drafts folder, using the GMail API.
        Return a message ID that can be used to reference the mail via URL"""

        if access_token is None:
            raise GGError(_("Unable to authenticate with GMail"))

        url = ("https://www.googleapis.com/upload/gmail/v1/users/%s/drafts" +
               "?uploadType=media") % urllib.parse.quote(user)

        opener = urllib.request.build_opener(urllib.request.HTTPSHandler)
        request = urllib.request.Request(url, data=self.message_text)
        request.add_header('Content-Type', 'message/rfc822')
        request.add_header('Content-Length', str(len(self.message_text)))
        request.add_header('Authorization', "Bearer " + access_token)
        request.get_method = lambda: 'POST'

        try:
            urlfp = opener.open(request)
        except urllib.error.HTTPError as e:
            raise GGError(_("Error returned from the GMail API - %s - %s") %
                          (e.code, e.msg))

        result = urlfp.fp.read()
        self.resource = result
        json_result = json.loads(result.decode('utf-8'))
        id = json_result['message']['id']

        return id

    def send_mail(self, user, access_token):
        """ send the recently uploaded draft message"""

        url = "https://www.googleapis.com/gmail/v1/users/%s/drafts/send" \
              % urllib.parse.quote(user)

        opener = urllib.request.build_opener(urllib.request.HTTPSHandler)
        request = urllib.request.Request(url, data=self.resource)
        request.add_header('Content-Type', 'application/json')
        request.add_header('Content-Length', str(len(self.resource)))
        request.add_header('Authorization', "Bearer " + access_token)
        request.get_method = lambda: 'POST'

        try:
            urlfp = opener.open(request)
        except urllib.error.HTTPError as e:
            raise GGError(_("Error returned from the GMail API - %s - %s") %
                          (e.code, e.msg))


class GMailURL():
    """ Logic to convert a mailto link to an appropriate GMail URL, by
    any means necessary, including API uploads."""

    def __init__(self, mailto_url, from_address, message=None):
        self.mailto_url = mailto_url
        self.from_address = from_address
        self.message = message

        if self.mailto_url:
            self.mail_dict = self.mailto2dict()
        else:
            self.mail_dict = {}

    def mailto2dict(self):
        """ Convert a mailto: reference to a dictionary containing the
        message parts """
        # get the path string from the 'possible' mailto url
        usplit = urllib.parse.urlsplit(self.mailto_url, "mailto")

        path = usplit.path

        try:
            # for some reason, urlsplit is not splitting off the
            # query string.
            # do it here
            # ( address, qs ) = string.split( path, "?", 1 )
            (address, query_string) = path.split("?", 1)
        except ValueError:
            address = path

            query_string = usplit.query

        # For whatever reason, xdg-open 1.0.2 on Ubuntu 15 passes
        # "mailto:///email@address" so the path has a leading slash when
        # parsed by urlsplit.  Just trim off leading slashes; they're not
        # valid in email addresses anyway.
        address = re.sub("^/+", "", address)

        qsdict = urllib.parse.parse_qs(query_string)

        qsdict['to'] = [address]

        if 'attachment' in qsdict:
            qsdict['attach'] = qsdict['attachment']

        outdict = {}
        for (key, value) in qsdict.items():
            for i in range(0, len(value)):
                if key.lower() in ['to', 'cc', 'bcc', 'body']:
                    value[i] = urllib.parse.unquote(value[i])
                else:
                    value[i] = urllib.parse.unquote_plus(value[i])

            outdict[key.lower()] = value

        if 'su' in qsdict:
            outdict["subject"] = outdict["su"]

        return(outdict)

    def simple_gmail_url(self):
        """ url to use if there is no mailto url """

        return("https://mail.google.com/mail/b/%s" % self.from_address)

    def api_gmail_url(self, send=False):
        """ if the mailto refers to an attachment,
        use the GMail API to upload the file """

        api_url = "https://mail.google.com/mail/b/%s#drafts/" % \
                  self.from_address

        try:
            gm_api = GMailAPI(self.mail_dict)

            if self.message:
                gm_api.message_text = self.message
            else:
                gm_api.form_message()
        except OSError:
            GGError(_("Error creating message with attachment"))

        msg_id = None
        auth = GMOauth()
        keys = Oauth2Keyring(auth.scope)
        try:
            old_access, old_refresh = keys.getTokens(self.from_address)
        except GLib.Error:
            print("Error getting tokens from keyring")
            old_access = old_refresh = None

        error_str = ""
        for access, refresh in auth.access_iter(old_access, old_refresh,
                                                self.from_address):
            try:
                msg_id = gm_api.upload_mail(self.from_address, access)
                break
            except GGError as e:
                error_str = e.value

        if msg_id:
            if (old_access, old_refresh) != (access, refresh):
                try:
                    keys.setTokens(self.from_address, access, refresh)
                except GLib.Error:
                    print("Error saving tokens to keyring")

            if send:
                gm_api.send_mail(self.from_address, access)
        else:
            raise GGError(error_str)

        return(api_url + msg_id)

    def gmail_url(self, send):
        """ Return a GMail URL appropriate for the mailto handled
        by this instance """
        if(len(self.mailto_url) == 0 and not self.message):
            gmailurl = self.simple_gmail_url()
        else:
            gmailurl = self.api_gmail_url(send)

        return(gmailurl)


def getFromAddress(last_address, config, gladefile):
    class Handler:
        def __init__(self, fromInit, dlg):
            self.txtbox = builder.get_object("entryFrom")
            self.txtbox.set_activates_default(True)

            self.txtbox.set_property("text", fromInit)

            self.txt = None

            self.dlg = dlg

        def onOkClicked(self, button):
            self.txt = self.txtbox.get_property("text")
            self.dlg.hide()
            Gtk.main_quit()

        def onCancelClicked(self, button):
            self.txt = None
            self.dlg.hide()
            Gtk.main_quit()

        def onUserSelClose(self, foo):
            self.onCancelClicked(foo)

        def onDestroy(self, foo):
            self.onCancelClicked(foo)

    suppress_account_selection = config.get_bool('suppress_account_selection')
    if last_address and suppress_account_selection:
        return last_address

    dlgid = "user_select_dialog"

    builder = Gtk.Builder()
    builder.add_objects_from_file(gladefile, (dlgid, ))

    dlg = builder.get_object(dlgid)

    hdlr = Handler(last_address, dlg)
    builder.connect_signals(hdlr)

    dlg.show_all()

    Gtk.main()

    sup_acc_sel = builder.get_object(
                    "check_account_dont_ask_again").get_active()
    config.set_bool('suppress_account_selection', sup_acc_sel)

    return hdlr.txt


def getGoogleFromAddress(last_address, config, gladefile):
    retval = getFromAddress(last_address, config, gladefile)

    if retval and not re.search('@', retval):
        retval += "@gmail.com"

    return retval


def fromFromMessage(message):
    line = [x for x in message.split('\n') if 'FROM:' in x.upper()][0]
    email = line.split(' ')[-1]
    email = re.sub('[<>]', '', email)

    return email


class GgConfig(SafeConfigParser):
    def __init__(self, *args, **kwargs):

        self.fpath = os.path.expanduser(self.strip_kwarg(kwargs, 'fpath'))
        self.section = self.strip_kwarg(kwargs, 'section')
        initvals = self.strip_kwarg(kwargs, 'initvals')
        self.header = self.strip_kwarg(kwargs, 'header')

        SafeConfigParser.__init__(self, *args, **kwargs)

        self.add_section(self.section)

        for option in initvals:
            self.set(self.section, option, initvals[option])

        self.read(self.fpath)
        self.save()

    def strip_kwarg(self, kwargs, option):
        val = kwargs[option]
        kwargs.pop(option, None)
        return val

    def save(self):
        dir = os.path.dirname(self.fpath)

        if not os.path.exists(dir):
            os.makedirs(dir)

        with open(self.fpath, 'w') as fp:
            fp.write(self.header)
            fp.write("# Automatically updated file - comments stripped\n")
            self.write(fp)

    def _saveit(fp):
        def wrapper(inst, *args, **kwargs):
            retval = fp(inst, *args, **kwargs)
            inst.save()
            return retval
        return wrapper

    def get_str(self, option):
        return self.get(self.section, option)

    @_saveit
    def set_str(self, option, value):
        return self.set(self.section, option, value)

    def get_bool(self, option):
        return self.getboolean(self.section, option)

    @_saveit
    def set_bool(self, param, val):
        if isinstance(val, bool):
            val = '1' if val else '0'
        return self.set(self.section, param, val)


class Oauth2Keyring():
    # per
    # https://people.gnome.org/~stefw/libsecret-docs/py-examples.html#py-schema-example
    TOKEN_SCHEMA = Secret.Schema.new(
        'com.github.davesteele.oauth2',
        Secret.SchemaFlags.NONE,
        {
            "user":  Secret.SchemaAttributeType.STRING,
            "scope": Secret.SchemaAttributeType.STRING,
        }
    )

    def __init__(self, scope):
        self.scope = scope

    def encodeTokens(self, access_token, refresh_token):
        return "access:%s;refresh:%s" % (access_token, refresh_token)

    def decodeTokens(self, encode_str):
        match = re.search("^access:(.+);refresh:(.+)$", encode_str)

        if match:
            return match.group(1, 2)
        else:
            return (None, None)

    def getTokens(self, user):
        attributes = {
                         "user": user,
                         "scope": self.scope,
                     }

        password = Secret.password_lookup_sync(self.TOKEN_SCHEMA,
                                               attributes, None)

        if password:
            return self.decodeTokens(password)
        else:
            return (None, None)

    def setTokens(self, user, access_token, refresh_token):
        attributes = {
                         "user": user,
                         "scope": self.scope,
                     }

        Secret.password_store_sync(
            self.TOKEN_SCHEMA, attributes,
            Secret.COLLECTION_DEFAULT,
            "Mail access to %s for %s" % (self.scope, user),
            self.encodeTokens(access_token, refresh_token),
            None
        )


def do_preferred(glade_file, config):

    class Handler:
        def onCancelClicked(self, button):
            Gtk.main_quit()

    dlgid = "preferred_app_dialog"

    builder = Gtk.Builder()
    builder.add_objects_from_file(glade_file, (dlgid, ))

    hdlr = Handler()
    builder.connect_signals(hdlr)

    response = builder.get_object(dlgid).run()

    preferred_setting = builder.get_object("check_dont_ask_again").get_active()
    config.set_bool('suppress_preferred', preferred_setting)

    if response == 1:
        set_as_default_mailer()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Send mail via the Gmail API and the browser interface.",
        usage="%(prog)s [-h|-q|[-s] <mailto>]",
        epilog=textwrap.dedent("""\
            The gnome-gmail utility will create an email message from the
            mailto argument, upload it to Gmail using the Gmail API, and open
            a browser window showing the Draft message. If necessary, it will
            display a dialog asking for the From address, and use the default
            browser to establish OAuth2 credentials. It's primary purpose is
            as a helper program to integrate the Gmail web interface with the
            desktop.
            """
        )
    )

    parser.add_argument(
        'mailto',
        nargs='?',
        default="",
        help="an RFC2368 mailto URL specifying the message to be sent",
    )

    parser.add_argument(
        '-q', '--quiet',
        action="store_true",
        help="determine if this should be the desktop mail handler, and exit",
    )

    parser.add_argument(
        '-s', '--send',
        action="store_true",
        help="actually send the draft. Otherwise, the draft is opened in a "
             "browser compose window",
    )

    parser.add_argument(
        '-r', '--rfc822',
        metavar="file",
        default=None,
        help="upload an RFC822-formatted message",
    )

    args = parser.parse_args()

    return args


def main():
    """ given an optional parameter of a valid mailto url, open an appropriate
    gmail web page """

    global config

    args = parse_args()

    header = textwrap.dedent("""\
        # GNOME Gmail Configuration
        #
        # suppress_preferred
        #     If True ('1', 'yes'...) don't ask if GNOME Gmail should be made
        #     the default mail program.
        # suppress_account_selection
        #     If True ('1', 'yes'...) don't ask account to use, if you have
        #         only one.
        # new_browser
        #     If True ('1', 'yes'...) forcedly open Gmail in a new browser
        #         window.
        # last_email
        #     The email account used for the last run. It is used to populate
        #     the account selection dialog. This is updated automatically.
        #
        # browser_options
        #     Replace the command line arguments used to call the browser. Note
        #     that these options are not portable acrosss browsers. '%s' is
        #     replaced with the url. '%action' is replaced with an option that
        #     that implements the 'new_browser' functionality. Default options
        #     are:
        #         Chrome - "%action %s"
        #         Mozilla - "-remote openurl(%s%action)"
        #         ...
        #
        """)
    config = GgConfig(
                fpath="~/.config/gnome-gmail/gnome-gmail.conf",
                section='gnome-gmail',
                initvals={
                    'suppress_preferred': '0',
                    'suppress_account_selection': '0',
                    'new_browser': '1',
                    'last_email': '',
                    'browser_options': '',
                },
                header=header,
             )

    # anyone know how to do this right?
    glade_suffix = "share/gnome-gmail/gnomegmail.glade"
    glade_file = os.path.join('/usr', glade_suffix)
    for gpath in [os.path.join(x, glade_suffix) for x in ['/usr/local']]:
        if os.path.isfile(gpath):
            glade_file = gpath

    if not is_default_mailer() \
            and not config.get_bool('suppress_preferred'):
        do_preferred(glade_file, config)

    # quiet mode, to set preferred app in postinstall
    if args.quiet:
        sys.exit(0)

    Notify.init("GNOME Gmail")

    from_address = None
    message = None
    if args.rfc822:
        message = open(args.rfc822, 'r').read()
        from_address = fromFromMessage(message)
    else:
        last_from = config.get_str('last_email')
        from_address = getGoogleFromAddress(last_from, config, glade_file)
        if from_address:
            config.set_str('last_email', from_address)

    try:
        gm_url = GMailURL(args.mailto, from_address, message)
        gmailurl = gm_url.gmail_url(args.send)
    except GGError as gerr:
        notice = Notify.Notification.new(
            "GNOME GMail",
            gerr.value,
            "dialog-information"
        )

        notice.show()
        time.sleep(5)
    else:
        if not args.send:
            new_browser = config.get_bool('new_browser')
            browser().open(gmailurl, new_browser, True)


if __name__ == "__main__":
    main()
