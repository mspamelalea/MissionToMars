#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd 
import datetime as dt

def scrape_all():
    # Windows users - Make sure your chromedriver.exe is in the same folder as this program
    # executable_path = {'executable_path': 'chromedriver.exe'}
    # Initiate headless driver for deployement
    # browser = Browser('chrome', **executable_path, headless=False)
    browser = Browser("chrome", executable_path='chromedriver', headless=True)
    
    # Use the mars_news function to pull data
    news_title, news_paragraph = mars_news(browser)
    image1_title = hemisphere1_title(browser)
    # Run all the scraping functions and store results in a dictionary
    data = {"news_title": news_title,
            "news_paragraph": news_paragraph,
            "featured_image": featured_image(browser),
            "facts": mars_facts(),
            "last_modified": dt.datetime.now(),
            "hemisphere_one": hemisphere1_img(browser),
            "image_one_title": image1_title
    }
    #Stop the webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # ### Mars News Article Scraping

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # set up the HTML parser and convert html to soup object
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        #use the parent element to find the first <a> tag (.find) and save as "news title"
        news_title =slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    
    return news_title, news_p
# Original code would not work
# def featured_image(browser):
#     # ### Scrape Featured Image from JPL site

#     # Visit URL
#     url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
#     browser.visit(url)

#     # Find and click the full image button
#     full_image_elem = browser.find_by_id('full_image')

#     # Find the "more info" button and click it
#     browser.is_element_present_by_text('more info', wait_time=1)
#     more_info_elem = browser.links.find_by_partial_text('more info')

#     # Parse the resulting HTML with soup
#     html = browser.html
#     img_soup = BeautifulSoup(html, 'html.parser')
    
#     try:
#         # Find the relative image url
#         img_url_rel = img_soup.select_one('figure.lede a img').get("src")
     
#     except AttributeError:
#         return None

#     # Use the base URL to create an absolute URL
#     img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

#     return img_url

def featured_image(browser):
    # ### Scrape Featured Image from JPL site

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    try: 
        image_url = img_soup.find('div', class_ = 'carousel_items')('article')[0]['style'].\
        replace('background-image: url(','').replace(');', '')[1:-1]
    except AttributeError:
        return None

       # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{image_url}'

    return img_url

def mars_facts():
    # ### Scrape a table from Space-facts site

    # Visit URL and
    # scrape the entire table from website with Pandas
    # searches for and returns first table ([0]) found in the HTML
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    # the updated index will remain in place, without having to reassign the DataFrame to a new variable
    df.set_index('Description', inplace=True)

    #Convert dataframe to usable HTML
    return df.to_html()

def  hemisphere1_img(browser):
    # ### Scrape Featured Image from USGS site
    ### Get Mars Hemisphere images

    # Visit URL: USGS
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html= browser.html

    # Find the full image 
    imgs_soup = BeautifulSoup(html, 'html.parser')
    collapsible_results = imgs_soup.find('div', class_ = 'collapsible results')
    item_one = collapsible_results.find('div', class_ = 'item')('a')[1]['href']
 
    # Use the base URL to create an absolute URL
    item_one_url = f'https://astrogeology.usgs.gov{item_one}'

    # Go to the link and parse html 
    browser.visit(item_one_url)
    html= browser.html
    img1_soup = BeautifulSoup(html, 'html.parser')
    
    try: 
         # Find the relative image url
        img1_full_url = img1_soup.select_one('ul li a').get('href')
    except AttributeError:
        return None
    
    img1_full_url = f'{img1_full_url}'

    return img1_full_url

    
def hemisphere1_title(browser):
    # ### Scrape Featured Image from USGS site
    ### Get Mars Hemisphere images

    # Visit URL: USGS
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html= browser.html

    # Find   the full image button 
    imgs_soup = BeautifulSoup(html, 'html.parser')
    collapsible_results = imgs_soup.find('div', class_ = 'collapsible results')
    item_one = collapsible_results.find('div', class_ = 'item')('a')[1]['href']
 
    # Use the base URL to create an absolute URL
    item_one_url = f'https://astrogeology.usgs.gov{item_one}'
    item_one_url

    # Go to the link and parse html 
    browser.visit(item_one_url)
    html= browser.html
    img1_soup = BeautifulSoup(html, 'html.parser')

    image1_title = img1_soup.select('div', class_ = 'content')[0]('h2')[0].text
    return image1_title

if __name__ == "__main__":
    # If running as script, print scraped data 
    print(scrape_all())