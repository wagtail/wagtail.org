from bs4 import BeautifulSoup, NavigableString

from wagtail_content_import.parsers.base import DocumentParser


import mammoth


class DocxHTMLParser(DocumentParser):
    def __init__(self, document):
        self.document = document

    def close_paragraph(self, block, stream_data):
        if block:
            stream_data.append({'type': 'html', 'value': ''.join(block)})
        block.clear()
        return

    def parse(self):
        
        html = mammoth.convert_to_html(self.document).value

        soup = BeautifulSoup(html)

        stream_data = []

        # Run through contents and populate stream
        current_paragraph_block = []

        for tag in soup.body.recursiveChildGenerator():
            # Remove all inline styles and classes
            if hasattr(tag, 'attrs'):
                for attr in ['class', 'style']:
                    tag.attrs.pop(attr, None)

        title = ''

        for tag in soup.body.contents:
            if isinstance(tag, NavigableString):
                stream_data.append({'type': 'html', 'value': str(tag)})
            else:
                if tag.name == 'h1':
                    self.close_paragraph(current_paragraph_block, stream_data)
                    stream_data.append({'type': 'heading', 'value': tag.text})
                    if not title:
                        title = tag.text
                elif tag.name in ['h2', 'h3', 'h4', 'h5', 'h6']:
                    self.close_paragraph(current_paragraph_block, stream_data)
                    current_paragraph_block = ['<tag.name>{}</tag.name>'.format(tag.text)]
                elif tag.name == 'img':
                    # Break the paragraph and add an image
                    self.close_paragraph(current_paragraph_block, stream_data)
                    stream_data.append({'type': 'image', 'value': tag.get('src'), 'title': tag.get('alt', '')})
                elif tag.text:
                    current_paragraph_block.append(str(tag))

                if tag.find_all('img'):
                    # Break the paragraph and add images
                    self.close_paragraph(current_paragraph_block, stream_data)
                    for img in tag.find_all('img'):
                        stream_data.append({'type': 'image', 'value': img.get('src'), 'title': img.get('alt', '')})

            self.close_paragraph(current_paragraph_block, stream_data)

        return {
            'title': title,
            'elements': stream_data
        }
