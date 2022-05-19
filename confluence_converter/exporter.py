from atlassian import Confluence
from confluence_converter import PROJECT_ROOT_DIR
from confluence_converter.config_util import ConfigManager
from typing import Dict


class PageNotFound(Exception):
    pass


class ConfluencePage:
    
    def __init__(self, id: str, title: str, 
                 content: Dict, attachments: Dict):
        self.id = id
        self.title = title
        self.content = content
        self.attachments = attachments

    @property
    def content_body(self):
        return self.content['body']['storage']['value']

    @property
    def title_filename(self):
        """
        Converts a title to all lower case with underscores instead of spaces.
        """        
        ret_val = self.title
        return ret_val.replace(" ", "_").lower()


class MyConfluenceExporter(Confluence):

    def __init__(self, config: ConfigManager):
        if config is None:
            return
        self._config = config
        super().__init__(url=config.confluence_url,
                         username=config.confluence_username,
                         password=config.confluence_password)
    
    def page_iterator(self) -> ConfluencePage:
        for title in self._config.confluence_pages:
            id = self.get_page_id(self._config.confluence_space, title)
            content = self.get_page_by_id(id, expand="body.storage")
            attachments = self.get_attachments_from_content(id)

            yield ConfluencePage(id, title, content, attachments)

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

                print("Successfully downloaded attachment to {}".format(filepath))

    def download_image(self, filename: str, page: ConfluencePage):
        for item in page.attachments['results']:
            if filename.replace("\\", "") == item["title"]:
                item["_links"]["download"]
                self._download_attachment(self.url + item["_links"]["download"], PROJECT_ROOT_DIR + "/sphinx/images/" + item["title"])