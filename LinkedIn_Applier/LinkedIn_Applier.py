from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from time import sleep


class LinkedIn_Applier:
    def __init__(self, username, password, job_title, city, driver_path, phone, resume_path):
        self.username = username
        self.password = password
        self.job_title = job_title
        self.city = city
        self.driver_path = driver_path
        self.phone = phone
        self.resume_path = resume_path

    def url_generator(self):
        base_url = 'https://www.linkedin.com/jobs/search/?keywords='
        job_title = self.job_title.replace(' ', '%20')
        city = self.city.replace(' ', '%20')
        url = base_url + job_title + '&location=' + city
        return url

    def init_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=options)
        self.driver.wait = WebDriverWait(self.driver, 10)
        return self.driver

    def find_element(self, category, name):
        cat = None
        if category == 'ID':
            cat = By.ID
        elif category == 'CLASS_NAME':
            cat = By.CLASS_NAME
        return WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((cat, name)))

    def find_all_elements(self, category, name):
        cat = None
        if category == 'ID':
            cat = By.ID
        elif category == 'CLASS_NAME':
            cat = By.CLASS_NAME
        return WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((cat, name)))

    def login(self):
        """Login to LinkedIn"""

        self.driver.get('https://www.linkedin.com/')

        self.find_element('CLASS_NAME', 'login-email').send_keys(self.username)
        self.find_element('CLASS_NAME', 'login-email').send_keys(Keys.TAB)

        self.find_element('CLASS_NAME', 'login-password').send_keys(self.password)

        self.find_element('ID', 'login-submit').click()

    def search_jobs(self):
        url = self.url_generator()
        self.driver.get(url)

        # Apply filters
        self.find_element('CLASS_NAME', 'search-filters-bar__all-filters').click()

        easy = int(input('Where is easy apply?'))

        for i in [0, easy, 7, 8, 30, 31, 32]:
            self.find_all_elements('CLASS_NAME', 'search-s-facet-value__label')[i].click()


        self.find_element('CLASS_NAME', 'search-advanced-facets__button--apply').click()
        sleep(2)

        # Sort by Post date
        self.find_element('ID', 'sort-by-select-trigger').click()
        self.find_element('CLASS_NAME', 'jobs-search-dropdown__option-button--date').click()

        sleep(2)

        try:
            total_pages = int(self.find_all_elements('CLASS_NAME', 'artdeco-pagination__indicator')[-1].text)

        except TimeoutException:
            total_pages = 1

        jobs = {'1-click': 0, 'easy_apply': 0, 'already_applied': 0}

        for page in range(1, total_pages+1):

            jobs_list = self.find_all_elements('CLASS_NAME', "occludable-update")

            for job in jobs_list:
                self.apply_to_job(job, jobs)

            if page < total_pages:
                # Move to next page
                self.find_element('ID', 'view-select-trigger').click()
                self.find_element('CLASS_NAME', 'jobs-search-dropdown__option-button--single').click()
                sleep(2)

                self.find_element('ID', 'view-select-trigger').send_keys(Keys.END)
                sleep(2)
                self.find_element('CLASS_NAME', 'artdeco-pagination__button--next').click()
                sleep(2)

                self.find_element('ID', 'view-select-trigger').click()
                self.find_element('CLASS_NAME', 'jobs-search-dropdown__option-button--split').click()
                sleep(2)

        print('Jobs:', jobs)

    def apply_to_job(self, job, jobs):
        ActionChains(self.driver).move_to_element(WebDriverWait(job, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "job-card-search__link-wrapper")))).click().perform()

        try:
            # Easy apply
            button = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'jobs-apply-button__text'))).text

            if button == '1-Click Apply':
                self.find_element('CLASS_NAME', 'jobs-apply-button--top-card').click()
                jobs['1-click'] += 1
                sleep(2)
                self.find_element('CLASS_NAME', 'artdeco-dismiss').click()
            else:
                jobs['easy_apply'] += 1

        except TimeoutException:
            jobs['already_applied'] += 1
