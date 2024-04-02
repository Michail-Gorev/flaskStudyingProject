from playwright.sync_api import Page, expect


# Идентификатор 1, проверка, что все поля на странице регистрации корректно отображены
def test_registration_fields(page: Page):
    page.goto('http://127.0.0.1:5000/profile')
    expect(page).to_have_title('Restricted')
    page.get_by_test_id('reg_link').click()
    expect(page).to_have_title('Регистрация')
    assert page.get_by_placeholder('Придумайте ник').is_visible()
    assert page.get_by_placeholder('Введите email').is_visible()
    assert page.get_by_placeholder('Придумайте надёжный пароль').is_visible()
    assert page.get_by_text('Укажите пол').is_visible()
