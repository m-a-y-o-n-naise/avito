import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()
driver.get("<https://qa-mesto.praktikum-services.ru/>")

# Выполните авторизацию
driver.find_element(By.ID, "email").send_keys("some_email")
driver.find_element(By.ID, "password").send_keys("some_password")
driver.find_element(By.CLASS_NAME, "auth-form__button").click()

# Добавьте явное ожидание для загрузки списка карточек контента
WebDriverWait(driver, 3).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "places__list")))

# Запомните title последней карточки
title_before = driver.find_element(By.XPATH, "//li[@class='places__item card']//h2[@class='card__title']").text

# Кликните по кнопке добавления нового контента
driver.find_element(By.CLASS_NAME, "profile__add-button").click()

# Сгенерируйте новое место и введите его в поле названия
new_title = f"Москва{random.randint(100, 999)}"
driver.find_element(By.NAME, "name").send_keys(new_title)

# Введите ссылку на изображение
driver.find_element(By.NAME, "link").send_keys(
    "<https://code.s3.yandex.net/qa-automation-engineer/python/files/photoSelenium.jpeg>")

# Сохраните контент
driver.find_element(By.XPATH, ".//form[@name='new-card']/button[text()='Сохранить']").click()

# Дождитесь, пока появится кнопка удаления карточки
WebDriverWait(driver, 3).until(expected_conditions.visibility_of_element_located(
    (By.XPATH, "//li[@class='places__item card'][1]/button[@class='card__delete-button card__delete-button_visible']")))

# Проверьте, что на карточке отображается верное название
title_after = driver.find_element(By.XPATH, "//li[@class='places__item card']//h2[@class='card__title']")
assert title_after.text == new_title

# Запомните количество карточек до удаления
cards_before = len(driver.find_elements(By.XPATH, "//li[@class='places__item card']"))

# Удалите карточку
driver.find_element(By.XPATH,
                    "//li[@class='places__item card'][1]/button[@class='card__delete-button card__delete-button_visible']").click()
WebDriverWait(driver, 3).until(expected_conditions.text_to_be_present_in_element(
    (By.XPATH, "//li[@class='places__item card']//h2[@class='card__title']"), title_before))

# Проверьте, что количество карточек стало на одну меньше
cards_after = len(driver.find_elements(By.XPATH, "//li[@class='places__item card']"))
assert cards_before - cards_after == 1

driver.quit()