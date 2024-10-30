import os
import time
from playwright.sync_api import sync_playwright, TimeoutError

def fill_form(page):
    """Fill out the application form fields"""
    try:
        page.fill('input[name="name"]', 'John Doe')
        page.fill('//input[@name="email" and @data-qa="email-input"]', 'xyz@abc.com')
        page.fill('//input[@name="phone" and @data-qa="phone-input"]', '888-123-4567')
        page.fill('//input[@name="urls[LinkedIn]" and @type="text"]', 'https://www.linkedin.com/in/johndoe')
        page.fill('//input[@name="urls[Twitter]" and @type="text"]', 'https://twitter.com/johndoe')
    except Exception as e:
        print(f'Error filling form: {str(e)}')

def fill_custom_questions(page):
    """Fill out custom questions in the application."""
    try:
        list_items = page.query_selector_all('//ul/li[contains(@class, "application-question") and contains(@class, "custom-question")]')
        for item in list_items:
            input_type = 'radio' if item.query_selector('//input[@type="radio"]') else 'textarea'

            if input_type == 'radio':
                radio_buttons = item.query_selector_all('//input[@type="radio"]')
                if 'Are you a US Citizen or permanent resident?' in item.inner_text():
                    for radio_button in radio_buttons:
                        if 'Yes' in radio_button.get_attribute('value'):
                            radio_button.check()
                elif 'If you\'re not a US citizen, will you now or in the future require' in item.inner_text():
                    for radio_button in radio_buttons:
                        if 'will not need sponsorship' in radio_button.get_attribute('value'):
                            radio_button.check()
                else:
                    radio_buttons[0].check()

            elif input_type == 'textarea':
                textarea = item.query_selector('//textarea[@class="card-field-input"]')
                if 'Why did you choose that language?' in item.inner_text():
                    textarea.fill('I chose this language because it is the best!')
                elif 'What was your favorite data project and what impact did it have?' in item.inner_text():
                    textarea.fill('My favorite data project was the one where I saved the world!')
                elif 'Give an example of how you’ve shared outcomes from a data project to stakeholders?' in item.inner_text():
                    textarea.fill('I shared the outcomes by presenting a PowerPoint presentation!')
                elif 'List the reporting tools that you have experience with:' in item.inner_text():
                    textarea.fill('I have experience with Tableau, PowerBI, and Excel!')
    except Exception as e:
        print(f'Error filling custom questions: {str(e)}')

def fill_equal_employment_questions(page):
    """Fill out US Equal Employment Opportunity questions."""
    try:
        dropdown_questions = page.query_selector_all('//div[@class="application-question"]')
        for dropdown_question in dropdown_questions:
            question = dropdown_question.query_selector('//div[@class="application-label"]')
            question_text = question.inner_text() if question else ''

            if question_text == 'Gender':
                dropdown = page.query_selector('//select[@name="eeo[gender]"]')
                dropdown.select_option(value='Female')
            elif question_text == '':
                dropdown = page.query_selector('//select[@name="eeo[race]"]')
                dropdown.select_option(index=5)
            elif question_text == 'Veteran status':
                dropdown = page.query_selector('//select[@name="eeo[veteran]"]')
                dropdown.select_option(value='I am a veteran')
            elif question_text == 'What is your location?':
                dropdown = page.query_selector('//select[@data-qa="candidate-location-select"]')
                dropdown.select_option(value='US')
    except Exception as e:
        print(f'Error filling equal employment questions: {str(e)}')

def fill_demographic_survey(page):
    """Fill out the demographic survey questions."""
    try:
        demographic_questions = page.query_selector_all('//div[contains(@id, "countrySurvey")]//li[@class="application-question"]')
        for demographic_question in demographic_questions:
            demographic_question_text = demographic_question.query_selector('//div[contains(@class, "application-label")]').inner_text()
            if 'What is your age range' in demographic_question_text:
                radio_buttons = demographic_question.query_selector_all('//input[@type="radio"]')
                for radio_button in radio_buttons:
                    if '21' in radio_button.get_attribute('value'):
                        radio_button.check()
            elif 'I identify my ethnicity as' in demographic_question_text:
                checkboxes = demographic_question.query_selector_all('//ul[@data-qa="checkboxes"]//li')
                for checkbox in checkboxes:
                    if 'White' in checkbox.inner_text() or 'Asian' in checkbox.inner_text():
                        checkbox.query_selector('//input').check()
            elif 'What gender do you identify as?' in demographic_question_text:
                radio_buttons = demographic_question.query_selector_all('//input[@type="radio"]')
                for radio_button in radio_buttons:
                    if 'Male' in radio_button.get_attribute('value'):
                        radio_button.check()
            elif 'My preferred pronouns are:' in demographic_question_text:
                radio_buttons = demographic_question.query_selector_all('//input[@type="radio"]')
                for radio_button in radio_buttons:
                    if 'He/His' in radio_button.get_attribute('value'):
                        radio_button.check()
            elif 'Where did you first hear about' in demographic_question_text:
                radio_buttons = demographic_question.query_selector_all('//input[@type="radio"]')
                for radio_button in radio_buttons:
                    if 'LinkedIn' in radio_button.get_attribute('value'):
                        radio_button.check()
    except Exception as e:
        print(f'Error filling demographic survey: {str(e)}')

def main():
    # Constants
    URL = 'https://jobs.lever.co/givebutter/15a4b3c1-6989-47f0-8a66-cb2473793be5'
    
    RESUME_FILE = os.path.abspath(r'<resume file path>')
    if not os.path.exists(RESUME_FILE):
        # raise FileNotFoundError(f'Resume file not found: {RESUME_FILE}')
        print(f'Resume file not found: "{RESUME_FILE}"')
        return
    
    try:
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(URL)

        # Click 'Apply for this job' button
        button = page.query_selector('//a[@data-qa="show-page-apply"]')
        if not button:
            raise Exception('Button not found')
        button.click()

        # Wait for the application form to load
        page.wait_for_selector('//input[@id="resume-upload-input"]', timeout=10000)
        time.sleep(1)

        # Fill out the application
        page.set_input_files('//input[@id="resume-upload-input"]', RESUME_FILE)
        time.sleep(2)

        fill_form(page)
        fill_custom_questions(page)
        fill_equal_employment_questions(page)
        fill_demographic_survey(page)

        # Wait for user to manually submit the form
        print('Press Enter in the console when you\'re done submitting')
        input()        

    except TimeoutError:
        print('Timed out waiting for the application form to load.')
    except Exception as e:
        print(f'An error occurred: {str(e)}')
    finally:
        browser.close()
        playwright.stop()

main()