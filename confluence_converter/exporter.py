import json
import time
import os

from atlassian import Confluence
from datetime import datetime, timedelta
from time import sleep
from typing import List, Union, Dict

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
ACCEPT_ENCODING = 'gzip, deflate, br'
ACCEPT_LANG = 'en-US,en;q=0.9'
HOST = 'confluence.di2e.net'
ORIGIN = 'https://confluence.di2e.net'

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../"


class PageNotFound(Exception):
    pass


CONFLUENCE_URL = "https://confluence.di2e.net"
CONFLUENCE_USERNAME = "david.navarro"
CONFLUENCE_PASSWORD = ""
CONFLUENCE_SPACE = "THISISCVAH"
CONFLUENCE_SAMPLE = "v3.7 Deployable Interceptor Platform (DIP) Troubleshooting Guide"
# CONFLUENCE_SAMPLE = "Test Page Delete Later For prototype"


class MyConfluenceExporter(Confluence):

    def __init__(self):
        super().__init__(url=CONFLUENCE_URL,
                         username=CONFLUENCE_USERNAME,
                         password=CONFLUENCE_PASSWORD)

        self._page_title = CONFLUENCE_SAMPLE
        self._page_id = self.get_page_id(CONFLUENCE_SPACE, self._page_title)
        self._page = self.get_page_by_id(self._page_id, expand="body.storage")
        self._attachments = self.get_attachments_from_content(self._page_id)

    def _download_attachment(self, url: str, filepath: str):
        with self._session.request(
                method='GET',
                url=url,
                # headers=headers,
                timeout=self.timeout,
                verify=self.verify_ssl,
                stream=True
            ) as response:
                response.raise_for_status()
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

                print("Successfully downloaded attachement to {}".format(filepath))

    @property
    def current_page(self):
        return self._page

    @property
    def current_page_content(self):
        return self._page['body']['storage']['value']

    @property
    def current_page_title(self):
        return self._page_title     

    def download_image(self, filename: str):
        for item in self._attachments['results']:
            if item["title"] == filename:
                item["_links"]["download"]
                self._download_attachment(self.url + item["_links"]["download"], SCRIPT_DIR + "/sphinx/images/" + filename)