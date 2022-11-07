import glob, os, ebooklib, textwrap
from ebooklib import epub
from lxml import html

class Book():
    def __init__(self, page=0) -> None:
        self.page = page
        self.book_page = []
        self.title = ''
        
        # self.split_text_for_tg(self.read_book_file())

    def _strip_html(self, string: str) -> str:
        """ Strip all html tags """
        return str(html.fromstring(string).text_content())

    def read_book_file(self) -> str:
        """ Reads last .epub and returns text from it"""

        list_of_files = glob.glob('./documents/*.epub') 
        latest_file = max(list_of_files, key=os.path.getctime)

        book = epub.read_epub(latest_file)
        self.title = book.get_metadata('DC', 'title')
        
        book_text = ''
        
        for doc in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            text = self._strip_html(doc.get_body_content()) 
            book_text += text
            
        # print(book_text)
        return book_text
    
    def split_text_for_tg(self, book_text:str) -> str:
        """ Gets first chunk of text in size of 4096 and returns it"""
        book_text_list = textwrap.wrap(book_text, width=2000)
        # for i in book_text_list:
        #     print(i)
        #     print(f'{len(i)}##############################\n\n')
        self.book_page = book_text_list
    
    def next_page(self):
        if self.is_first_page():
            page = self.book_page[self.page]
            self.page += 1
            return page
        else:
            self.page += 1
            return self.book_page[self.page]
             

    def prev_page(self):
        self.page -= 1
        page = self.book_page[self.page]
        return page 
    
    def is_first_page(self):
        if self.page == 0: return True
        else: return False
    
    def is_last_page(self):
        if self.page == len(self.book_page) - 1:
            return True
        else: 
            return False

if __name__ == '__main__':
    b = Book()
    # b.split_text_for_tg(b.read_book_file())
    print(b.title)