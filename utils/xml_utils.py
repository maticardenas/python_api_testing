from lxml import etree

def get_xml_etree(text: str) -> etree._Element:
    return etree.fromstring(bytes(text, encoding='utf8'))