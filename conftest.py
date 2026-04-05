import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    """
        Фикстура Pytest для запуска браузера перед тестом
        и его закрытия после теста.
        """
    chrome_options = webdriver.ChromeOptions()  # создали объект для опций
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=640,480')
    # driver.maximize_window() полноэкранный режим
    driver = webdriver.Chrome(options=chrome_options)  # создали драйвер и передали в него настройки
    # driver.implicitly_wait(5)  # Неявное ожидание (до 5 сек.)
    yield driver  # Передаём драйвер в тест
    driver.quit()  # Закрываем браузер после теста


