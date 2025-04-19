import scrapy


class SnowySpider(scrapy.Spider):
    name = "snowy"
    allowed_domains = ["www.sourceboards.com"]
    start_urls = ["https://www.sourceboards.com/collections/snowboards"]

    # The parse function is automatically called as soon as our spider begins crawling
    def parse(self, response):
        
        # Once the function is called, the first thing we want to do is grab our list of products
        snowboards = response.xpath("//li[@class='grid__item']")
        
        # Once we get our list of snowboards, we want to loop through each one and yield the important information``
        for board in snowboards:
            
            yield {
                'product_name': board.xpath("normalize-space(.//h3[@class='card__heading h5']/a/text())").get(),
                'price': board.xpath("normalize-space(.//div[contains(@class,'price__regular')]//span[contains(@class,'price-item--regular')])"
                ).get(),
                'sale_price': board.xpath("normalize-space(.//div[contains(@class, 'price__sale')]//span[contains(@class, 'price-item--sale')]/text())").get(),
                'url': board.xpath("normalize-space(.//h3[contains(@class, 'card__heading h5')]/a/@href)").get()
            }
            
        # Once we are done iterating through the first/current page, then we want to move onto the next page
        next_page_btn = response.xpath("//ul[contains(@class, 'pagination__list')]/li[last()]/a/@href").get() # this grabs the partial url  
        main_url = 'https://www.sourceboards.com/'
        
        # if next_page_btn is not none, then go to the next page
        if next_page_btn is not None:
            
            # construct full url
            full_url = f"{main_url}{next_page_btn}"
            
            # After the full url is constructed, go to the next page and scrape the next page
            yield response.follow(full_url, self.parse)
        