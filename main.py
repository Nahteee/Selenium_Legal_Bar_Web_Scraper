from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import csv
import time


def createFile(number):
    global record_count
    global file
    global writer
    record_count = 0
    file = open(f'Law Firms {file_number}.csv', 'w', encoding='utf8', newline='')
    writer = csv.writer(file)

    # writer header rows
    writer.writerow(["Company", "Phone", "Street", "Email", "Website", "Last Name", "Description", "Lead Source",
                     "Industry"])


options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("--window-size=1920,1200")
options.add_experimental_option("detach", True)

DRIVER_PATH = '/path/to/chromedriver'

# To view with window closed (top) or open (bottom)
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
# driver = webdriver.Chrome(executable_path=DRIVER_PATH)

driver.get('https://legaldirectory.malaysianbar.org.my/')

record_count = 0
file_number = 1
file = open(f'Law Firms {file_number}.csv', 'w', encoding='utf8', newline='')
writer = csv.writer(file)

# writer header rows
writer.writerow(["Company", "Phone", "Street", "Email", "Website", "Last Name", "Description", "Lead Source", "Industry"])

untick = driver.find_element(By.XPATH, '//*[@id="searchtypelawyer"]')
untick.click()


search_entries = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                  "U", "V", "W", "X", "Y", "Z"]

for entry in search_entries:
    search = Select(driver.find_element(By.XPATH, '//*[@id="alphabet"]'))
    search.select_by_value(entry)
    submit = driver.find_element(By.XPATH, '//*[@id="submit"]')
    submit.click()
    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "blueBarHdPara"))
        )
        print(f'Successfully loaded search "{entry}".')
    except:
        print('Uh Oh, Trying again...')
        time.sleep(10)
        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "blueBarHdPara"))
            )
            print(f'Successfully loaded search "{entry}".')
        except:
            print('Search failed...Retry program')

    pages = driver.find_elements(By.XPATH, '//*[@id="firmpage"]/option')
    for page in pages:
        ALL_firms = []
        detail_row = 0
        next_page = Select(driver.find_element(By.XPATH, '//*[@id="firmpage"]'))
        next_page.select_by_value(page.text)

        # LOADING PAGE---------------------------------------------------------------------------------------------
        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, f'// *[ @ id = "fpDetailIcon{detail_row}"]'))
            )
            print(f"Entered page {page.text}")
        except:
            print('Uh Oh, Waiting(1)...')
            time.sleep(5)
            try:
                element = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, f'// *[ @ id = "fpDetailIcon{detail_row}"]'))
                )
                print(f"Entered page {page.text}")
            except:
                print('Trouble loading page. Last try...')
                time.sleep(10)
                try:
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, f'// *[ @ id = "fpDetailIcon{detail_row}"]'))
                    )
                    print(f"Entered page {page.text}")
                except:
                    print('Could not load. Skipping page...')
                    continue
        time.sleep(0.5)

        # FINDING FIRMS--------------------------------------------------------------------------------------------
        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tblRow"))
            )
            firms = driver.find_elements(By.CLASS_NAME, "tblRow")
        except:
            print('Uh Oh, Waiting (2)...')
            time.sleep(5)
            try:
                element = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "tblRow"))
                )
                firms = driver.find_elements(By.CLASS_NAME, "tblRow")
            except:
                print('Trouble loading firms. Last try...')
                time.sleep(10)
                try:
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "tblRow"))
                    )
                    firms = driver.find_elements(By.CLASS_NAME, "tblRow")
                except:
                    print('Could not load firms. Skipping page....')
                    continue
            try:
                print('Confirming firms')
                time.sleep(1)
                element = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "tblRow"))
                )
                firms = driver.find_elements(By.CLASS_NAME, "tblRow")
            except:
                print('Could not load firms. Skipping page....')
                continue

        if record_count < 990:
            ID_number = 2
            fail_count = 0
            for firm in firms:
                firm_details = []

                # TITLE--------------------------------------------------------------------------------------------
                try:
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[1]/span'))
                    )
                    title = driver.find_element(By.XPATH,
                                                f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[1]/span')
                except:
                    if fail_count > 1:
                        print("No records found.")
                        continue
                    print('Uh Oh, Waiting (3)...')
                    time.sleep(2)
                    try:
                        element = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[1]/span'))
                        )
                        title = driver.find_element(By.XPATH,
                                                    f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[1]/span')
                    except:
                        print('Trouble Loading Title. Last try...')
                        time.sleep(3)
                        try:
                            element = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.XPATH,
                                                                f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[1]/span'))
                            )
                            title = driver.find_element(By.XPATH,
                                                        f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[1]/span')
                        except:
                            fail_count += 1
                            print("No records found. Skipping record")
                            detail_row += 1
                            ID_number += 2
                            continue
                try:
                    firm_details.append(title.text)
                except:
                    print('Dude failed to append title. Trying again')
                    title = driver.find_element(By.XPATH,
                                                f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[1]/span')
                    time.sleep(5)
                try:
                    firm_details.append(title.text)
                except:
                    print('Nah bad website. Skipping record')
                    continue


                # CONTACT--------------------------------------------------------------------------------------------
                try:
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[4]/div[2]'))
                    )
                    contact = driver.find_element(By.XPATH,
                                                  f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[4]/div[2]')
                except:
                    print('Uh Oh, Waiting (4)...')
                    time.sleep(5)
                    try:
                        element = WebDriverWait(driver, 15).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[4]/div[2]'))
                        )
                        contact = driver.find_element(By.XPATH,
                                                      f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[4]/div[2]')
                    except:
                        print('Trouble Loading contacts. Last try...')
                        time.sleep(10)
                        try:
                            element = WebDriverWait(driver, 15).until(
                                EC.presence_of_element_located((By.XPATH,
                                                                f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[4]/div[2]'))
                            )
                            contact = driver.find_element(By.XPATH,
                                                          f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[4]/div[2]')
                        except:
                            print("Can't load elements. Skipping record")
                            detail_row += 1
                            ID_number += 2
                            continue


                try:
                    firm_details.append(contact.text)
                except:
                    print('Dude failed to append contact. Trying again')
                    contact = driver.find_element(By.XPATH,
                                                  f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[4]/div[2]')
                    time.sleep(5)
                try:
                    firm_details.append(contact.text)
                except:
                    print('Nah bad website. Skipping record')
                    continue

                # DROPDOWN--------------------------------------------------------------------------------------------
                try:
                    element = WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, f'// *[ @ id = "fpDetailIcon{detail_row}"]'))
                    ).click()
                except:
                    print('Uh Oh, Waiting (5)...')
                    time.sleep(5)
                    try:
                        element = WebDriverWait(driver, 15).until(
                            EC.element_to_be_clickable((By.XPATH, f'// *[ @ id = "fpDetailIcon{detail_row}"]'))
                        ).click()
                    except:
                        print('Page is having trouble loading. Last try.')
                        time.sleep(5)
                        try:
                            element = WebDriverWait(driver, 15).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH, f'// *[ @ id = "fpDetailIcon{detail_row}"]'))
                            ).click()
                        except Exception as e:
                            print("Can't expand dropdown. Skipping record")
                            print('Error! Code: {c}, Message, {m}'.format(c=type(e).__name__, m=str(e)))
                            print(detail_row, "Detail row")
                            print(ID_number, "ID")
                            detail_row += 1
                            ID_number += 2

                            continue

                # DETAILS--------------------------------------------------------------------------------------------
                try:
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.ID, f"fpDetail{detail_row}"))
                    )
                    details = driver.find_element(By.ID, f"fpDetail{detail_row}")
                except:
                    print('Uh Oh, Waiting (6)...')
                    time.sleep(5)
                    try:
                        element = WebDriverWait(driver, 15).until(
                            EC.presence_of_element_located((By.ID, f"fpDetail{detail_row}"))
                        )
                        details = driver.find_element(By.ID, f"fpDetail{detail_row}")
                    except:
                        print('Trouble loading details. Last try.')
                        time.sleep(10)
                        try:
                            element = WebDriverWait(driver, 15).until(
                                EC.presence_of_element_located((By.ID, f"fpDetail{detail_row}"))
                            )
                            details = driver.find_element(By.ID, f"fpDetail{detail_row}")
                        except:
                            print("Can't load elements. Skipping record")
                            detail_row += 1
                            ID_number += 2
                            continue

                # COLUMNS--------------------------------------------------------------------------------------------
                try:
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'ctblCol2'))
                    )
                    col = details.find_elements(By.CLASS_NAME, 'ctblCol2')
                except:
                    print('Uh Oh, Waiting (7)...')
                    time.sleep(5)
                    try:
                        element = WebDriverWait(driver, 15).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'ctblCol2'))
                        )
                        col = details.find_elements(By.CLASS_NAME, 'ctblCol2')
                    except:
                        print('Trouble Loading Columns. Last try.')
                        time.sleep(10)
                        try:
                            element = WebDriverWait(driver, 15).until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'ctblCol2'))
                            )
                            col = details.find_elements(By.CLASS_NAME, 'ctblCol2')
                        except:
                            print("Can't load elements. Skipping record")
                            detail_row += 1
                            ID_number += 2
                            continue

                # Appending--------------------------------------------------------------------------------------------
                for c in col:
                    firm_details.append(c.text)
                detail_row += 1
                ID_number += 2
                firm_details.append("Web")
                firm_details.append("Legal Firms")
                ALL_firms.append(firm_details)
                record_count += 1
                print(record_count)
            writer.writerows(ALL_firms)
        else:
            file.close()
            file_number += 1
            createFile(file_number)
            ID_number = 2
            fail_count = 0
            for firm in firms:
                firm_details = []

                # TITLE--------------------------------------------------------------------------------------------
                try:
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[1]/span'))
                    )
                    title = driver.find_element(By.XPATH,
                                                f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[1]/span')
                except:
                    if fail_count > 2:
                        print("No records found. Skipping record")
                        continue
                    print('Uh Oh, Waiting (3)...')
                    time.sleep(2)
                    try:
                        element = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[1]/span'))
                        )
                        title = driver.find_element(By.XPATH,
                                                    f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[1]/span')
                    except:
                        print('Trouble Loading Title. Last try...')
                        time.sleep(3)
                        try:
                            element = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.XPATH,
                                                                f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[1]/span'))
                            )
                            title = driver.find_element(By.XPATH,
                                                        f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[1]/span')
                        except:
                            fail_count += 1
                            print("No records found. Skipping record")
                            detail_row += 1
                            ID_number += 2
                            continue

                try:
                    firm_details.append(title.text)
                except:
                    print('Dude failed to append title. Trying again')
                    title = driver.find_element(By.XPATH,
                                                f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[1]/span')
                    time.sleep(5)
                try:
                    firm_details.append(title.text)
                except:
                    print('Nah shitty website. Skipping record')
                    continue

                # CONTACT--------------------------------------------------------------------------------------------
                try:
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[4]/div[2]'))
                    )
                    contact = driver.find_element(By.XPATH,
                                                  f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[4]/div[2]')
                except:
                    print('Uh Oh, Waiting...')
                    time.sleep(5)
                    try:
                        element = WebDriverWait(driver, 15).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[4]/div[2]'))
                        )
                        contact = driver.find_element(By.XPATH,
                                                      f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[4]/div[2]')
                    except:
                        print('Trouble Loading contacts. Last try...')
                        time.sleep(10)
                        try:
                            element = WebDriverWait(driver, 15).until(
                                EC.presence_of_element_located((By.XPATH,
                                                                f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[4]/div[2]'))
                            )
                            contact = driver.find_element(By.XPATH,
                                                          f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[4]/div[2]')
                        except:
                            print("Can't load elements. Skipping record")
                            detail_row += 1
                            ID_number += 2
                            continue
                try:
                    firm_details.append(contact.text)
                except:
                    print('Dude failed to append contact. Trying again')
                    contact = driver.find_element(By.XPATH,
                                                  f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[4]/div[2]')
                    time.sleep(5)
                try:
                    firm_details.append(contact.text)
                except:
                    print('Nah shitty website. Skipping record')
                    continue

                # DROPDOWN--------------------------------------------------------------------------------------------
                try:
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, f'// *[ @ id = "fpDetailIcon{detail_row}"]'))
                    )
                    expand = driver.find_element(By.XPATH, f'// *[ @ id = "fpDetailIcon{detail_row}"]')
                    expand.click()
                except:
                    print('Uh Oh, Waiting...')
                    time.sleep(5)
                    try:
                        expand = driver.find_element(By.XPATH, f'// *[ @ id = "fpDetailIcon{detail_row}"]')
                        expand.click()
                    except:
                        print('Page is having trouble loading. Last try.')
                        time.sleep(5)
                        try:
                            expand = driver.find_element(By.XPATH, f'// *[ @ id = "fpDetailIcon{detail_row}"]')
                            expand.click()
                        except:
                            print("Can't expand dropdown. Skipping record")
                            detail_row += 1
                            ID_number += 2
                            continue

                # DETAILS--------------------------------------------------------------------------------------------
                try:
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.ID, f"fpDetail{detail_row}"))
                    )
                    details = driver.find_element(By.ID, f"fpDetail{detail_row}")
                except:
                    print('Uh Oh, Waiting...')
                    time.sleep(5)
                    try:
                        element = WebDriverWait(driver, 15).until(
                            EC.presence_of_element_located((By.ID, f"fpDetail{detail_row}"))
                        )
                        details = driver.find_element(By.ID, f"fpDetail{detail_row}")
                    except:
                        print('Trouble loading details. Last try.')
                        time.sleep(10)
                        try:
                            element = WebDriverWait(driver, 15).until(
                                EC.presence_of_element_located((By.ID, f"fpDetail{detail_row}"))
                            )
                            details = driver.find_element(By.ID, f"fpDetail{detail_row}")
                        except:
                            print("Can't load elements. Skipping record")
                            detail_row += 1
                            ID_number += 2
                            continue

                # COLUMNS--------------------------------------------------------------------------------------------
                try:
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'ctblCol2'))
                    )
                    col = details.find_elements(By.CLASS_NAME, 'ctblCol2')
                except:
                    print('Uh Oh, Waiting...')
                    time.sleep(5)
                    try:
                        element = WebDriverWait(driver, 15).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'ctblCol2'))
                        )
                        col = details.find_elements(By.CLASS_NAME, 'ctblCol2')
                    except:
                        print('Trouble Loading Columns. Last try.')
                        time.sleep(10)
                        try:
                            element = WebDriverWait(driver, 15).until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'ctblCol2'))
                            )
                            col = details.find_elements(By.CLASS_NAME, 'ctblCol2')
                        except:
                            print("Can't load elements. Skipping record")
                            detail_row += 1
                            ID_number += 2
                            continue

                # Appending--------------------------------------------------------------------------------------------
                for c in col:
                    firm_details.append(c.text)
                detail_row += 1
                ID_number += 2
                firm_details.append("Web")
                firm_details.append("Legal Firms")
                ALL_firms.append(firm_details)
                record_count += 1
                print(record_count)
            writer.writerows(ALL_firms)
driver.quit()
file.close()
