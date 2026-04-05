import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# Инициализации и завершения веб-драйвера
@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# Тест для проверки функциональности добавления товара в корзину
def test_add_to_cart(browser):
    # Открываем веб-страницу интернет-магазина
    browser.get('https://www.avito.ru/')  # URL веб-сайта магазина

    # Находим товар на странице и кликаем на него
    product = browser.find_element(By.ID, 'product-id')  # ID элемента товара на странице
    product.click()

    # Нажимаем кнопку "Добавить в корзину"
    add_to_cart_button = browser.find_element(By.ID, 'add-to-cart')  # ID кнопки "Добавить в корзину"
    add_to_cart_button.click()

    # Проверяем, что товар добавлен в корзину
    cart_items = browser.find_element(By.ID, 'cart-items').text  # ID элемента, отображающего количество товаров в корзине
    assert cart_items == '1 item(s) in cart', f"Expected '1 item(s) in cart', but got '{cart_items}'"

class TestLogout:

    def test_logout(self, setup_teardown):
        driver = setup_teardown

        # Открыть веб-страницу (замените URL на актуальный)
        driver.get("https://example.com")

        # Найдем кнопку "Выйти" по тексту и кликнем на нее
        logout_button = driver.find_element(By.XPATH, ".//button[text()='Выйти']")
        logout_button.click()

        # После выхода из аккаунта, проверим, что мы перешли на страницу входа (замените URL на актуальный)
        login_page_url = "https://example.com/login"  # URL страницы входа
        assert driver.current_url == login_page_url