import json
import time

from atlassian import Confluence
from datetime import datetime, timedelta
from time import sleep
from typing import List, Union, Dict

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
ACCEPT_ENCODING = 'gzip, deflate, br'
ACCEPT_LANG = 'en-US,en;q=0.9'
HOST = 'confluence.di2e.net'
ORIGIN = 'https://confluence.di2e.net'

class PageNotFound(Exception):
    pass


class MyConfluenceExporter(Confluence):

    def download_attachment(self, url: str, filepath: str):                
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

    