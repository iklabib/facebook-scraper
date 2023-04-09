import config

def login(context):
    base_url = 'https://m.facebook.com/login'

    page = context.new_page()
    page.goto(base_url)

    email, password = config.load()['auth'].values()

    page.locator('xpath=//*[@id="m_login_email"]').fill(email)
    page.locator('xpath=//*[@id="m_login_password"]').fill(password)
    page.locator('xpath=//*[@id="login_password_step_element"]/button').click()
