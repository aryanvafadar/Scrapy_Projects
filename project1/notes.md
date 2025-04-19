**Step 1 - Creating a Project and Using the Scrapy Shell**

1. Staring a project: To start a new project, we write the following in the terminal: scrapy startproject {projectname}. In this case, we wrote **scrapy startproject bookscraper**.
2. Then, we need to go into the spiders folder and create a new spider. To create a new spider, we write the following in the terminal: scrapy genspider {spidername} {link of the website to scrape}. In this case, we wrote **scrapy genspider bookspider https://books.toscrape.com/index.html**
3. Once our spider is created, we run the command 'scrapy shell' in our terminal in order to retrieve the css selectors necessary to update our parse function.
4. Once our shell is initilized, we will fetch the target url by running the following command in the IPython Shell: fetch(url)
   - All of the results from our fetch(url) command will be returned and store in the 'response' variable.
   - By writing and executing 'response' in the terminal, we can return the status code. 200 = successful
5. Then, we ran the command: **books1 = response.xpath("//article[contains(@class, 'product-pod')]")** This retrieved all the books and stored them in the books1 variable.
   - We do not want to use .getall() here, as it will convert the variable to a str and not a Scrapy Selector Object.
6. We then created another variable titled **book_1**. This variable was created by running the command: book_1 = books[0]. We selected the first book that was previously returned in our list of books.
7. We used book_1 and various xpath's to find the necessary code commands to retrieve the content we need.

**Step 2 - Updating our Parse Function, Iterating through Subsequent Pages:**

1. Once we know the code commands we need to run to extract the necessary information, we update our parse function with these commands.
2. After our parse function has been completed, we can run our spider using the following command: **scrapy crawl {spider name}**. In our case, we used the command: scrapy crawl bookspider.
3. If our code is correct, the terminal should display many different messages showcasing success.
4. We then added additonal commands within the function to go to the next page. This was done using \*\*yield response.follow({full page url}, {callback function})
