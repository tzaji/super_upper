# GT Team present you SUPER UPPER!!!

# IMPORTS
import json
from datetime import datetime
import database as database_config
import create_and_update_database_and_its_tables as database_functions

# GLOBAL
JSON_FILE_ITEMS_MASTER = 'items_master.json'
JSON_FILE_SECTIONS_MASTER = 'sections_master.json'
JSON_FILE_NAME_PATH = 'config_scrape_paths.json'
IF_SEARCH_NEW_PRODUCT = True
IF_UPDATE_PRICES = False
IF_CREATE_DATABASE = False
IF_ANSWER_QUERY = False



# Test: limit of item per group to scrap. For unlimited: -1.
test_limit_item_per_group_ini = -1

# Scraping speed: 3 is the normal speed. We recommend to scrap between 1 and 5. Please enter your preference.
scrap_speed = 3

def db_query(text, limit_num):
    text = f"SELECT * FROM products JOIN price_records ON products.id = price_records.product_id LIMIT {limit_num};"
    query_answer = database_functions.execute_sql_commands([text], type="SELECT")
    for row in query_answer:
        print(row)


def convert_tuples_to_dictionary(tuples=()):
    dictionary = {}
    for first_item, second_item in tuples:
        dictionary[first_item] = second_item
    return dictionary


def fix_item_price(item_price_scraped):
    return int(item_price_scraped[-4:-2]) + int(item_price_scraped[:-5]) * 100


def export_dict_to_json(dict, json_file_name):
    with open(json_file_name, "w") as file:
        json.dump(dict, file)


def import_dict_from_json(file_name):
    with open(file_name, 'r') as f:
        json_dict = json.load(f)
        print(f'json {file_name} running')
    return json_dict


def search_id(url, section_name, speed=3, scrape_tag_path='//*[@id]', scrape_tag_atribute='id', scrape_tag_name='item',
              scrolling_times=10, sleeping_time=5):
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
    for _ in range(int(scrolling_times / speed)):
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

    return [element[element.find(chr) + 1:] for element in list]


def build_item_url(item_id, config_scrap_paths, master_section_dict, master_items_dict):
    """
    this function receives list of strings from the form of 'string prefix'+'char'+'digits' and return list of integers
    (i.e. digits).
    :param list of strings:
    :param char :
    :return: list_int
    """
    print('item_id', item_id)
    section_id = master_items_dict["items"][item_id]["section"]
    print("section_id", section_id, type(section_id))
    print("url_item_start", config_scrap_paths["path"]["item_scrap"]["system_parameters"]["url_item_start"])
    print("section_direct_item_url", master_section_dict["sections"][section_id]["section_direct_item_url"])
    print("url_item_middle", config_scrap_paths["path"]["item_scrap"]["system_parameters"]["url_item_middle"])
    print("item_id", item_id)

    return config_scrap_paths["path"]["item_scrap"]["system_parameters"]["url_item_start"] + \
           master_section_dict["sections"][section_id]["section_direct_item_url"] + \
           config_scrap_paths["path"]["item_scrap"]["system_parameters"]["url_item_middle"] + item_id


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


def build_item_dict(master_items_dict, list_id_int, section):
    for item in list_id_int:
        if not item in master_items_dict:
            new_item_dict = {"section": section}
            master_items_dict["items"][item] = new_item_dict
            print(f"new item {item} of section {section}")
        else:
            if str(master_items_dict[item]["section"]) != str(section):
                print(
                    f'Different section in master_items to {item}({type(item)}). {master_items_dict[item]["section"]} ({type(master_items_dict[item]["section"])}) instead of {section} ({type(section)})')
    return master_items_dict


def scrape_rami(list_id_int, url_section, section_name, test_limit_item_per_group=-1, scrolling_times=10,
                sleeping_time=5, speed=3):
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
    time.sleep(5 * 3 / speed)

    # SCROLLING
    for i in range(int(scrolling_times / speed)):
        driver.execute_script("window.scrollTo(61, document.body.scrollHeight);")
        time.sleep(sleeping_time)

    # NUM ITEM TO RUN: -1 NO LIMIT.
    if test_limit_item_per_group == -1:
        items_to_run = len(list_id_int)
    else:
        items_to_run = test_limit_item_per_group

    for i in range(items_to_run):
        # try:
            driver.find_element(By.ID, path_list[i])
            driver.find_element(By.ID, path_list[i]).click()
            time.sleep(3 * 3 / scrap_speed)
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

            time.sleep(3 * 5 / speed)

        # except Exception:
        #     pass

    print(f'>> {section_name} section finished \n')
    return items_in_section_dict


def scrape_items_data(list_id_int, master_items_dict, url_section, section_name, section_id, config_scrap_paths,
                      test_limit_item_per_group=-1, scrolling_times=10, sleeping_time=5, speed=3):
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

    # VARIABLE INITIATION
    path_list = []
    items_in_section_dict = {}
    print(f'>> {section_name} scraping started \n')

    # PATH LIST CONSTRACTOR
    for i in list_id_int:
        path_list.append("""item-""" + str(i))

    # DRIVER STARTER
    driver.get(url_section)
    time.sleep(5 * 3 / speed)

    # SCROLLING
    for i in range(int(scrolling_times / speed)):
        driver.execute_script("window.scrollTo(61, document.body.scrollHeight);")
        time.sleep(sleeping_time)

    # NUM ITEM TO RUN: -1 NO LIMIT.
    if test_limit_item_per_group == -1:
        items_to_run = len(list_id_int)
    else:
        items_to_run = test_limit_item_per_group

    items_data_dict = {}

    for i in range(items_to_run):
        try:
            driver.find_element(By.ID, path_list[i])
            print('path_list[i]', path_list[i])
            driver.find_element(By.ID, path_list[i]).click()

            time.sleep(3 * 3 / scrap_speed)

            temp_product = {}
            temp_product['item'] = list_id_int[i]

            temp_product_nutrition = {}
            print('item', path_list[i])
            print(f'scrap item {path_list[i]} start')

            for data in config_scrap_paths["path"]["item_scrap"]["scrap"]["item"]:
                time.sleep(2)
                data_value = driver.find_element(By.XPATH,
                                                 config_scrap_paths["path"]["item_scrap"]["scrap"]["item"][data][
                                                     "path"])
                value = str(data_value.text)
                if data == 'barcode':
                    value = value[6:]
                if data == 'name':
                    value = str("'" + value + "'")
                temp_product[data] = value
                # temp_product_nutrition[data] = value

            temp_product['section_id'] = section_id
            print('temp_product print after uni data', temp_product)

            product_insert_sql = [{'products': temp_product}]
            # insert_sql_product
            database_functions.updating_db_tables(product_insert_sql)
            # return new id product db
            product_id_db_return = f"select id from products where item = {list_id_int[i]} order by id desc limit 1;"

            product_id = database_functions.execute_sql_commands([product_id_db_return], type="SELECT")

            if len(product_id) > 0:
                print('product_id', product_id[0][0])
                temp_product_nutrition['product_id'] = product_id[0][0]

                # print('temp_nutrition print after uni data', nutrition_data)

                try:
                    driver.find_element(By.XPATH, config_scrap_paths["path"]["item_scrap"]["clicks"]["click_open_nutrition_values"]).click()
                    time.sleep(3 * 3 / scrap_speed)
                    nutrition_facts_counter = 1
                    temp_nutrition = {}

                    # check nutrition facts
                    while nutrition_facts_counter < int(config_scrap_paths["path"]["item_scrap"]["system_parameters"][
                                                            "num_nutrition_facts_to_lookfor"]):
                        temp_nutrition[nutrition_facts_counter] = {}
                        for nutrition_data in config_scrap_paths["path"]["item_scrap"]["scrap"]["nutrition"]:

                            # check new nutrition fact
                            try:
                                data_value = driver.find_element(By.XPATH,
                                                                 f"{config_scrap_paths['path']['item_scrap']['scrap']['nutrition'][nutrition_data]['pre_num']}{str(nutrition_facts_counter)}{config_scrap_paths['path']['item_scrap']['scrap']['nutrition'][nutrition_data]['post_num']}")
                                temp_nutrition[nutrition_facts_counter][nutrition_data] = str(data_value.text)
                            except:
                                pass

                            print('temp_nutrition', temp_nutrition)
                            # temp_product_nutrition['nutrition'] = temp_nutrition
                            # print('temp print nutrition collect', temp_product_nutrition)

                            if temp_nutrition[nutrition_facts_counter] == {}:
                                del temp_nutrition[nutrition_facts_counter]
                            nutrition_facts_counter += 1

                    else:
                        pass
                except:
                    pass



            barcode_out = """//*[@id="close-popup"]"""
            driver.find_element(By.XPATH, barcode_out).click()
            time.sleep(3 * 5 / speed)

            print('>>>> temp_product print final item scrap', temp_product)
            print('>>>> temp_product_nutrition print final item scrap to pass Mysql ', temp_product_nutrition)
            # product information completed
            # insert mysql

            # items_data_dict[path_list[i][5:]] = temp
            # print('dict after add item', items_data_dict)

        except:
             print(f'{path_list[i]} not scraped')

    # print('return dict of items', items_data_dict)
    print(f'>> {section_name} section printing finished \n')
    # add_general_items_data = {}
    # add_general_items_data['items'] = items_data_dict
    # return add_general_items_data


def scrape_update_price(dictionary, list_id_int, url_section, config_scrap_paths, section_name, test_limit_item_per_group=-1,
                        scrolling_times=10, sleeping_time=5, speed=3):
    """
    this function clicks on each id (i.e. an element from the given list of id-s as integers: list_id_int) within the
    given section url (i.e. url_section) and scrapes items' information and print and return it as a dictionary.
    :param list of items id-s in a section (integers):
    :param section url:
    :param secttion_name:
    :return: {item_id: {barcode: 'str', name: 'str',  price: float, date: scraping_date}}
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
    path_list = []
    items_in_section_dict = {}
    print(f'>> {section_name} scraping started \n')

    # PATH LIST CONSTRACTOR
    for i in list_id_int:
        path_list.append("""item-""" + str(i))

    # GET SITE
    driver.get(url_section)

    time.sleep(5 * 3 / speed)

    # SCROLLING
    for i in range(int(scrolling_times / speed)):
        driver.execute_script("window.scrollTo(61, document.body.scrollHeight);")
        time.sleep(sleeping_time)

    # NUM ITEM TO RUN: -1 NO LIMIT.
    if test_limit_item_per_group == -1:
        items_to_run = len(path_list)
    else:
        items_to_run = test_limit_item_per_group

    price_correction_func = config_scrap_paths['path']['item_scrap']['scrap']['section_page']['price'][
        'correction_func']

    print(f'dictionary: {dictionary}')

    for item in range(items_to_run):
        try:
            driver.find_element(By.ID, path_list[item])


            print('preview to check check price')
            print('item path_list', path_list[item])
            print('item list_id_int', list_id_int[item])

            if int(list_id_int[item]) in dictionary:

                id_prod_db = dictionary[int(list_id_int[item])]
                print(f'id_prod_db: {id_prod_db}')


                item_price_path = str(
                    config_scrap_paths['path']['item_scrap']['scrap']['section_page']['price']['pre_num']) + str(
                    path_list[item]) + str(
                    config_scrap_paths['path']['item_scrap']['scrap']['section_page']['price']["post_num"])
                print('item_price_path', item_price_path)
                # check the price
                data_price = driver.find_element(By.XPATH, item_price_path)
                price_string = data_price.text
                price = int(price_string[-4:-2]) + int(price_string[:-5]) * 100
                print('price:', price, type(price))

                # insert price record
                # id = 1

                now = datetime.now()
                formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
                price_record = [{'price_records': {'product_id': str(id_prod_db), 'price': str(price), 'record_time': str("'" + formatted_date + "'")}}]
                print('>>>> price_record', price_record)
                database_functions.updating_db_tables(price_record)

            # Assuming you have a cursor named cursor you want to execute this query on:
            # cursor.execute('insert into table(id, date_created) values(%s, %s)', (id, formatted_date))

        except Exception:
            print(f"{item} is not checking price")

    # print(f'>> {section_name} section printing finished \n')
    # return items_in_section_dict


def main():
    print('')
    print('SUPER UPPER by GT Team !!!')

    # Initialize database with tables
    if IF_CREATE_DATABASE:
        database_functions.sql_commands_to_create_database(database_config.tables_queries)


    if IF_ANSWER_QUERY:
        db_query("0", "15")


    # SELECT list of tuples(item, id) of products
    product_tuples = database_functions.execute_sql_commands([database_config.select_products_items_query], type="SELECT")
    if product_tuples:
        product_dictionary = convert_tuples_to_dictionary(product_tuples)


    if test_limit_item_per_group_ini > 0:
        print('')
        print("You are running in test mode. Please change test_limit_item_per_group to -1 to run in production mode.")

    master_section_dict = import_dict_from_json(JSON_FILE_SECTIONS_MASTER)
    print('master_sections_dict imported from json', type(master_section_dict), master_section_dict)

    master_items_dict = import_dict_from_json(JSON_FILE_ITEMS_MASTER)
    print('master_items_dict imported from json', type(master_items_dict), master_items_dict)

    config_scrap_paths = import_dict_from_json(JSON_FILE_NAME_PATH)
    print('config_scrap_paths imported from json', type(config_scrap_paths), config_scrap_paths)

    if IF_SEARCH_NEW_PRODUCT or IF_UPDATE_PRICES:

        items_data = {}

        for section_id in master_section_dict["sections"]:
            print(master_section_dict["sections"])
            print('value ID', type(section_id), section_id)  # key
            print('master_section_dict["sections"] - URL', type(master_section_dict["sections"]),
                  master_section_dict["sections"][section_id])  # ["name"]

            list_id_str = search_id(master_section_dict["sections"][section_id]['url'],
                                    master_section_dict["sections"][section_id]['name'])

            print(len(list_id_str), list_id_str)
            list_id_int = clean_str_in_list(list_id_str)
            print('master_items_dict before build', len(master_items_dict), master_items_dict)
            print('list_id_int before enter to scrap section page', list_id_int)

            if IF_SEARCH_NEW_PRODUCT:
                scrape_items_data(list_id_int, master_items_dict, master_section_dict["sections"][section_id]['url'],
                                  master_section_dict["sections"][section_id]['name'], section_id, config_scrap_paths,
                                  test_limit_item_per_group=test_limit_item_per_group_ini,
                                  scrolling_times=10, sleeping_time=5, speed=3)

                items_data['items'] = scrape_items_data
                print(items_data)

            if IF_UPDATE_PRICES:
                items_data = scrape_update_price(product_dictionary, list_id_int, master_section_dict["sections"][section_id]['url'],
                                                 config_scrap_paths, master_section_dict["sections"][section_id]['name'],
                                                 test_limit_item_per_group=test_limit_item_per_group_ini,
                                                 scrolling_times=10, sleeping_time=5, speed=3)

            master_items_dict = build_item_dict(master_items_dict, list_id_int, section_id)
            print('master_items_dict after build', len(master_items_dict), master_items_dict)

        export_dict_to_json(master_items_dict, JSON_FILE_ITEMS_MASTER)
        export_dict_to_json(items_data, 'items_first_insert.json')

        print(config_scrap_paths)
        print(master_items_dict)
        print(master_section_dict)

    # for item in master_items_dict['items']:
    #     print(build_item_url(item, config_scrap_paths, master_section_dict, master_items_dict))


if __name__ == '__main__':
    main()
