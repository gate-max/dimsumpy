
# STANDARD LIBRARIES
from http.client import HTTPResponse
from io import StringIO
import shutil
from typing import Dict, List
import urllib

# THIRD PARTY LIBRARIES
from bs4 import BeautifulSoup
from bs4.element import ResultSet
import pandas
from pandas.core.frame import DataFrame
import requests
from requests.models import Response


from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_selenium_text(url: str, headless: bool = True, timeout: int = 10) -> str:
    """
    Selenium will emulate a real browser to open web pages.

    Args:
        url (str): The URL of the webpage to fetch.
        headless (bool): Whether to run the browser in headless mode (default: True).
        timeout (int): Maximum wait time in seconds for the page to load (default: 10).

    Returns:
        str: The HTML source code of the webpage.

    driver.quit() Ensure the browser quits even if an error occurs
    """
    options = Options()
    if headless:
        options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    
    driver.get(url)
        
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
    html_source = driver.page_source
    
    driver.quit()

    return html_source




default_headers: Dict[str, str] = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.89 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}



def get_html_text(url: str) -> str :
    """ 
    * INDEPENDENT *
    IMPORTS: requests

    yahoo finance requires Accept field headers
    """
    html_response: Response = requests.get(url, headers=default_headers)
    return html_response.text


def get_html_soup(url: str) -> BeautifulSoup :
    """ 
    DEPENDS ON: get_html_text()
    IMPORTS: beautifulsoup4
    """
    html_text: str = get_html_text(url)
    soup: BeautifulSoup = BeautifulSoup(html_text, 'html.parser')
    return soup


def get_html_dataframes(url: str, header=None) -> List[DataFrame]:
    """
    * INDEPENDENT *
    IMPORTS: beautifulsoup4, pandas, requests

    https://google.com   (has <table>)
    https://yahoo.com   (no <table>)
    https://googel.com   (INVALID SSL cert)

    If there is non <table> tag, soup_tables will be just be empty ResultRet [], soup.find_all() function is safe.
    
    I MUST ensure html_text has a <table> tag, otherwise pandas.read_html will have No tables found error.

    for the header keyword argument, the default is None, that is no header row, if I want to have the first row as header row, I could write header=0) 
    """
    html_text: str = get_html_text(url)
    soup: BeautifulSoup = BeautifulSoup(html_text, 'html.parser')
    soup_tables: ResultSet = soup.find_all('table')
    dataframes: List[DataFrame] = pandas.read_html(StringIO(html_text), header=header) if soup_tables else []
    return dataframes



def get_urllib_response(url: str) -> HTTPResponse :
    """ 
    * INDEPENDENT *
    IMPORTS: urllib
    """
    req = urllib.request.Request(url, headers=default_headers)
    with urllib.request.urlopen(req) as response:
        return response
    

def get_urllib_text(url: str) -> str :
    """ 
    * INDEPENDENT *
    IMPORTS: urllib
    """
    req = urllib.request.Request(url, headers=default_headers)
    with urllib.request.urlopen(req) as response:
        return response.read().decode('utf-8') 
    

def save_urllib_file(url: str, output: str='file.txt') -> None:
    """
    * INDEPENDENT *
    IMPORTS: shutil, urllib
    """
    req = urllib.request.Request(url, headers=_headers)
    with urllib.request.urlopen(req) as response, open(output, 'wb') as f:
        shutil.copyfileobj(response, f)
        
    

def get_csv_dataframe(url: str, header=None) -> DataFrame :
    """ 
    DEPENDS ON: get_urllib_text()
    IMPORTS: pandas, io
    """
    text: str = get_urllib_text(url)
    df = pandas.read_csv(StringIO(text), header=header)
    return df


def test1():
    """
    
    """
    x = 'https://finance.yahoo.com/quote/NVDA/options?date=1734652800'
    print(x)




if __name__ == '__main__':
    test1()