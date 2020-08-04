from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from cleaning_and_reading import cv_cleaning

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException
import time
import pandas as pd

# map_of_streams_e.g. = {'Development': ['software developer'], 'Business Intelligence': ['business intelligence','data analyst']}


map_of_streams_actual = {
    'Business Analysis': ['business analyst'], 'Business Intelligence': ['business intelligence', 'data analyst'],
    'Cloud Computing': ['cloud', 'azure'], 'Compliance and Risk': ['compliance and risk', 'risk analyst'],
    'Cyber Security': ['cyber security'], 'Development': ['software developer'],
    'Information Security Management': ['information security'], 'IT Service Management': ['technical support'],
    'PMO': ['project manager'], 'Robotic Process Automation': ['rpa'],
    'Testing': ['software tester', 'software test', 'java test engineer']}

job_titles = []
links = []
streams = []
descriptions = []


def scrape_web_job_description(map_of_streams):
    # specify driver path
    DRIVER_PATH = '/Users/santiagomasip/Downloads/chromedriver'

    # stop pop-ups
    chrome_options = Options()
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--disable-notifications")
    # chrome_options.add_argument("--disable-popup-blocking")

    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-extensions")

    # Pass the argument 1 to allow and 2 to block
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1
    })

    # prefs = {}
    # prefs["profile.default_content_settings.cookies"] = 2
    # chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options, executable_path=DRIVER_PATH)

    driver.get('https://www.indeed.co.uk/advanced_search')
    df_stream_description = pd.DataFrame()


    for stream, job_descriptions in map_of_streams.items():

        # BA, BUSINESS ANALYSIS
        for job_description in job_descriptions:

            # Search in the advanced page
            # Input it also in the "With all these words in the title" box
            try:
                search_job = driver.find_element_by_xpath('//input[@id="as_and"]')
            except:
                # this might need to be an if statement
                close_popup = driver.find_element_by_id("popover-x")
                close_popup.click()
                close_cookie_popup = driver.find_element_by_id("onetrust-accept-btn-handler")
                close_cookie_popup.click()
            search_job = driver.find_element_by_xpath('//input[@id="as_and"]')
            search_job.send_keys([job_description])

            # Input it also in the "With these words in the title" box
            search_job = driver.find_element_by_xpath('//input[@id="as_ttl"]')
            search_job.send_keys([job_description])

            # for rpa loof for robotic in the description as well
            if(stream == 'Robotic Process Automation'):
                search_job = driver.find_element_by_xpath('//input[@id="as_any"]')
                search_job.send_keys(['robotic'])

            # set display limit of 30 results per page
            display_limit = driver.find_element_by_xpath('//select[@id="limit"]//option[@value="10"]')
            display_limit.click()
            # sort by date
            sort_option = driver.find_element_by_xpath('//select[@id="sort"]//option[@value="date"]')
            sort_option.click()
            search_button = driver.find_element_by_xpath('//*[@id="fj"]')
            search_button.click()
            try:
                close_cookie_popup = driver.find_element_by_id("onetrust-accept-btn-handler")
                close_cookie_popup.click()
            except:
                print("No cookies popup")

            # Save the data to a table
            # let the driver wait 3 seconds to locate the element before exiting out
            driver.implicitly_wait(3)

            for i in range(0, 2):

                job_card = driver.find_elements_by_xpath('//div[contains(@class,"clickcard")]')

                for job in job_card:

                    try:

                        # driver.implicitly_wait(3)
                        title = job.find_element_by_xpath('.//h2[@class="title"]//a').text
                        job_titles.append(title)
                        links.append(job.find_element_by_xpath('.//h2[@class="title"]//a').get_attribute(name="href"))
                        streams.append(stream)

                    except:
                        title = job.find_element_by_xpath('.//h2[@class="title"]//a').get_attribute(name="title")
                        job_titles.append(title)
                        links.append(job.find_element_by_xpath('.//h2[@class="title"]//a').get_attribute(name="href"))
                        streams.append(stream)

                try:
                    next_page = driver.find_element_by_xpath('//a[@aria-label={}]//span[@class="pn"]'.format(i + 2))
                    next_page.click()

                except ElementClickInterceptedException:

                    try:
                        time.sleep(8)  # Sometimes the pop-up takes time to load
                        close_cookie_popup = driver.find_element_by_id("onetrust-accept-btn-handler")
                        close_cookie_popup.click()

                    # except:
                    # next_page = driver.find_element_by_xpath('//a[.//span[contains(text(),"Next")]]')
                    # next_page.click()
                    except:
                        next_page = driver.find_element_by_xpath('//a[@aria-label="Next"]//span[@class="np"]')
                        next_page.click()

                print("Page: {}".format(str(i + 2)))

            # we need to be able to clear search and go on to the next role

            # go to the clear advanced search page to insert new job description

            driver.get('https://www.indeed.co.uk/advanced_search')

    for link in links:
        driver.get(link)
        jd = driver.find_element_by_xpath('//div[@id="jobDescriptionText"]').text
        # jd = cv_cleaning.clean_cv(jd)
        descriptions.append(jd)

    df_stream_description['Title'] = job_titles
    # df_stream_description['Link']=links
    df_stream_description['Description'] = descriptions

    df_stream_description['Stream'] = streams

    return df_stream_description


map_of_streams_test = {
    'Robotic Process Automation': ['rpa']}
df = scrape_web_job_description(map_of_streams_test)
print(df.head())
print(df.tail())
print(df['Stream'].unique())
