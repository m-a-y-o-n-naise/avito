from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

driver = webdriver.Chrome()
driver.get("https://qa-mesto.praktikum-services.ru/")

# Выполните авторизацию
driver.find_element(By.ID, "email").send_keys("some_email")
driver.find_element(By.ID, "password").send_keys("some_password")
driver.find_element(By.CLASS_NAME, "auth-form__button").click()

# Добавьте явное ожидание загрузки страницы
WebDriverWait(driver, 3).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "header__user")))

# Кликните по изображению профиля
driver.find_element(By.CLASS_NAME, "profile__image").click()

# В поле ссылки на изображение введите ссылку, используйте переменную avatar_url
avatar_url = "https://code.s3.yandex.net/qa-automation-engineer/python/files/avatarSelenium.png"
driver.find_element(By.ID, "owner-avatar").send_keys(avatar_url)

# Сохраните новое изображение
driver.find_element(By.XPATH, ".//form[@name='edit-avatar']/button[text()='Сохранить']").click()

# Проверьте атрибут style для элемента изображения профиля
style = driver.find_element(By.CLASS_NAME, "profile__image").get_attribute('style')
assert avatar_url in style

driver.quit()
