from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import re
import pandas as pd
import time

def set_web_driver(headless_option):
    options = Options()
    if headless_option=='y':
        options.add_argument("--headless=new")
    
    return webdriver.Chrome(options=options)

def manage_specific_popup(driver, x_path):
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, x_path))).click()
    except:
        pass

def manage_generic_popup(driver):
    try:
        driver.find_element(By.XPATH, "//button[contains(text(), 'OK')]").click() 
    except:
        try:
            driver.find_element(By.XPATH, "//button[contains(text(), 'ok')]").click()
        except:
            try:
                driver.find_element(By.XPATH, "//button[contains(text(), 'Ok')]").click() 
            except:
                try:
                    driver.find_element(By.XPATH, "//button[contains(text(), 'Enter')]").click() 
                except:
                    pass

def get_elements_of_a_list_in_the_page(driver, x_path):
    return WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, x_path)))
    #return driver.find_elements(By.XPATH, x_path)

def get_item_name(item_parent, x_path):
    try:
        item_name = item_parent.find_element(By.XPATH, x_path).text
    except:
        item_name = ''
    return item_name
    
def get_item_location(item_parent, x_path):
    try:
        item_location = item_parent.find_element(By.XPATH, x_path).text
    except:
        item_location = ''
    return item_location

def get_item_website(item_parent, x_path):
    try:
        item_website = item_parent.find_element(By.XPATH, x_path).text
    except:
        item_website = ''
    return item_website

def click_on_a_link(item_parent, item_name_on_the_link):
    try:
        item_parent.find_element(By.PARTIAL_LINK_TEXT, str(item_name_on_the_link)).click()
    except:
        pass

# TODO: function to review
def check_and_switch_window(driver, original_window):
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break

def get_email_addresses(driver, x_path):
    email_pattern = r"([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})" # See and try out this pattern: [^@]+@[^@]+\.[^@]+
    try:
        email_address = driver.find_element(By.XPATH, x_path).get_attribute('href')
    except:
        try:
            email_address = driver.find_element(By.XPATH, x_path).text
        except:
            email_address = ''
    email_matches = re.findall(email_pattern, email_address)
    return '; '.join(email_matches)

def record_into_csv(data, lista_ospiti, conduttore, talk_show_name, csv_path):
    df = pd.read_csv(csv_path)
    new_entry = pd.DataFrame.from_dict({"Data": [data], "ListaOspiti": [lista_ospiti], "Conduttore": [conduttore], "Show": [talk_show_name]})
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(csv_path, index=False)

def check_and_close_window_handle_except_first(driver, original_window):
    while len(driver.window_handles)>1:
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
    else:
        pass
    driver.switch_to.window(original_window)