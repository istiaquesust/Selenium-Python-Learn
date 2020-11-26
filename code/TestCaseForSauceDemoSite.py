import platform
from selenium import webdriver
from selenium.webdriver.support.select import Select


class SauceDemo:
    def __init__(self):
        if 'Windows' in platform.system(): # windows
            path = '../drivers/chromedriver.exe'
        else:
            path = '../drivers/chromedriver'
        url = 'https://www.saucedemo.com/'
        self.driver = webdriver.Chrome(path)
        self.driver.get(url)
        self.driver.maximize_window()
        self.price = []
        self.products = []
        self.total_price = 0
        self.search_product_number = 0

    def login(self):
        self.driver.find_element_by_css_selector('#user-name').send_keys('standard_user')
        self.driver.find_element_by_css_selector('#password').send_keys('secret_sauce')
        self.driver.find_element_by_css_selector('#login-button').click()

        success_login_expected_url = 'https://www.saucedemo.com/inventory.html'
        if self.driver.current_url.__contains__(success_login_expected_url):
            print('Login success')
        else:
            print('Login failed')

    def sort_items(self):
        # Sort by low price to high price
        select = Select(self.driver.find_element_by_css_selector('#inventory_filter_container > select'))
        select.select_by_value('lohi')

    def add_to_cart(self, order_products=[], max_price=False, min_price=False):
        self.search_product_number = len(order_products)
        self.driver.get('https://www.saucedemo.com/inventory.html')
        self.total_price = 0
        product_elements = self.driver.find_elements_by_class_name('inventory_item_name')
        price_elements = self.driver.find_elements_by_class_name('inventory_item_price')

        # Load products and prices in List variables
        if not self.products and not self.price:
            for price_element, product_element in zip(price_elements, product_elements):
                self.products.append(str(product_element.text))

                price_with_sign = str(price_element.text)
                price_without_sign = price_with_sign.replace('$', '')
                self.price.append(float(price_without_sign))

        if min_price:
            self.total_price = min(self.price)
            min_price_position = self.price.index(min(self.price)) + 1
            add_to__cart_xpath = '//*[@id="inventory_container"]/div/div[' + str(min_price_position) + ']/div[3]/button'
            self.driver.find_element_by_xpath(add_to__cart_xpath).location_once_scrolled_into_view
            self.driver.find_element_by_xpath(add_to__cart_xpath).click()
        elif max_price:
            self.total_price = max(self.price)
            max_price_position = self.price.index(max(self.price)) + 1
            add_to__cart_xpath = '//*[@id="inventory_container"]/div/div[' + str(max_price_position) + ']/div[3]/button'
            self.driver.find_element_by_xpath(add_to__cart_xpath).location_once_scrolled_into_view
            self.driver.find_element_by_xpath(add_to__cart_xpath).click()
        elif len(order_products) <= len(self.products):
            for i in range(len(order_products)):
                for j in range(len(self.products)):
                    if order_products[i] in self.products[j]:
                        self.total_price += self.price[j]
                        product_position = j + 1
                        add_to__cart_xpath = '//*[@id="inventory_container"]/div/div[' + str(
                            product_position) + ']/div[3]/button'
                        self.driver.find_element_by_xpath(add_to__cart_xpath).location_once_scrolled_into_view
                        self.driver.find_element_by_xpath(add_to__cart_xpath).click()
                        break

    def order_product(self, test_type):
        self.driver.find_element_by_class_name('shopping_cart_container').click()
        self.driver.find_element_by_link_text('CHECKOUT').click()
        self.driver.find_element_by_id('first-name').send_keys('John')
        self.driver.find_element_by_id('last-name').send_keys('Doye')
        self.driver.find_element_by_id('postal-code').send_keys('12525')
        self.driver.find_element_by_css_selector('.cart_button').click()
        compare_price = str(self.driver.find_element_by_class_name('summary_subtotal_label').text)
        print(self.total_price, compare_price)
        if self.total_price is not 0 and str(self.total_price) in compare_price:
            self.driver.find_element_by_link_text('FINISH').location_once_scrolled_into_view
            self.driver.find_element_by_link_text('FINISH').click()
            if 'Finish' in self.driver.page_source:
                print(test_type, 'test case is passed - Order is finished successfully')
            else:
                print(test_type, 'test case is failed')
        elif self.total_price is 0 and self.search_product_number is not 0:
            print(test_type, 'test case is passed - No product is matched to order')
        elif self.search_product_number is 0:
            print(test_type, 'test case is passed - Product search list is empty')
            print(self.search_product_number)

        self.driver.implicitly_wait(5)  # seconds


# Instantiate and login to site
sauce_demo = SauceDemo()
sauce_demo.login()

# Test case 1: order maximum priced product
sauce_demo.add_to_cart(max_price=True)
sauce_demo.order_product(test_type='order_max_priced_product')

# Test case 2: order minimum priced product
sauce_demo.add_to_cart(min_price=True)
sauce_demo.order_product(test_type='order_min_priced_product')

# Test case 3: order specific products that match with given keywords
sauce_demo.add_to_cart(order_products=['Jacket', 'Bike Light'])
sauce_demo.order_product(test_type='order_specific_products')
