import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle

map_of_streams_actual1 = {
    'Business Analysis': ['business analyst'], 'Business Intelligence': ['business intelligence', 'data analyst'],
    'Cloud Computing': ['cloud', 'azure'], 'Compliance and Risk': ['compliance and risk', 'risk analyst'],
    'Cyber Security': ['cyber security'], 'Development': ['software developer']}

map_of_streams_actual2 = {
    'Information Security Management': ['information security'], 'IT Service Management': ['technical support'], 'Robotic Process Automation': ['rpa'],
    'Testing': ['software tester', 'software test', 'java test engineer']}

map_of_streams_3 = {
    'PMO': ['project manager']
}
map_of_streams_dev = {
    'Development': ['software developer']
}


job_titles = []
links = []
streams = []
descriptions = []


def scrape_web_job_description(map_of_streams):
    # specify driver path
    DRIVER_PATH = '/Users/kaykay/Downloads/chromedriver'

    # stop pop-ups
    chrome_options = Options()

    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-extensions")

    # Pass the argument 1 to allow and 2 to block
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1
    })

    driver = webdriver.Chrome(options=chrome_options, executable_path=DRIVER_PATH)
    driver.get('https://www.indeed.co.uk/advanced_search')
    # driver.find_element_by_id("popover-x").click()
    df_stream_description = pd.DataFrame()

    for stream, job_descriptions in map_of_streams.items():
        print(stream, ' >>>>>>>')

        for job_description in job_descriptions:
            print(job_description, '>>>>>')

            # Search in the advanced page
            # Input it also in the "With all these words in the title" box
            try:
                search_job = driver.find_element_by_xpath('//input[@id="as_and"]')
            except:
                print("")
            #                 close_popup = driver.find_element_by_id("popover-x")
            #                 close_popup.click()
            #                 close_cookie_popup = driver.find_element_by_id("onetrust-accept-btn-handler")
            #                 close_cookie_popup.click()
            search_job = driver.find_element_by_xpath('//input[@id="as_and"]')
            search_job.send_keys([job_description])
            driver.implicitly_wait(3)

            # Input it also in the "With these words in the title" box
            search_job = driver.find_element_by_xpath('//input[@id="as_ttl"]')
            search_job.send_keys([job_description])

            # for rpa look for robotic in the description as well
            if stream == 'Robotic Process Automation':
                search_job = driver.find_element_by_xpath('//input[@id="as_any"]')
                search_job.send_keys(['robotic'])

            driver.implicitly_wait(3)
            # set display limit of 30 results per page
            display_limit = driver.find_element_by_xpath('//select[@id="limit"]//option[@value="50"]')
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

            for i in range(1, 40):

                job_card = driver.find_elements_by_xpath('//div[contains(@class,"clickcard")]')

                for job in job_card:

                    try:

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
                #                     WebDriverWait(driver, 3).until(EC.alert_is_present(),
                #                                                     'Timed out waiting for PA creation ' +
                #                                                     'confirmation popup to appear.')

                #                     alert = browser.switch_to.alert
                #                     alert.accept()
                except ElementClickInterceptedException:
                    close_popup = driver.find_element_by_id("popover-x")
                    close_popup.click()

                except TimeoutException:
                    print("no alert")

                except NoSuchElementException:
                    try:
                        close_popup = driver.find_element_by_id("popover-x")
                        close_popup.click()

                    except:
                        try:
                            next_page = driver.find_element_by_xpath('//a[@aria-label="Next"]//span[@class="np"]')
                            next_page.click()
                            driver.implicitly_wait(3)
                        except:
                            break

                except:

                    next_page = driver.find_element_by_xpath('//a[@aria-label="Next"]//span[@class="np"]')
                    next_page.click()

                print("Page: {}".format(str(i + 2)))

            # we need to be able to clear search and go on to the next role
            # go to the clear advanced search page to insert new job description
            driver.get('https://www.indeed.co.uk/advanced_search')

    for link in links:
        try:

            driver.get(link)
            jd = driver.find_element_by_xpath('//div[@id="jobDescriptionText"]').text
        except NoSuchElementException:
            print(" empty website")
            jd = ""

        descriptions.append(jd)

    del links[:]

    df_stream_description['Title'] = job_titles
    df_stream_description['Description'] = descriptions
    df_stream_description['Stream'] = streams

    return df_stream_description
# df_pmo = scrape_web_job_description(map_of_streams_)
# print(df_pmo.info())

df_dev = scrape_web_job_description(map_of_streams_dev)
print(df_dev.info())
# map_of_streams_test = {
#     'Robotic Process Automation': ['rpa']}
# df1 = scrape_web_job_description(map_of_streams_actual1)
# print(df1.head())
# print(df1.tail())
# print(df1['Stream'].unique())
#
# with open(Path(__file__).parent / 'df1_jd', 'wb') as fh:  # notice that you need the 'wb' for the dump
#     pickle.dump(df1_mo, fh)

# df2 = scrape_web_job_description(map_of_streams_actual2)
# print(df2.info())
with open('/Users/kaykay/Downloads/RecognitionEngineProject/recognitionengine/src/ml_determine_stream/df_dev', 'wb') as fh:  # notice that you need the 'wb' for the dump
    pickle.dump(df_dev, fh)