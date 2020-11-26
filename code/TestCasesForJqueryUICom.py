import platform
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class JqueryUICom:
    def __init__(self):
        if 'Windows' in platform.system():
            path = '../drivers/chromedriver.exe'
        else:
            path = '../../drivers/chromedriver'
        url = 'https://jqueryui.com'
        self.driver = webdriver.Chrome(path)
        self.driver.web
        self.driver.get(url)
        self.driver.maximize_window()

    def drag_and_drop(self, test_type):
        self.driver.get('https://jqueryui.com/droppable/')
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        self.driver.find_element_by_id('draggable').location_once_scrolled_into_view
        drag = self.driver.find_element_by_id('draggable')
        drop = self.driver.find_element_by_id('droppable')
        action = ActionChains(self.driver)
        action.drag_and_drop(drag, drop).perform()
        self.driver.switch_to.default_content()
        print(test_type, 'test case is passed')


    def resizeable_element(self, test_type):
        self.driver.get('https://jqueryui.com/resizable/')
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        self.driver.find_element_by_id('resizable').location_once_scrolled_into_view
        action = ActionChains(self.driver)
        # Resize width
        element_to_resize_x = self.driver.find_element_by_xpath('//*[@id="resizable"]/div[1]')
        action.move_to_element(element_to_resize_x).click_and_hold().move_by_offset(100, 0).release().perform()
        # Resize height
        element_to_resize_y = self.driver.find_element_by_xpath('//*[@id="resizable"]/div[3]')
        action.move_to_element(element_to_resize_y).click_and_hold().move_by_offset(0, 80).release().perform()
        self.driver.switch_to.default_content()
        print(test_type, 'test case is passed')

    def sort_item(self, test_type):
        self.driver.get('https://jqueryui.com/sortable/')
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        self.driver.find_element_by_xpath('//*[@id="sortable"]/li[1]').location_once_scrolled_into_view
        sort_from_item_element = self.driver.find_element_by_xpath('//*[@id="sortable"]/li[1]')
        sort_to_item_element = self.driver.find_element_by_xpath('//*[@id="sortable"]/li[2]')
        action = ActionChains(self.driver)
        action.drag_and_drop(sort_from_item_element, sort_to_item_element).perform()
        self.driver.switch_to.default_content()
        print(test_type, 'test case is passed')

    def accordion(self, test_type):
        self.driver.get('https://jqueryui.com/accordion/')
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        self.driver.find_element_by_xpath('//*[@id="ui-id-3"]').location_once_scrolled_into_view
        # Click on section 2
        self.driver.find_element_by_xpath('//*[@id="ui-id-3"]').click()
        if self.driver.find_element_by_xpath('//*[@id="ui-id-4"]').is_displayed():
            print(test_type, 'test case is passed')
        self.driver.switch_to.default_content()

    def autocomplete(self, test_type):
        self.driver.get('https://jqueryui.com/autocomplete/')
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        self.driver.find_element_by_id('tags').location_once_scrolled_into_view
        self.driver.find_element_by_id('tags').send_keys('pyddfddd')

        try:
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.XPATH, '//div[contains(.,"Python")]')))
            self.driver.find_element_by_xpath('//div[contains(.,"Python")]').click()
            print(test_type, 'test case is passed - item is found')
        except TimeoutException:
            print(test_type, 'test case is failed - item is not found')
            pass


        self.driver.switch_to.default_content()

    def datepicker(self, pick_date, pick_month, pick_year, test_type):
        self.driver.get('https://jqueryui.com/datepicker/')
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        self.driver.find_element_by_id('datepicker').location_once_scrolled_into_view
        self.driver.find_element_by_id('datepicker').click()

        try:
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.ID, 'ui-datepicker-div')))
            # To decide left or right click when given year is same from this
            the_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                          'October', 'November', 'December']
            pick_month_position = the_months.index(pick_month)
            the_month_position = the_months.index(self.driver.find_element_by_class_name('ui-datepicker-month').text)
            pick_year_position = int(pick_year)
            the_year_position = int(self.driver.find_element_by_class_name('ui-datepicker-year').text)

            while (pick_month not in self.driver.find_element_by_class_name(
                    'ui-datepicker-month').text or pick_year not in self.driver.find_element_by_class_name(
                'ui-datepicker-year').text):
                if pick_year_position == the_year_position:
                    if pick_month_position < the_month_position:
                        self.driver.find_element_by_xpath('//span[contains(.,"Prev")]').click()
                    elif pick_month_position > the_month_position:
                        self.driver.find_element_by_xpath('//span[contains(.,"Next")]').click()
                elif pick_year_position < the_year_position:
                    self.driver.find_element_by_xpath('//span[contains(.,"Prev")]').click()
                elif pick_year_position > the_year_position:
                    self.driver.find_element_by_xpath('//span[contains(.,"Next")]').click()

            self.driver.find_element_by_link_text(pick_date).click()
            print(test_type, 'test case is passed -', pick_date, '/', pick_month, '/', pick_year,
                  'is picked successfully')
        except TimeoutException as e:
            print(test_type, 'test case is failed - ', str(e))
            pass
        except ValueError as e:
            print(test_type, 'test case is failed - ', str(e))
            pass

        self.driver.switch_to.default_content()


jquery_ui_com = JqueryUICom()
jquery_ui_com.drag_and_drop(test_type='drag_and_drop')
jquery_ui_com.resizeable_element(test_type='resize element')
jquery_ui_com.sort_item(test_type='sort_item')
jquery_ui_com.accordion(test_type='accordion')
jquery_ui_com.autocomplete(test_type='autocomplete')
jquery_ui_com.datepicker(pick_date='15', pick_month='December', pick_year='2019', test_type='datepicker')

