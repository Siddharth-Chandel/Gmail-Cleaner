import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from undetected_chromedriver.webelement import WebElement
import pyautogui as gui
import time
import os

path = input('Path of Chrome Driver : ')
os.chdir(path+'\\')


def TotalMails(driver: uc.Chrome) -> WebElement:
    '''This function helps to get the total no. of mails.'''
    mailMarking = [i for i in driver.find_elements(
        by=By.CSS_SELECTOR, value='span[class="ts"]')]
    if len(mailMarking) == 6:
        return mailMarking[5]
    elif len(mailMarking) == 3:
        return mailMarking[2]


def main() -> None:
    '''Main Program'''
    print('Starting...')
    try:
        # Initializing chrome driver
        driver = uc.Chrome(use_subprocess=True, version_main='104')
        driver.implicitly_wait(30)
        driver.get('https://mail.google.com/mail/u/0/#inbox')
        driver.maximize_window()
        time.sleep(2)

        # Asking for entering credentials
        gui.alert(
            text='Enter your credentials before you go ahead', title='Note :-')

        # Action to be taken on Emails
        action = gui.prompt(text="Delete / Read",
                            title='Action', default='Delete')
        if action != None:
            # Delete Action
            if action.lower() == 'delete':
                # No. of emails which will be left
                amount = gui.prompt(
                    text='How many E-mails you want to be left ?', title='Amount of E-mails', default='0')

                if amount != None:
                    if amount.isnumeric():
                        # Warraning message
                        gui.alert(text='Deletion is going to start...',
                                  title='Deleting')

                        # Total no. of emails
                        totalMails = TotalMails(driver=driver)

                        # Deletion
                        while int(totalMails.text) > int(amount):
                            try:
                                # Selection
                                driver.find_element(
                                    by=By.CSS_SELECTOR, value='div[data-tooltip="Select"]').click()

                                # Delete
                                driver.find_element(
                                    by=By.CSS_SELECTOR, value='div[data-tooltip="Delete"]').click()
                                time.sleep(5)

                                # Checking the no. of emails left
                                totalMails = TotalMails(driver=driver)
                                time.sleep(5)
                            except:
                                break
                        print('Done')
            # Read Action
            elif action.lower() == 'read':
                while driver.find_element(
                        by=By.CSS_SELECTOR, value='span[class="ts"]').text != 0:
                    try:
                        # Selection of Emails
                        driver.find_elements(
                            by=By.CSS_SELECTOR, value='span[role="checkbox"')[0].click()

                        # Mark Read
                        driver.find_element(by=By.CSS_SELECTOR,
                                            value='div[data-tooltip="Mark as read"]').click()
                        time.sleep(2)

                        # Deselect all Emails
                        driver.find_elements(
                            by=By.CSS_SELECTOR, value='span[role="checkbox"')[0].click()

                        # Refresh
                        driver.find_element(
                            by=By.CSS_SELECTOR, value='div[data-tooltip="Refresh"]').click()

                        time.sleep(5)
                    except:
                        break
                print('Done')
        print('Closed')
        driver.close()
    except Exception as e:
        print('error : ', e)


if __name__ == '__main__':
    main()
