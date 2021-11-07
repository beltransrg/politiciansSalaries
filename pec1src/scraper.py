from selenium import webdriver
import time
from datetime import datetime
import writer

last_active_page = ''

def process_person_in_new_tab(id, url):

    #id
    
    # Open a new window
    driver.execute_script("window.open('');")

    # Switch to the new window
    driver.switch_to.window(driver.window_handles[1])
    driver.get(url)
    time.sleep(1)

    # Variable att contain the attributes of each person
    att =[]
    
    #id
    att.append(id)

    # nombre
    title = driver.find_element_by_xpath('//h1').text
    att.append(title)
    
    # cargo (job_title) /   partido (affiliation)
    c_person = driver.find_element_by_xpath("//div[@id='content']/div[@class='c-person']//h2").text.splitlines()
    if len(c_person) == 3:
        active = 0
        job_title = c_person[1] 
        affiliation = c_person[2] 
    else:
        active = 1
        job_title = c_person[0]
        affiliation = c_person[1]         
     
    att.append(active)
    att.append(job_title)
    att.append(affiliation)

    # fecha nacimiento

    # institucion

    # biografia

    # historico (V2?)

    # foto (V2?) => aqui parece que hay derechos y demas

    # bruto anual
    salary =driver.find_element_by_xpath("//div[@id='comparator']")
    salary = salary.text.replace('COMPARADOR','').split()[0]
    att.append(salary)
    
    #fecha de extracción
    today = datetime.today().strftime('%Y-%m-%d')
    att.append(today)

    

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
    i = 0
    if active_page.text != last_active_page: 

        print(f"Processing page {active_page.text}")
        last_active_page = active_page.text
        persons = driver.find_elements_by_class_name('e-result')
        print(len(persons))
        
        # looping over persons
        for person in persons:
            i += 1
            #product_name = result.text
            link = person.find_element_by_tag_name('a')
            url_link = link.get_attribute("href")
            process_person_in_new_tab(i,url_link)
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
headerList=["Id","Name","Active","JobTitle","Affiliation","Salary","Date"]
politicianList.append(headerList)

#Descomentar i para scripear todas las páginas
j=0
# processing one page (TODO loop)
while process_page():
    
    # next page
    next_button_selector = '#advanced-search > section.b-results > div.e-pagination > div > div > div > div > a.next'
    next_button = driver.find_element_by_css_selector(next_button_selector)
    next_button.click()
    time.sleep(2)
    j = j+1
    if j == 1: break

print("quitting")
driver.quit()
writer.write_file(politicianList)
