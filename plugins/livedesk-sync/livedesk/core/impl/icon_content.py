'''
Created on August 19, 2013

@package: livedesk-sync
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Martin Saturka

Content for icons of collaborators of chained blogs.
'''

import socket
import logging
from urllib.request import urlopen
from ally.api.model import Content
from urllib.error import HTTPError

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class ChainedIconContent(Content):
    '''
    Simple remote icon content taking
    '''

    inner = {}

    def setIconInfo(self, contentURL, fileName):
        '''
        Initialize the content.

        @param contentURL: string
            The URL of the icon to be downloaded.
        @param fileName: string
            The name of file under that the icon should be saved.
        '''
        self.inner['url'] = contentURL
        self.inner['response'] = None
        self.name = fileName
        self.charSet = 'binary'
        self.type = 'image'
        self.length = 0

    def read(self, nbytes=None):
        '''
        @see: Content.read
        '''
        if not self.inner['response']:
            try: self.inner['response'] = urlopen(self.inner['url'])
            except (HTTPError, socket.error) as e:
                log.error('Can not read icon image data %s' % e)
                return
            if not self.inner['response']:
                log.error('Can not read icon image data %s' % e)
                return

            self.type = self.inner['response'].getheader('Content-Type')
            if not self.type:
                self.type = 'image'
            self.length = self.inner['response'].getheader('Content-Length')
            if not self.length:
                self.length = 0

        if self.inner['response'].closed:
            return ''

        if nbytes:
            return self.inner['response'].read(nbytes)

        return self.inner['response'].read()

    def next(self):
        '''
        @see: Content.next
        '''
        return None
