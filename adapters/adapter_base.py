
import logging
import os

import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options as ChromeOptions



logger = logging.getLogger(__name__)


class SeleniumConfirmation:
    def __init__(self) -> None:
        self.options = ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--lang=ru')
        self.options.add_argument("--window-size=1366,1080")
        profile_path = os.path.join(os.path.expanduser("~"), ".profile1")
        self.options.add_argument(f"--user-data-dir={profile_path}")
        self.driver = webdriver.Chrome(options=self.options)



    def login_up_products(self) -> None:
        try:
            self.driver.get("https://funpay.com/account/login")
            try:
                WebDriverWait(self.driver, 5).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, "a.social-login-item-vk"))
                ).click()
                try:
                    WebDriverWait(self.driver, 5).until(
                        ec.presence_of_element_located((By.XPATH,
                                             "//*[contains(text(), \"FunPay\")]")))
                    time.sleep(3)
                    WebDriverWait(self.driver, 5).until(
                        ec.presence_of_element_located((By.XPATH,
                                             "//*[contains(text(), \"FunPay\")]")))
                    self.driver.save_screenshot(os.path.join(os.getcwd(), 'qr.png'))
                except Exception as exc:
                    logger.error(f'Ошибка: Не появился qr')
                time.sleep(100)
            except Exception as exc:
                logger.error(f'Ошибка: Нет окна авторизации через вк')

            try:
                WebDriverWait(self.driver, 5).until(
                    ec.presence_of_element_located((By.CLASS_NAME, "user-link-photo"))).click()
            except Exception as exc:
                logger.error(f'Ошибка: Не смог войти в настройки лк')

            try:
                self.driver.find_element(By.XPATH, "//*[contains(text(), \"Профиль\")]").click()
            except Exception as exc:
                logger.error(f'Ошибка: Не нашел кнопку входа в профиль')
            try:
                links = self.driver.find_elements(By.CSS_SELECTOR, 'a.btn.btn-default.btn-plus')
                all_products = []
                for link in links:
                    href = link.get_attribute("href")
                    all_products.append(href)

                for product in all_products:
                    try:
                        self.driver.get(product)
                        self.driver.find_element(By.XPATH, "//*[contains(text(), \"Поднять предложения\")]").click()
                        time.sleep(3)
                    except Exception as exc:
                        logger.error(f'Ошибка: Не смог поднять товар {exc}')


            except Exception as exc:
                logger.error(f'Ошибка: Не нашел ссылки на товары {exc}')
        except Exception as exc:
            logger.error(f'Ошибка: Всё упало {exc}')

        finally:
            self.driver.quit()