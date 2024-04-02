from playwright.sync_api import Page, expect


# Идентификатор 1, проверка, что все поля на странице входа корректно отображены
def test_registration_fields(page: Page):
    page.goto('http://127.0.0.1:5000/profile')
    expect(page).to_have_title('Restricted')
    page.get_by_test_id('login_btn').click()
    expect(page).to_have_title('Авторизация')
    assert page.get_by_placeholder('Введите ник').is_visible()
    assert page.get_by_placeholder('Введите пароль').is_visible()
    assert page.get_by_text('Войти').is_visible()
