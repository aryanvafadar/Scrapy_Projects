import scrapy


class SnowySpider(scrapy.Spider):
    name = "snowy"
    allowed_domains = ["www.sourceboards.com"]
    start_urls = ["https://www.sourceboards.com/collections/snowboards?filter.v.availability=1"]

    # The parse function is automatically called as soon as our spider begins crawling
    def parse(self, response):
        
        retry_after = response.headers.get(b'Retry-After')
        if retry_after:
            self.logger.info(f"Server asked us to retry after {retry_after.decode()} seconds")
        
        # Once the function is called, the first thing we want to do is grab our list of products
        snowboards = response.xpath("//li[@class='grid__item']")
            
        # for each snowboard in our snowboards list, go into each snowboard and grab the required information
        for snowboard in snowboards:
            
            # get the relative url for the snowboard
            relative_snowboard_url = snowboard.xpath(".//h3/a/@href").get()
            main_url = "https://www.sourceboards.com"
            
            # Create the full url
            full_board_url = f"{main_url}{relative_snowboard_url}"
            
            # Once the full URL is created, go into each snowboard and pull the important information using a separate parsing function
            yield response.follow(full_board_url, self.parse_each_snowboard)
            
        # Once we are done iterating through each snowboard in the list of snowboards, we'll move onto the next page of the website and scrape a new list of snowboards
        
        # get the next page url
        next_page_url = response.xpath("//ul[contains(@class, 'pagination__list')]/li[last()]/a/@href").get()
    
        # if next page url exists, go to the next page and call the parse function again
        if next_page_url is not None:
            
            # create the full url
            main_url = "https://www.sourceboards.com/"
            full_url = f"{main_url}{next_page_url}"
            
            # After the full url is constructed, go to it and parse the new list of snowboards
            yield response.follow(full_url, self.parse)
            
    
    # This function is called during the parse function, and is used to go into each snowboard and retrieve the information we need        
    def parse_each_snowboard(self, response):
        
        # get all the rows of the table
        table_rows = response.xpath(".//table[contains(@class,'section-table')]//tr")
        
        # Create a dictionary of headers -> values with normalized lowercase dict keys
        table_data = {}
        
        # iterate through the table_rows and append to the table data dictionary
        for row in table_rows:
            key = row.xpath("normalize-space(./td[contains(@class,'first-column')])").get()
            value = row.xpath("normalize-space(./td[contains(@class,'second-column')])").get()
            
            # if both the key and value exist, append to the dictionary
            if key and value:
                table_data[key.strip().lower()] = value.strip()
        
        # Yield the data
        yield {
            'product_url': response.url,
            'product_name': response.xpath(".//h1/text()").get(),
            'item_number': response.xpath(".//p[contains(@class, 'product__sku')]/span/following-sibling::text()").get().strip(),
            'price': response.xpath("//span[contains(@class, 'price-item--regular')]/text()").get().strip(),
            'personality': table_data.get('personality/response'),
            'skill_level': table_data.get('rider skill level'),
            'board_shape': table_data.get('shape'),
            'terrain': table_data.get('terrain'),
            'flex_rating': table_data.get('flex rating'),
        }
        