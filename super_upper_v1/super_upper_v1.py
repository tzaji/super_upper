# GT Team present you SUPER UPPER!!!

# IMPORTS
import database as database_config
import create_and_update_database_and_its_tables as database_functions


# GLOBAL

SECTIONS_DICT = {
                1: {'name': 'fruits_vegtables', 'url': 'https://www.rami-levy.co.il/he/online/market/%D7%A4%D7%99%D7%A8%D7%95%D7%AA-%D7%95%D7%99%D7%A8%D7%A7%D7%95%D7%AA' },
                2: {'name': 'dairy_eggs_salad', 'url': 'https://www.rami-levy.co.il/he/online/market/%D7%97%D7%9C%D7%91-%D7%91%D7%99%D7%A6%D7%99%D7%9D-%D7%95%D7%A1%D7%9C%D7%98%D7%99%D7%9D' },
                3: {'name': 'meat_fish', 'url': 'https://www.rami-levy.co.il/he/online/market/%D7%91%D7%A9%D7%A8-%D7%95%D7%93%D7%92%D7%99%D7%9D' },
                4: {'name': 'organic_health', 'url': 'https://www.rami-levy.co.il/he/online/market/%D7%90%D7%95%D7%A8%D7%92%D7%A0%D7%99-%D7%95%D7%91%D7%A8%D7%99%D7%90%D7%95%D7%AA' },
                5: {'name': 'frozen', 'url': 'https://www.rami-levy.co.il/he/online/market/%D7%A7%D7%A4%D7%95%D7%90%D7%99%D7%9D' },
                6: {'name': 'cans_baking_cooking', 'url': 'https://www.rami-levy.co.il/he/online/market/%D7%A9%D7%99%D7%9E%D7%95%D7%A8%D7%99%D7%9D-%D7%91%D7%99%D7%A9%D7%95%D7%9C-%D7%95%D7%90%D7%A4%D7%99%D7%94' },
                7: {'name': 'beans_cereal', 'url': 'https://www.rami-levy.co.il/he/online/market/%D7%A7%D7%98%D7%A0%D7%99%D7%95%D7%AA-%D7%95%D7%93%D7%92%D7%A0%D7%99%D7%9D' },
                8: {'name': 'snacks', 'url': 'https://www.rami-levy.co.il/he/online/market/%D7%97%D7%98%D7%99%D7%A4%D7%99%D7%9D-%D7%95%D7%9E%D7%AA%D7%95%D7%A7%D7%99%D7%9D' },
                9: {'name': 'drinks', 'url': 'https://www.rami-levy.co.il/he/online/market/%D7%9E%D7%A9%D7%A7%D7%90%D7%95%D7%AA' },
                10: {'name': 'disposable', 'url': 'https://www.rami-levy.co.il/he/online/market/%D7%97%D7%93-%D7%A4%D7%A2%D7%9E%D7%99-%D7%95%D7%9E%D7%AA%D7%9B%D7%9C%D7%94' },
                11: {'name': 'house_pets', 'url': 'https://www.rami-levy.co.il/he/online/market/%D7%90%D7%97%D7%96%D7%A7%D7%AA-%D7%94%D7%91%D7%99%D7%AA-%D7%95%D7%91%D7%A2-%D7%97' },
                12: {'name': 'pharm_babies', 'url': 'https://www.rami-levy.co.il/he/online/market/%D7%A4%D7%90%D7%A8%D7%9D-%D7%95%D7%AA%D7%99%D7%A0%D7%95%D7%A7%D7%95%D7%AA' },
                13: {'name': 'pastry', 'url': 'https://www.rami-levy.co.il/he/online/market/%D7%9C%D7%97%D7%9D-%D7%9E%D7%90%D7%A4%D7%99%D7%9D-%D7%95%D7%94%D7%9E%D7%90%D7%A4%D7%99%D7%99%D7%94-%D7%94%D7%98%D7%A8%D7%99%D7%94' },
                 }



# Test: limit of item per group to scrap. For unlimited: -1.
test_limit_item_per_group = -1

# Scraping speed: 3 is the normal speed. We recommend to scrap between 1 and 5. Please enter your preference.
scrap_speed = 3

def search_id(url, section_name, speed, scrape_tag_path='//*[@id]', scrape_tag_atribute='id', scrape_tag_name='item',  scrolling_times=10, sleeping_time=5):
    """
    this function receive section URL and return list of all section's id-s (item numbers).
    :param url_section:
    :return: list_id_str
    """

    # IMPORTS
    from seleniumwire import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    import time

    # PARAMETERS
    svc = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=svc)
    driver.maximize_window()

    # VARIABLE INITIATION
    id_list = []
    print(f'>> {section_name} id searching started \n')

    # GET SITE
    driver.get(url)

    # SCROLLING
    for _ in range(int(scrolling_times/speed)):
        driver.execute_script("window.scrollTo(61, document.body.scrollHeight);")
        time.sleep(sleeping_time)

    # SCARIPING ID
    items = driver.find_elements(By.XPATH, scrape_tag_path)

    # CLEANING ID LIST
    for item in items:
        temp = item.get_attribute(scrape_tag_atribute)
        if scrape_tag_name in temp:
            id_list.append(temp)

    # CLOSE WINDOWS
    driver.quit()

    print(f'>> {section_name} section id listing finished \n')

    return id_list


def clean_str_in_list(list, chr='-'):
    """
    this function receives list of strings from the form of 'string prefix'+'char'+'digits' and return list of integers
    (i.e. digits).
    :param list of strings:
    :param char :
    :return: list_int
    """

    return [int(element[element.find(chr)+1:]) for element in list]


def print_from_dict(section_name, item_id, info_dict, num_print, total_print):
    """
    this function receives section name and a dictionary of items' information and print it.
    :param section_name:
    :param {barcode: 'str', name: 'str',  price: float, date: scraping_date}:
    :return:  -
    """

    print(f'____{section_name}: {num_print}/{total_print}____')
    print('Product ID:', item_id)
    print('Barcode:', info_dict['barcode'])
    print('Name:', info_dict['name'])
    print('Price:', info_dict['price'])
    print('Date:', info_dict['date'])


def scrape_rami(list_id_int, url_section, section_name, test_limit_item_per_group = -1, scrolling_times=10, sleeping_time=5, speed=3):
    """
    this function clicks on each id (i.e. an element from the given list of id-s as integers: list_id_int) within the
    given section url (i.e. url_section) and scrapes items' information and print and return it as a dictionary.
    :param list of items id-s in a section (integers):
    :param section url:
    :param secttion_name:
    :return: {item_id: {barcode: 'str', name: 'str',  price: float, date: scraping_date}}
    """

    # IMPORTS
    import datetime
    from seleniumwire import webdriver
    from webdriver_manager.chrome import ChromeDriverManager

    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    import time

    # PARAMETERS
    svc = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=svc)
    driver.maximize_window()

    barcode = """//*[@id="main-product-modal___BV_modal_body_"]/div/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div"""
    barcode_out = """//*[@id="close-popup"]"""
    barcode_price = """//*[@id="main-product-modal___BV_modal_body_"]/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div/span[1]/span"""
    barcode_name = """//*[@id="main-product-modal___BV_modal_body_"]/div/div[2]/div/div/div/div[1]/div[2]/div[1]/h3"""

    # VARIABLE INITIATION
    path_list = []
    items_in_section_dict = {}
    print(f'>> {section_name} scraping started \n')

    # PATH LIST CONSTRACTOR
    for i in list_id_int:
        path_list.append("""item-""" + str(i))

    # DRIVER STARTER
    driver.get(url_section)
    time.sleep(5*3/speed)

    # SCROLLING
    for i in range(int(scrolling_times/speed)):
        driver.execute_script("window.scrollTo(61, document.body.scrollHeight);")
        time.sleep(sleeping_time)

    # NUM ITEM TO RUN: -1 NO LIMIT.
    if test_limit_item_per_group == -1:
        items_to_run = len(list_id_int)
    else:
        items_to_run = test_limit_item_per_group

    for i in range(items_to_run):
        try:
            driver.find_element(By.ID, path_list[i])
            driver.find_element(By.ID, path_list[i]).click()
            time.sleep(3*3/scrap_speed)
            data_barcode = driver.find_element(By.XPATH, barcode)
            data_price = driver.find_element(By.XPATH, barcode_price)
            data_name = driver.find_element(By.XPATH, barcode_name)

            # DICTIONARY ITEM BUILD
            temp = {}

            temp['barcode'] = ''.join((char for char in data_barcode.text if char.isdigit() or "." in char))
            temp['price'] = float(''.join((char for char in data_price.text if char.isalnum() or "." in char)))
            temp['name'] = data_name.text
            print(temp['name'])
            temp['date'] = str(datetime.datetime.now())
            print(temp['date'])

            items_in_section_dict[list_id_int[i]] = temp

            print_from_dict(section_name, list_id_int[i], temp, i + 1, items_to_run)

            driver.find_element(By.XPATH, barcode_out).click()

            time.sleep(3*5/speed)

        except Exception:
             pass

    print(f'>> {section_name} section printing finished \n')
    return items_in_section_dict


def main():

    print('')
    print('SUPER UPPER by GT Team !!!')

    if test_limit_item_per_group > 0:
        print('')
        print("You are running in test mode. Please change test_limit_item_per_group to -1 to run in production mode.")

    items_per_section_dict = {}

    # Initialize database with tables
    database_functions.sql_commands_to_create_database(database_config.tables_queries)

    for section_id in SECTIONS_DICT:
        list_id_str = search_id(SECTIONS_DICT[section_id]['url'], SECTIONS_DICT[section_id]['name'], scrap_speed)
        list_id_int = clean_str_in_list(list_id_str)
        items_per_section_dict[section_id] = scrape_rami(list_id_int, SECTIONS_DICT[section_id]['url'], SECTIONS_DICT[section_id]['name'], test_limit_item_per_group, scrap_speed)

        print(items_per_section_dict)

if __name__ == '__main__':
    main()
