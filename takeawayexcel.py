from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time, csv
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


driver = webdriver.Chrome(ChromeDriverManager().install())
time.sleep(2)
web_page = input('Please, paste the website link which do you want to scrape?: ')
name_the_file = input('Please, write the name for the excel/csv file: ')

driver.get(web_page)
driver.maximize_window()
time.sleep(3)

populaire_names = driver.find_elements(By.CLASS_NAME, '_50YZr.CgiCq')

count_populaire_names = len(populaire_names)*6
y = 1000

for timer in range(0, count_populaire_names):
    driver.execute_script("window.scrollTo(0, " + str(y) + ")")
    new_height = driver.execute_script("return document.body.scrollHeight")
    y += 300
    time.sleep(1)




populare_section = driver.find_elements(By.CLASS_NAME, '_2q59Cu._2-ueMg')
headings = driver.find_elements(By.CLASS_NAME, '_3hLchg')

populaire = driver.find_element(By.XPATH, '//*[@id="page"]/div[2]/section/div[1]/div[3]/section/section[1]/div[2]')
elements = populaire.find_elements(By.CLASS_NAME, '_1sMed._1wlHd.Yc8ZH._1VvW7.hzg-6')


heading_names = []
headings_length = len(populaire_names)
all_numbers_of_chars = []

for i in populare_section:
    element = i.find_elements(By.CLASS_NAME, '_1qJsB')
    all_numbers_of_chars.append(len(element))

for i in populaire_names:
    heading_names.append(i.text)

for i in headings:
    element = i.find_elements(By.CLASS_NAME, '_2TWTUN')
    all_numbers_of_chars.append(len(element))


total_categories = sum([[s] * n for s, n in zip(heading_names, all_numbers_of_chars)], [])




items = driver.find_elements(By.CLASS_NAME, '_1sMed._1wlHd.Yc8ZH._1VvW7.hzg-6')
populaire_list = []


for item in items:
    populaire_dict = {}

    position = items.index(item)
    populaire_dict['Category'] = total_categories[position]

    populaire_dict['Product'] = ''
    populaire_dict['Description'] = ''
    populaire_dict['Choix_de'] = ''
    populaire_dict['Price'] = ''
    for number in range(0, headings_length-1):
        try:
            chapter = item.find_elements(By.CLASS_NAME, '_50YZr._3hlni')[number]
            populaire_dict['Product'] = chapter.text
            description = item.find_elements(By.CLASS_NAME, '_2GljJ')[number]
            populaire_dict['Description'] = description.text

        except IndexError:
            pass

    choices_of = item.find_elements(By.CLASS_NAME, '_3jA7k')
    for choice_of in choices_of:
        populaire_dict['Choix_de'] = choice_of.text
    prices = item.find_elements(By.CLASS_NAME, '_2PRj3E')
    for price in prices:
        x = price.text
        y = x.replace('€ ', '')
        z = y.replace(',', '.')
        populaire_dict['Price'] = z
    populaire_list.append(populaire_dict)

df = pd.DataFrame(populaire_list)
writer = pd.ExcelWriter(f'{name_the_file}.xlsx')
df.to_excel(writer, sheet_name='welcome', index=False, encoding='utf8')
writer.save()

driver.quit()


























