import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/index.html"]

    # The parse function gets called once the response comes back
    # This function gets updated to allow us to extract all the necessary information we need
    def parse(self, response):
        
        # Get our list of books from the response. Do not add getall() otherwise it will turn the the variable into a str instead of a Scrapy Selector Object
        books = response.xpath("//article[@class='product_pod']")
        
        # loop through each book in our books variable. And Yield the the results. Yield is similar to return, but the function does not end like return does
        for book in books:
            yield {
                'title': book.xpath(".//h3/a/@title").get(),
                'price': book.xpath(".//p[contains(@class, 'price_color')]/text()").get(),
                'availability': book.xpath("normalize-space(.//p[contains(@class, 'instock') and contains(@class, 'availability')])").get(),
                'url': book.xpath(".//h3/a/@href").get(),
            }
            
        # Once we're done looping, go to the next page 
        next_page = response.xpath("//li[contains(@class, 'next')]/a/@href").get()
        main_url = "https://books.toscrape.com/"
        partial_url = "https://books.toscrape.com/catalogue/"
        
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
