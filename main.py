from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome import options
from selenium.webdriver.common.keys import Keys
import pandas as pd

# Disable geolocation
from selenium.webdriver.chrome.options import Options
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.geolocation" :2}
options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(options=options)

driver.get("https://ocs.ca/pages/store-locator")
print(driver.current_url)

# To go back, use driver.back()
# To go forward, use driver.forward()
# To refresh, use driver.refresh()
# To read page title, use driver.title

def agewall_bypass():
    dob_month = driver.find_element_by_id('dob__month')
    dob_month.send_keys('01011970')
    dob_month.send_keys(Keys.RETURN)

agewall_bypass()

store_pin_links = driver.find_elements_by_xpath('//*[@id="main"]/div[3]/div/div/div[1]/div[2]/div/div/div/div[1]/div[3]/div/div[3]/div')

store_data = []

for store_pin_link in store_pin_links:
    driver.execute_script('arguments[0].click();', store_pin_link)

    # Prevent "coming soon" shops from stopping the program
    try:
        store_details_link = driver.find_element_by_class_name('store-location-tile__more-details__store-details')
        driver.execute_script('arguments[0].click();', store_details_link)
    except Exception:
        continue

    store_details = driver.find_element_by_class_name('store-details')
    
    store_details_header = store_details.find_element_by_class_name('store-details__header')
    store_name = store_details_header.find_element_by_tag_name('h2').text

    store_details_info = store_details.find_element_by_class_name('store-details__info__contact__connect')

    try:
        phone_number = store_details_info.find_element_by_xpath('.//a[1]').text
        assert phone_number.replace('-', '').isdigit()
    except Exception:
        phone_number = 'none specified'

    try:
        email = store_details_info.find_element_by_xpath('.//p[1]/a[1]').text
        assert '@' in email
    except Exception:
        email = 'none specified'

    store_data.append({'name': store_name, 'email': email.lower(), 'phone_number': phone_number})
    print(store_name, email, phone_number)
    driver.execute_script('$("#modal_bye.modal__dismiss")[1].click()')

store_dataframe = pd.DataFrame(store_data)
print(store_dataframe)
print(store_dataframe['email'])
print(store_dataframe['phone_number'])

store_dataframe.to_csv('~/OCS_Stores.csv')