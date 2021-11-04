from typing import Sized
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os
import csv

last_active_page = ''

def process_person_in_new_tab(url):

    # Open a new window
    driver.execute_script("window.open('');")

    # Switch to the new window
    driver.switch_to.window(driver.window_handles[1])
    driver.get(url)
    time.sleep(1)

    # TODO extract information from person
    att =[]
    # nombre
    title = driver.find_element_by_xpath('//h1').text
    att.append(title)
    # cargo (job_title)

    # partido (affiliation)

    # fecha nacimiento

    # institucion

    # biografia

    # historico (V2?)

    # foto (V2?) => aqui parece que hay derechos y demas

    # bruto anual
    salary =driver.find_element_by_xpath("//div[@id='comparator']")
    salary = salary.text.replace('COMPARADOR','').split()[0]
    att.append(salary)
    politicianList.append(att)

#get_attribute() to get value of input box
    
    # bruto mensual

    # close the active tab
    driver.close()

    # Switch back to the first tab
    driver.switch_to.window(driver.window_handles[0])

def process_page():

    # getting active page to check when the last page has been reached
    active_page_selector = '#advanced-search > section.b-results > div.e-pagination > div > div > div > div > ul > li.active'
    active_page = driver.find_element_by_css_selector(active_page_selector)
    global last_active_page
    if active_page.text != last_active_page: 

        print(f"Processing page {active_page.text}")
        last_active_page = active_page.text
        persons = driver.find_elements_by_class_name('e-result')
        print(len(persons))
        
        # looping over persons
        for person in persons:
            #product_name = result.text
            link = person.find_element_by_tag_name('a')
            url_link = link.get_attribute("href")
            process_person_in_new_tab(url_link)
            #print(url_link)

        # return value to keep going on
        return True
    else:
        print(f"Last page {active_page} has been reached")

        # return value to stop processsing
        return False

 


               

# does not work
# r = requests.get('https://transparentia.newtral.es/busqueda-avanzada?name=&inactive=true')
# soup = BeautifulSoup(r.text, 'lxml')
# print(soup.html)
# persons = soup.find_all('div', class_='e-result')
# print(persons)



# trying to use Selenium
print("initializing webdriver")
driver = webdriver.Firefox()

print("getting url")
url = 'https://transparentia.newtral.es/busqueda-avanzada?name=&inactive=true'
driver.get(url)

print("sleeping")
time.sleep(2)


politicianList = []
headerList=["Name","Salary"]
politicianList.append(headerList)

#Descomentar i para scripear todas las páginas
i = 0
# processing one page (TODO loop)
while process_page():
    
    # next page
    next_button_selector = '#advanced-search > section.b-results > div.e-pagination > div > div > div > div > a.next'
    next_button = driver.find_element_by_css_selector(next_button_selector)
    next_button.click()
    time.sleep(2)
    i = i+1
    if i == 2: break

print("quitting")
driver.quit()


filename = "politician_salaries.csv"

with open(filename, 'w', newline='') as csvFile:
  writer = csv.writer(csvFile)
  for politicianData in politicianList:
      writer.writerow(politicianData)
