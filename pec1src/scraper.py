from selenium import webdriver
import time
from datetime import datetime
import writer

last_active_page = ''

from selenium.common.exceptions import NoSuchElementException        
def get_value_by_selector(driver, selector):
    try:
        return driver.find_element_by_css_selector(selector).text
    except NoSuchElementException:
        return None

def get_value_by_xpath(driver, xpath):
    try:
        return driver.find_element_by_xpath(xpath).text
    except NoSuchElementException:
        return None

def process_person_in_new_tab(id, url):

    # Open a new window
    driver.execute_script("window.open('');")

    # Switch to the new window
    driver.switch_to.window(driver.window_handles[1])
    driver.get(url)
    time.sleep(1)

    try:
        
        # Variable att contain the attributes of each person
        att =[]
        
        # id
        att.append(id)

        # fecha de extracción
        today = datetime.today().strftime('%d-%m-%Y')
        att.append(today)

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

        # institucion
        institution = get_value_by_selector(driver, '.location > dd:nth-child(2) > span:nth-child(1)')
        att.append(institution)

        # bruto anual
        salary = driver.find_element_by_xpath("//div[@id='comparator']")
        salary = salary.text.replace('COMPARADOR','').split()[0]
        att.append(salary)
        
        # bruto mensual (y desglose)
        salary_month = get_value_by_xpath(driver, '*//tr/th[contains(text(),"Salario bruto mensual")]/following-sibling::td')    
        salary_month_base = get_value_by_xpath(driver, '*//tr/th[contains(text(),"Salario base")]/following-sibling::td')
        salary_month_supplement = get_value_by_xpath(driver, '*//tr/th[contains(text(),"Suplementos")]/following-sibling::td')
        salary_month_diets = get_value_by_xpath(driver, '*//tr/th[contains(text(),"Dietas")]/following-sibling::td')
        # nos quedamos sólo con los números
        if salary_month:
                salary_month = salary_month.split()[0]
        if salary_month_base:
                salary_month_base = salary_month_base.split()[0]
        if salary_month_supplement:
                salary_month_supplement = salary_month_supplement.split()[0]
        if salary_month_diets:
                salary_month_diets = salary_month_diets.split()[0]

        att.append(salary_month)
        att.append(salary_month_base)
        att.append(salary_month_supplement)
        att.append(salary_month_diets)

        # fecha nacimiento
        birth_date = get_value_by_selector(driver, '#content > div > section.b-bio > div > div > div > div.col-12.col-lg-4.col-xl-3.offset-xl-1.float-lg-right > div > dl.date > dd')
        att.append(birth_date)

        # biografia
        #biography = get_value_by_selector(driver, '#content > div > section.b-bio > div > div > div > div.col-12.col-lg-8 > div > p')
        #att.append(biography)

        # historico (V2?)

        # foto (V2?) => aqui parece que hay derechos y demas

        politicianList.append(att)

    except:
        print(f"Error on {url}")

    

    # close the active tab
    driver.close()

    # Switch back to the first tab
    driver.switch_to.window(driver.window_handles[0])

person_idx = 0
def process_page(page_idx):

    # uncomment if skipping pages
    # if page_idx < 400:
    #     return True

    # getting active page to check when the last page has been reached
    active_page_selector = '#advanced-search > section.b-results > div.e-pagination > div > div > div > div > ul > li.active'
    active_page = driver.find_element_by_css_selector(active_page_selector)
    global last_active_page
    global person_idx
    if active_page.text != last_active_page: 

        print(f"Processing page {active_page.text}")
        last_active_page = active_page.text
        try:
            persons = driver.find_elements_by_class_name('e-result')
        except Exception:
            print("Error to get e-result container ... retrying")
            time.sleep(3)
            try:
                persons = driver.find_elements_by_class_name('e-result')
            except Exception:
                # doing nothing, just protecting
                print("[again] Error to get e-result container ... let's get next page")
                persons = None
        
        # looping over persons
        if persons:
            for person in persons:
                person_idx += 1
                try:
                    link = person.find_element_by_tag_name('a')
                    url_link = link.get_attribute("href")
                    process_person_in_new_tab(person_idx,url_link)
                except:
                    kk = 2

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



# trying to use Selenium => initializing
print("initializing webdriver")
driver = webdriver.Firefox()

print("getting url")
url = 'https://transparentia.newtral.es/busqueda-avanzada?name=&inactive=true'
driver.get(url)

print("sleeping")
time.sleep(2)

politicianList = []
headerList = ["Id", "Date", "Name", "Active", "JobTitle", "Affiliation", "Institution", "GrossSalary_Year", "GrossSalary_Month", "GrossSalary_Month_Base", "GrossSalary_Month_Supplement", "GrossSalary_Month_Diets", "BirthDate"]
politicianList.append(headerList)

#Descomentar i para scripear todas las páginas
j=0
# processing one page (TODO loop)
while process_page(j):
    
    # next page
    next_button_selector = '#advanced-search > section.b-results > div.e-pagination > div > div > div > div > a.next'
    next_button = driver.find_element_by_css_selector(next_button_selector)
    next_button.click()
    time.sleep(2)
    j = j+1
    #if j == 1: break

    # descargar cada 10 paginas
    if j > 0 and (j % 10 == 0) and (len(politicianList) > 2):
        print(f"flushing politicians until page {j}")
        writer.write_file_batch(politicianList, j)
        politicianList = []

print("quitting")
driver.quit()
writer.write_file(politicianList)
