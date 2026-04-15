import pytest
from playwright.sync_api import expect


def test_iphone_filters(page):
    """Тест: применение фильтров для iPhone 15"""

    # 1. Открыть сайт
    page.goto("https://www.avito.ru/")

    # 2. Поиск iPhone 15
    page.locator('[data-marker="search-form/suggest/input"]').click()
    page.locator('[data-marker="search-form/suggest/input"]').fill("iPhone 15")
    page.locator('[data-marker="search-form/submit-button"]').click()

    # 3. Открыть фильтры и выбрать объёмы памяти все попытки одного и того же
    # memory_block = page.get_by_role("heading", name="Память").locator("..").locator("..")
    # memory_block.get_by_role("button", name="Показать ещё").click() функционал плавающий
    # Находим заголовок
    memory_header = page.get_by_role("heading", name="Память").first
    # Поднимаемся до общего родительского блока
    filter_block = memory_header.locator(
        "xpath=ancestor::div[contains(@class, 'styles-module-root-yVYmx')]"
    )
    filter_block.locator('div.expand-list-expandButton-MBDEk a').click()
    # page.locator('[data-marker="params[112691]/show-button"]').click()
    # page.locator('input[value="757884"]').check()  # 256 ГБ
    # page.get_by_text("256 ГБ", exact=False).first.click()
    # page.locator('input[value="757885"]').check()  # 512 ГБ
    # page.get_by_text("512 ГБ", exact=False).first.click()
    # page.locator('input[value="757884"]').locator('..').click(force=True)
    # page.locator('input[value="757885"]').locator('..').click(force=True)
    page.locator('label:has-text("256 ГБ")').first.click()
    page.locator('label:has-text("512 ГБ")').first.click()

    # 5. Выбрать тип SIM
    # page.locator('input[value="3338066"]').check()  # SIM + e-SIM
    # page.locator('input[value="3338066"]').locator('..').click(force=True)
    page.locator('label:has-text("SIM + eSIM")').first.click()

    # 6. Выбрать состояние
    # page.locator('input[value="2850684"]').locator('..').click(force=True)  # Новое
    # page.locator('input[value="2850685"]').check()  # Отличное
    # page.locator('input[value="2850686"]').check()  # Хорошее
    page.locator('label:has-text("Новое")').first.click()
    page.locator('label:has-text("Отличное")').first.click()
    page.locator('label:has-text("Хорошее")').first.click()
    page.locator("label").filter(has_text="Хорошее").click()  # Хорошее нажатие по label для отмены

    # 7. Дополнительные опции
    page.locator("label").filter(has_text="Есть возврат").click()

    # 8. Приоритет по локации
    # page.locator('[name="localPriority"]').check()
    page.locator('label:has([name="localPriority"])').first.click()

    # 9. Сортировка
    # page.locator('[data-marker="sort/title"]').click()
    # Клик по кнопке с точным названием
    page.get_by_role("button", name="Сортировка").click()
    # page.locator('[data-marker="sort/custom-option(1)"]').click()  # Сначала дешевле
    page.get_by_role("button", name="Сортировка").click()

    # ✅ ДОБАВЛЯЕМ ПРОВЕРКИ
    # Проверка, что результаты загрузились
    expect(page.locator('[data-marker="catalog-serp"]')).to_be_visible() #  есть список
    expect(page.locator('[data-marker="item"]')).to_be_visible() #  для конкретного результата в списках

    # Проверка, что в результатах есть iPhone
    first_item = page.locator('[data-marker="item"]').first
    expect(first_item).to_contain_text("iPhone", timeout=10000)

    # Проверка, что цены отображаются
    prices = page.locator('[data-marker="item-price-value"]').all_text_contents()
    assert len(prices) > 0, "Цены не найдены"

    # Проверка цены (что сортировка сработала)
    prices_num = [int(p.replace('₽', '').replace(' ', '')) for p in prices[:10]]
    assert all(prices_num[i] <= prices_num[i + 1] for i in range(len(prices_num) - 1))

    # Можно сохранить скриншот для отчёта
    page.screenshot(path="results/avito_filters.png")

#draft
import re
import pytest
from playwright.sync_api import Playwright, sync_playwrightц


def run(playwright: Playwright) -> None: #  playwright: Playwright — это аннотация типа.
    # Она говорит, что в переменную playwright мы ожидаем объект класса Playwright.
    # Сам объект playwright — это главная "входная точка" в библиотеку.
    # Через него мы получаем доступ ко всем браузерам (chromium, firefox, webkit)
    browser = playwright.chromium.launch(headless=False)  #  метод, который физически запускает браузер
    context = browser.new_context() #  метод, который создает новый контекст браузера
    # создаются свои cookies, локальное хранилище (localStorage), история, настройки (размер окна, геолокация и т.д.)
    # Это позволяет изолировать тесты друг от друга. Ты можешь создать >=2 контекста в одном браузере
    page = context.new_page() #  создает новую вкладку (страницу) внутри текущего контекста
    page.goto("https://www.avito.ru/")

    page.locator('[data-marker="search-form/suggest/input"]').click()
    page.locator('[data-marker="search-form/suggest/input"]').fill("iPhone 15")
    page.locator('[data-marker="search-form/submit-button"]').click()

    page.locator('[data-marker="params[112691]/show-button"]').click()
    page.locator('input[value="757884"]').check() #  объем 256
    page.locator('input[value="757885"]').check() #  объем 512
    # page.get_by_role("button", name="Показать ещё").first.click()

    page.locator('input[value="3338066"]').check() #  sim + e-sim

    page.locator('input[value="2850684"]').check() #  состояние новое
    page.locator('input[value="2850685"]').check() #  Отличное
    page.locator('input[value="2850686"]').check() #  Хорошее
    page.locator("label").filter(has_text="Хорошее").click() #  Хорошее нажатие по label

    page.locator("label").filter(has_text="Есть возврат").click() #  дополнительная опция

    page.locator('[name="localPriority"]').check() #  приоритет по локации

    page.locator('[data-marker="sort/title"]').click() #  сортировка
    page.locator('[data-marker="sort/custom-option(1)"]').click() #  сначала дешевле

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

#codagen

import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.avito.ru/")
    page.get_by_placeholder("Поиск по объявлениям").click()
    page.get_by_label("", exact=True).fill("iPhone 15")
    page.get_by_role("button", name="Найти").click()
    page.get_by_role("button", name="Показать ещё").first.click()
    page.locator("label").filter(has_text="512 ГБ").click()
    page.locator("label").filter(has_text="1 ТБ").click()
    page.get_by_role("button", name="Показать ещё").first.click()
    page.locator("label").filter(has_text="SIM + eSIM").click()
    page.locator("label").filter(has_text="Новое").click()
    page.locator("label").filter(has_text="Отличное").click()
    page.locator("label").filter(has_text="Хорошее").click()
    page.locator("label").filter(has_text="Отличное").click()
    page.locator("label").filter(has_text="Хорошее").click()
    page.locator("label").filter(has_text="Есть возврат").click()
    page.locator(".styles-module-switcherCircle-PlbWD").click()
    page.locator(".styles-module-toggle-tnaHU").first.click()
    page.get_by_role("button", name="Сортировка").click()
    page.get_by_role("checkbox", name="Дешевле").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)