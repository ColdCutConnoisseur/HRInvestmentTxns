"""Enter taxable transactions on H&R Block"""

import sys
import time
import csv

#from selenium import webdriver
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys


def DEPRclick_next_button(driver):
    next_button_xpath = "//a[@class='nextButton']"

    wait = WebDriverWait(driver, 10)
    next_button = wait.until(ec.presence_of_element_located((By.XPATH, next_button_xpath)))
    driver.execute_script("arguments[0].click();", next_button)


def click_next_button(driver):
    next_button_xpath = "//a[@title='Add Crypyocurrency Transaction']"

    wait = WebDriverWait(driver, 10)
    next_button = wait.until(ec.presence_of_element_located((By.XPATH, next_button_xpath)))
    driver.execute_script("arguments[0].click();", next_button)


def click_add_transaction_button(driver):
    add_txn_button_xpath = "//a[contains(text(), 'Add transaction')]"

    wait = WebDriverWait(driver, 10)
    txn_button = wait.until(ec.presence_of_element_located((By.XPATH, add_txn_button_xpath)))
    driver.execute_script("arguments[0].click();", txn_button)


def add_service_text(driver, service_text):
    """Add name of service for txn info e.g. Coinbase"""
    service_box_xpath = "//input[@id='XFormatTextBoxtxtService']"
    
    wait = WebDriverWait(driver, 10)
    service_box = wait.until(ec.presence_of_element_located((By.XPATH, service_box_xpath)))
    service_box.send_keys(service_text)


def add_description_of_property(driver, property_text):
    description_box_xpath = "//input[@id='XFormatTextBoxtxtDescOfProperty']"

    description_box = driver.find_element(By.XPATH, description_box_xpath)
    description_box.send_keys(property_text)


def add_date_acquired(driver, date_acquired_text):
    date_acquired_box_xpath = "//input[@id='XFormatTextBoxtxtDateAcquired']"

    date_acquired_box = driver.find_element(By.XPATH, date_acquired_box_xpath)
    date_acquired_box.send_keys(date_acquired_text)


def add_date_of_sale(driver, date_of_sale_text):
    date_of_sale_box_xpath = "//input[@id='XFormatTextBoxtxtDateOfSale']"

    date_of_sale_box = driver.find_element(By.XPATH, date_of_sale_box_xpath)
    date_of_sale_box.send_keys(date_of_sale_text)


def add_proceeds(driver, proceeds_text):
    proceeds_box_xpath = "//input[@id='XFormatTextBoxtxtSaleProceeds']"

    proceeds_box = driver.find_element(By.XPATH, proceeds_box_xpath)
    proceeds_box.send_keys(proceeds_text)


def add_cost_basis(driver, cost_basis_text):
    cost_basis_box_xpath = "//input[@id='XFormatTextBoxtxtCostBasis']"

    cost_basis_box = driver.find_element(By.XPATH, cost_basis_box_xpath)
    cost_basis_box.send_keys(cost_basis_text)
    cost_basis_box.send_keys(Keys.TAB)


def await_user_ok():
    user_in = input("Does the transaction look ok?\n")
    if user_in:
        return


def add_crypto_txn(driver, transaction_record):
    service_text = transaction_record[0]
    description_of_property = transaction_record[1]
    date_acquired_text = transaction_record[2]
    date_of_sale_text = transaction_record[3]
    proceeds_text = transaction_record[4]
    cost_basis_text = transaction_record[5]

    # click_add_transaction_button(driver)

    # time.sleep(2.5)

    add_service_text(driver, service_text)
    add_description_of_property(driver, description_of_property)
    add_date_acquired(driver, date_acquired_text)
    add_date_of_sale(driver, date_of_sale_text)
    add_proceeds(driver, proceeds_text)
    add_cost_basis(driver, cost_basis_text)

    # await_user_ok()

    click_next_button(driver)

    time.sleep(2.5)


if __name__ == "__main__":
    TXN_FILE_PATH = "./formatted_transactions_2022_thruQ4.csv"
    CONTINUE_INDEX = 0

    #Load tax transactions
    all_tax_transactions = []

    with open(TXN_FILE_PATH, 'r') as csv_in:
        csv_reader = csv.reader(csv_in)
        for row in csv_reader:
            all_tax_transactions.append(row)

    #Set Driver
    driver = uc.Chrome()

    #Log in to H&R Dingus
    # hr_url = "https://idp.hrblock.com/idp/profile/SAML2/Redirect/SSO?execution=e1s1"
    hr_url = "https://www.hrblock.com/home/"
    driver.get(hr_url)
    user_logged_in = input("Log in to your H&R Block account, navigate to crypto txns page\n")

    if user_logged_in:

        #Upload transactions
        for ct, current_transaction_record in enumerate(all_tax_transactions):

            print(f"Current Txn Index: {ct}")

            if ct >= CONTINUE_INDEX:

                print("Continuation index matched..")

                try:
                    add_crypto_txn(driver, current_transaction_record)

                except NoSuchElementException:
                    print("'NoSuchElement' caught.  Closing...")
                    sys.exit(0)

                except TimeoutException:
                    print("'TimeoutException' caught.  Closing...")
                    sys.exit(0)

        time.sleep(500)
        driver.quit()

    else:
        driver.quit()
