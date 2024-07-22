from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from general_scraping_methods import *

website = "https://www.la7.it/otto-e-mezzo/rivedila7?page="
csv_path = "ospiti_puntate.csv"
anchor_name = 'Lilli Gruber'
show_name = 'Otto e Mezzo'

for n in range(0, 3):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(website+str(n))
    items = get_elements_of_a_list_in_the_page(driver=driver, x_path="//div[@class='view-content clearfix']/div")
    for s in items:
        data_puntata = get_item_name(item_parent=s, x_path=".//div[@class='data']")
        click_on_a_link(item_parent=s, item_name_on_the_link=data_puntata)
        lista_ospiti = driver.find_element(By.XPATH, "//div/div/p").text
        conduttore = anchor_name
        record_into_csv(data_puntata, lista_ospiti, conduttore, show_name, csv_path)
        driver.back()
    driver.close()