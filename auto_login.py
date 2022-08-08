###############################################################################
# AUTOMATED TESTING
# PURPOSE: To test successful logins and failed logins to the demo blaze website.
# SITE: demoblaze.com/index.html
# AUTHOR: Christopher Brough
# DATE: 8/5/2022
# NOTE: In order to run this, you MUST have the latest version of Chrome
###############################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os.path import exists
from os import remove

def log_result(result, username, password):
    """Logs the result of a test."""
    with open('log.txt', 'a') as log:
        user_info = (f'Username: {username}, Password: {password}\n')
        print(user_info.strip())
        log.write(user_info)

        if result:
            outcome = '\tLogin successful\n'
        else:
            outcome = '\tLogin failed\n'

        print(outcome.rstrip())
        log.write(outcome)

def login(username, password, browser):
    """Logs into an account given a username and password."""
    # Find and click the login navigation button
    login_button = browser.find_element(By.ID,'login2')
    login_button.click()

    # Find and wait for login button
    login_button = browser.find_element('xpath',"//button[@onclick='logIn()']")
    WebDriverWait(browser,0.75).until(EC.element_to_be_clickable(login_button))

    # Find the username and password.
    username_field = browser.find_element(By.ID,'loginusername')
    password_field = browser.find_element(By.ID,'loginpassword')

    # Enter the username and password.
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Click the login button
    login_button.click()

    # Check for alerts. If there are any, print "login failed", otherwise print "login successful".
    try:
        WebDriverWait(browser,0.57).until(EC.alert_is_present())
        alert = browser.switch_to.alert
        alert.accept()
        browser.refresh()
        return False
    except:
        logout_button = browser.find_element(By.ID,'logout2') 
        logout_button.click()
        return True

def main():
    """Prepare the test environment and run tests."""
    # Open the browser and navigate to the website.
    browser = webdriver.Chrome('chromedriver')
    browser.get('https://demoblaze.com/index.html')

    # For counting totals
    fails = 0
    successes = 0
    
    # If log exists, delete it
    if exists('log.txt'):
        remove('log.txt')

    # Prepare usernames and passwords
    users_and_pass = []
    
    if not exists('users.txt'):
        print('users.txt does not exist. Exiting...')
        return

    with open('users.txt', 'r') as f:
        users_pass = f.readlines()
        for line in users_pass:
            username, password = line.split(',')
            users_and_pass.append((username, password.rstrip('\n')))

    # Run the tests.
    for username,password in users_and_pass:
        result = login(username, password,browser)
        log_result(result, username, password)
        if result:
            successes += 1
        else:
            fails += 1

    # Quitting
    print(f'Finished.\n\tSuccessful logins: {successes}\n\tFailed logins: {fails}\nQuitting...')
    browser.quit()
    return

main()