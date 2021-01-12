from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time

CHROME_DRIVER_PATH = "/YOUR DRIVER PATH HERE"
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

GOOGLE_FORM = "YOUR GOOGLE FORM HERE"

my_espc_dunfermline = "https://espc.com/properties?locations=kinross-and-west-fife_dunfermline&maxprice=225000&ptype=house"

response = requests.get(my_espc_dunfermline)
data = response.text
soup = BeautifulSoup(data, "html.parser")
homes = soup.select(".infoWrap a")

home_links = []
prices = []
addresses = []
for home in homes[::2]:# had to filter out the Nones as they werent recognized by equivalency statements
    href = home.get("href")
    home_links.append(f"http://espc.com/{href}")
    price = home.find(class_="price").text
    prices.append(price)
    address = home.find(name='span', style="white-space:nowrap").text
    addresses.append(address)

# The time.sleep() is inserted to simulate a person filling out the form, otherwise google blocked my attempts
for num in range(len(prices)):
    driver.get(GOOGLE_FORM)
    time.sleep(2)
    question_address = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    question_price = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    question_link = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')

    question_address.send_keys(addresses[num])
    time.sleep(3)
    question_price.send_keys(prices[num])
    time.sleep(3)
    question_link.send_keys(home_links[num])
    time.sleep(3)
    submit.click()
