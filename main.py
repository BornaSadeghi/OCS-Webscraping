from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import pandas as pd

driver = Chrome()

driver.get("https://ocs.ca/pages/store-locator")
print(driver.current_url)
driver.maximize_window()

# To go back, use driver.back()
# To go forward, use driver.forward()
# To refresh, use driver.refresh()
# To read page title, use driver.title

def agewall_bypass():
    dob_month = driver.find_element_by_id('dob__month')
    dob_month.send_keys('01011970')
    dob_month.send_keys(Keys.RETURN)

agewall_bypass()

# Click "See all stores" button
see_all_stores_link = driver.find_element_by_xpath("//*[contains(text(), 'See all stores')]")
see_all_stores_link.click()

store_details_links = driver.find_elements_by_class_name('store-location-tile__more-details__store-details')

store_data = []

for store_details_link in store_details_links:
    store_details_link.click()
    store_details = driver.find_element_by_class_name('store-details')
    
    store_details_header = store_details.find_element_by_class_name('store-details__header')
    store_name = store_details_header.find_element_by_tag_name('h2').text

    store_details_info = store_details.find_element_by_class_name('store-details__info__contact__connect')

    phone_number = store_details_info.find_element_by_xpath('.//a[1]').text
    email = store_details_info.find_element_by_xpath('.//p[1]/a[1]').text

    if not '@' in email:
        email = 'none'
    if not phone_number.replace('-', '').isdigit():
        phone_number = 'none'

    store_data.append({'name': store_name, 'email': email.lower(), 'phone_number': phone_number})
    driver.execute_script('$("#modal_bye.modal__dismiss")[1].click()')

store_dataframe = pd.DataFrame(store_data)
print(store_dataframe)
print(store_dataframe['email'])
print(store_dataframe['phone_number'])

store_dataframe.to_csv('~/OCS_Stores.csv')