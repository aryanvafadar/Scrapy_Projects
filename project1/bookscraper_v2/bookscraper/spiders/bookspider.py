import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/index.html"]

    # The parse function gets called once the response comes back
    # This function gets updated to allow us to extract all the necessary information we need
    def parse(self, response):
        
        # There are two different urls to reference in our function
        main_url = "https://books.toscrape.com/"
        partial_url = "https://books.toscrape.com/catalogue/"
        
        # Get our list of books from the response. Do not add getall() otherwise it will turn the the variable into a str instead of a Scrapy Selector Object
        books = response.xpath("//article[@class='product_pod']")
        
        # loop through each book in our books variable. And Yield the the results. Yield is similar to return, but the function does not end like return does
        for book in books:
            
            # go inside of each book
            # check if catalogue exists in the relative book url or not. then construct the full url
            book_relative_url =  book.xpath(".//h3/a/@href").get()
            if 'catalogue' in book_relative_url:
                full_book_url = f"{main_url}{book_relative_url}"
            else:
                full_book_url = f"{partial_url}{book_relative_url}"
                
            # Once the full url is contructed, go into each book
            yield response.follow(full_book_url, self.parse_current_book)
            
        # Once we're done looping, go to the next page 
        next_page = response.xpath("//li[contains(@class, 'next')]/a/@href").get()
        if next_page is not None: # if we reach the last page of the website, this will return None
            
            # We need to create the full url, as next_page is only the relative url
            # check if catalogue is in next_page
            if 'catalogue' in next_page:
                # Create the full url
                next_page_full_url = f"{main_url}{next_page}"
                
            # if catalogue is not in next_page, then create another url    
            else:
                # Create the full url
                next_page_full_url = f"{partial_url}{next_page}"
            
            # After the full url is constructed, go to the next page and call the self.parse function again
            yield response.follow(next_page_full_url, self.parse)

    def parse_current_book(self, response):
        
        # Get the Book Rating
        rating_class = response.xpath(".//p[contains(@class, 'star-rating')]/@class").get()
        if rating_class:
            book_rating = [value for value in rating_class.split() if value.lower() != 'star-rating']
            rating_value = book_rating[0]
        else:
            rating_value = 'N/A'
            
        # Select all rows in the striped table
        rows = response.xpath("//table[@class='table table-striped']/tr")

        # Build a dict of header → value with normalized lowercase keys
        table_data = {}
        for row in rows:
            key = row.xpath("./th/text()").get()
            val = row.xpath("./td/text()").get()
            if key and val:
                table_data[key.strip().lower()] = val.strip()
        
        yield {
            'book_title':         response.xpath(".//h1/text()").get(),
            'genre':              response.xpath(".//ul[contains(@class, 'breadcrumb')]/li[3]/a/text()").get(),
            'rating':             rating_value,
            'upc':                table_data.get('upc'), # Returns None by Default if the key does not exist
            'product_type':       table_data.get('product type'),
            'price':              response.xpath(".//p[@class='price_color']/text()").get(),
            'tax':                table_data.get('tax'),
            'number_of_reviews':  table_data.get('number of reviews'),
            'book_url':           response.url
        }
        
    
