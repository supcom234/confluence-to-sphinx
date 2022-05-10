from bs4.element import Tag, NavigableString

class HTMLTag:

    @classmethod
    def has_tag(cls, tag: Tag, tag_name: str) -> bool:
        if not isinstance(tag, Tag):
            return False
        
        for child_tag in tag:
            if child_tag.name == tag_name:
                return True

        return False

    @classmethod
    def has_structured_macro(cls, tag: Tag) -> bool:
        return cls.has_tag(tag, "ac:structured-macro")

    @classmethod
    def has_rich_text_body(cls, tag: Tag) -> bool:
        return cls.has_tag(tag, "ac:rich-text-body")

    @classmethod
    def _is_tag(cls, tag: Tag, tag_type: str) -> bool:
        if not isinstance(tag, Tag):
            return False
        return tag.name == tag_type

    @classmethod
    def is_paragraph(cls, tag: Tag) -> bool:
        if cls.has_structured_macro(tag):
            return False
        return cls._is_tag(tag, "p")

    @classmethod
    def is_structured_macro(cls, tag: Tag) -> bool:
        return cls._is_tag(tag, "ac:structured-macro")

    @classmethod
    def is_rich_text_body(cls, tag: Tag) -> bool:
        return cls._is_tag(tag, "ac:rich-text-body")

    @classmethod
    def is_heading(cls, tag: Tag) -> bool:
        if cls._is_tag(tag, "h1") or cls._is_tag(tag, "h2") or cls._is_tag(tag, "h3") or cls._is_tag(tag, "h4"):
            return True
        return False

    @classmethod
    def is_span(cls, tag: Tag) -> bool:
        return cls._is_tag(tag, "span")

    @classmethod
    def is_strong(cls, tag: Tag) -> bool:
        return cls._is_tag(tag, "strong")
    
    @classmethod
    def is_underline(cls, tag: Tag) -> bool:
        return cls._is_tag(tag, "u")
        
    @classmethod
    def is_italics(cls, tag: Tag) -> bool:
        return cls._is_tag(tag, "em")

    @classmethod
    def is_break(cls, tag: Tag) -> bool:
        return cls._is_tag(tag, "br")

    @classmethod
    def is_table(cls, tag: Tag) -> bool:
        return cls._is_tag(tag, "table")

    @classmethod
    def is_ordered_list(cls, tag: Tag) -> bool:
        return cls._is_tag(tag, "ol")

    @classmethod
    def is_unordered_list(cls, tag: Tag) -> bool:
        return cls._is_tag(tag, "ul")

    @classmethod
    def is_image(cls, tag: Tag) -> bool:
        return cls._is_tag(tag, "ac:image")
    
    @classmethod
    def is_link(cls, tag: Tag) -> bool:
        return cls._is_tag(tag, "ac:link") or cls._is_tag(tag, "a")

    @classmethod
    def is_list_item(cls, tag: Tag) -> bool:
        return cls._is_tag(tag, "li")

    @classmethod
    def is_parent_a_macro_or_rich_text(cls, tag: Tag) -> bool:
        if tag.parent:
            if HTMLTag.is_rich_text_body(tag.parent) or HTMLTag.is_structured_macro(tag.parent):
                return True

            elif tag.parent.parent:
                if HTMLTag.is_rich_text_body(tag.parent.parent) or HTMLTag.is_structured_macro(tag.parent.parent):
                    return True
        return False    