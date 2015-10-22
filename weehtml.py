# -*- coding: utf-8 -*-
#
# weehtml.py
# Copyright (c) 2015 hrubi <hrubi@hrubi.cz>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


SCRIPT_NAME = 'weehtml'
SCRIPT_AUTHOR = 'hrubi'
SCRIPT_VERSION = '0.0.0'
SCRIPT_LICENSE = 'MIT'
SCRIPT_DESC = 'Convert HTML messages to plaintext'

try:
    import weechat
    import html2text
    import re
    IMPORT_OK = True
except ImportError as error:
    IMPORT_OK = False
    if str(error).find('weechat') != -1:
        print('This script must be run under WeeChat.')
        print('Get WeeChat at http://www.weechat.org.')
    else:
        weechat.prnt('', '{0}: {1}'.format([SCRIPT_NAME, error]))


def cb_irc_in_privmsg(data, signal, server, irc_cmd):
    try:
        return format_privmsg(irc_cmd)
    except Exception:
        weechat.prnt(
            '',
            'Error: %s cannot parse message "%s"' % (SCRIPT_NAME, irc_cmd))
        return irc_cmd


def format_privmsg(privmsg):
    '''Takes IRC command line and outputs the same line with formatted
    message.'''

    # see: https://tools.ietf.org/html/rfc2812
    privmsg_re = '^(?P<privmsg_start>:.*? PRIVMSG .*? :?)(?P<text>.*)$'
    m = re.match(privmsg_re, privmsg, re.IGNORECASE)
    if m is None:
        raise Exception('Unparseable PRIVMSG')

    privmsg_start = m.group('privmsg_start')
    text = m.group('text')
    formatted_text = format_text(text)
    formatted_privmsg = '%s%s' % (privmsg_start, formatted_text)
    return formatted_privmsg


def format_text(msg):
    h = html2text.HTML2Text()
    h.images_to_alt = True
    h.body_width = 0
    return h.handle(msg.decode('utf-8'))


def main():
    '''Sets up weechat hooks.'''
    weechat.hook_modifier(
        'irc_in_privmsg',
        'cb_irc_in_privmsg',
        ''
    )

if __name__ == '__main__' and IMPORT_OK and weechat.register(
    SCRIPT_NAME,
    SCRIPT_AUTHOR,
    SCRIPT_VERSION,
    SCRIPT_LICENSE,
    SCRIPT_DESC,
    '',
    ''
):
    main()
