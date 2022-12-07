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
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

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
        print('Successfully loaded search.')
    except:
        print('Uh Oh')

    pages = driver.find_elements(By.XPATH, '//*[@id="firmpage"]/option')
    for page in pages:
        ALL_firms = []
        detail_row = 0
        next_page = Select(driver.find_element(By.XPATH, '//*[@id="firmpage"]'))
        next_page.select_by_value(page.text)
        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, f'// *[ @ id = "fpDetailIcon{detail_row}"]'))
            )
            print("Entered page")
        except:
            print('Uh Oh')
        time.sleep(0.5)

        firms = driver.find_elements(By.CLASS_NAME, "tblRow")

        if record_count < 990:
            ID_number = 2
            for firm in firms:
                firm_details = []
                try:
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[1]/span'))
                    )
                    title = driver.find_element(By.XPATH,
                                                f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[1]/span')
                except:
                    title = ''
                    print("Couldn't load element")

                firm_details.append(title.text)
                try:
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[4]/div[2]'))
                    )
                    contact = driver.find_element(By.XPATH, f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[4]/div[2]')
                except:
                    contact = ''
                    print("Couldn't load element")
                firm_details.append(contact.text)
                try:
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, f'// *[ @ id = "fpDetailIcon{detail_row}"]'))
                    )
                    expand = driver.find_element(By.XPATH, f'// *[ @ id = "fpDetailIcon{detail_row}"]')
                    expand.click()
                except:
                    print('Uh Oh, Waiting...')
                    time.sleep(10)
                    expand = driver.find_element(By.XPATH, f'// *[ @ id = "fpDetailIcon{detail_row}"]')
                    expand.click()
                # print(detail_row)
                try:
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.ID, f"fpDetail{detail_row}"))
                    )
                    details = driver.find_element(By.ID, f"fpDetail{detail_row}")
                except:
                    print("Couldn't load element. Trying again")
                    time.sleep(10)
                    details = driver.find_element(By.ID, f"fpDetail{detail_row}")

                try:
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'ctblCol2'))
                    )
                    col = details.find_elements(By.CLASS_NAME, 'ctblCol2')
                except:
                    # print('Uh Oh, Waiting...')
                    # time.sleep(5)
                    # col = details.find_elements(By.CLASS_NAME, 'ctblCol2')
                    print("Could not load element")
                    col = []
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
            # print(ALL_firms)
        else:
            file.close()
            file_number += 1
            createFile(file_number)
            ID_number = 2
            for firm in firms:
                firm_details = []
                try:
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[1]/span'))
                    )
                    title = driver.find_element(By.XPATH,
                                                f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[1]/span')
                except:
                    title = ''
                    print("Couldn't load element")
                firm_details.append(title.text)
                try:
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[4]/div[2]'))
                    )
                    contact = driver.find_element(By.XPATH,
                                                  f'//*[@id="firmResultPanel"]/div[1]/div[{ID_number}]/div[4]/div[2]')
                except:
                    contact = ''
                    print("Couldn't load element")
                firm_details.append(contact.text)
                try:
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, f'// *[ @ id = "fpDetailIcon{detail_row}"]'))
                    )
                    expand = driver.find_element(By.XPATH, f'// *[ @ id = "fpDetailIcon{detail_row}"]')
                    expand.click()
                except:
                    print('Uh Oh, Waiting...')
                    time.sleep(10)
                    expand = driver.find_element(By.XPATH, f'// *[ @ id = "fpDetailIcon{detail_row}"]')
                    expand.click()
                # print(detail_row)
                try:
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.ID, f"fpDetail{detail_row}"))
                    )
                    details = driver.find_element(By.ID, f"fpDetail{detail_row}")
                except:
                    print("Couldn't load element. Trying again")
                    time.sleep(10)
                    details = driver.find_element(By.ID, f"fpDetail{detail_row}")
                try:
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'ctblCol2'))
                    )
                    col = details.find_elements(By.CLASS_NAME, 'ctblCol2')
                except:
                    # print('Uh Oh, Waiting...')
                    # time.sleep(5)
                    # col = details.find_elements(By.CLASS_NAME, 'ctblCol2')
                    print("Could not load element")
                    col = []
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
            # print(ALL_firms)
driver.quit()
file.close()