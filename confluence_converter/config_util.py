import getpass
import inspect
import yaml

from argparse import ArgumentParser, Namespace
from typing import List


class ConfigManager:

    def __init__(self, args: Namespace):
        """
        All members of this class are strings unless otherwise specified below.
        """
        yml = self._load_yaml(args.config_path)
        self.confluence_url = args.confluence_url if args.confluence_url is not None else yml["CONFLUENCE"]["URL"]
        self.confluence_space = args.confluence_space if args.confluence_space is not None else yml["CONFLUENCE"]["SPACE"]

        # Confluence_pages is a List
        self.confluence_pages = args.confluence_pages if args.confluence_pages is not None else yml["CONFLUENCE"]["PAGES"] # type: List
        self.confluence_username = args.confluence_username if args.confluence_username is not None else yml["CONFLUENCE"]["USERNAME"]
        self.confluence_password = args.confluence_password if args.confluence_password is not None else yml["CONFLUENCE"]["PASSWORD"]
        if self.confluence_password is None or len(self.confluence_password) == 0:
            self.confluence_password = getpass.getpass("Enter your confluence password: ")
    
    def __str__(self):
        my_str = "Config:"
        for member_name, member_value in inspect.getmembers(self, lambda a:(not inspect.ismethod(a))):
            if not member_name.startswith("_"):
                my_str += f"\n{member_name}: {str(member_value)}"
        return my_str

    def _load_yaml(self, file: str) -> dict:
        with open (file, 'r') as file:
            data = yaml.safe_load(file)
        return data

    @classmethod
    def setup_arg_parse_options(cls) -> Namespace:
        parser = ArgumentParser(
            description="This application is used to convert confluence documentation "
                        "to RST markup for the Sphinx document generator."
        )
        
        parser.add_argument(
            "-c",
            "--config",
            dest="config_path",
            required=False,
            nargs="*",
            default="config.yml",
            help="Builds a specified component."        
        )

        parser.add_argument(
            "-p",
            "--confluence-pages",
            dest="confluence_pages",
            nargs="*",
            help="The confluence pages to convert to RST markup."
        )

        parser.add_argument(
            "-u",
            "--confluence-url",
            dest="confluence_url",
            help="The confluence URL to get pages from."
        )

        parser.add_argument(
            "-s",
            "--confluence-space",
            dest="confluence_space",
            help="The confluence space to grab the pages from."
        )

        parser.add_argument(
            "-usr",
            "--confluence-username",
            dest="confluence_username",
            help="The confluence username."
        )

        parser.add_argument(
            "-pwd",
            "--confluence-password",
            dest="confluence_password",
            help="The confluence password."
        )
        
        # parser.add_argument(
        #     "-R",
        #     "--Recursive",
        #     action="store_true",
        #     dest="recursive",
        #     help="Grabs all child pages if set under parent page."        
        # )

        return parser.parse_args()
