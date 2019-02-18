from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Config import *
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
from aditing_detail import *


option = webdriver.ChromeOptions()
option.add_argument('disable-infobars')
browser = webdriver.Chrome(chrome_options=option)
browser.maximize_window()
wait = WebDriverWait(browser, 10)
def login():
    #页面加载
    browser.get(login_url)
    login_handle = browser.current_window_handle
    # print(login_handle)
    user_name = wait.until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR,
            'body > form > table > tbody > tr > td:nth-child(3) > table > tbody > '
            'tr:nth-child(2) > td:nth-child(2) > input')))
    password = wait.until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR,
            'body > form > table > tbody > tr > td:nth-child(3) > table > tbody > '
            'tr:nth-child(3) > td:nth-child(2) > input'
        ))
    )
    verify = wait.until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR,
            'body > form > table > tbody > tr > td:nth-child(3) > table > tbody > '
            'tr:nth-child(5) > td:nth-child(2) > input.login_input.adm_verify.adm_verify_new'
        ))
    )
    submit = wait.until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR,
            '#login_btn'
        ))
    )

    #输入登陆账号信息
    user_name.send_keys(adm_name)
    password.send_keys(adm_password)
    verify.send_keys(adm_verify)

    #模拟登陆
    submit.click()


def aditing_detail_html():
    cookies = browser.get_cookies()
    # print(cookies)
    js = 'window.open("{}");'.format(my_auditing)
    browser.execute_script(js)
    browser.get(my_auditing)
    auditing_handle = browser.current_window_handle
    browser.switch_to_window(auditing_handle)

    #点击审核操作
    auditing_detail = wait.until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR,
            '#dataTable > tbody > tr:nth-child(3) > td:nth-child(15) > a'
        ))
    )
    auditing_detail.click()

    aditing_html = browser.page_source
    return aditing_html
    # doc = pq(html)
    # print(doc)


def parse_aditing_detail(aditing_html):
    insight = get_Insight(aditing_html)
    print(insight)
    # xuexin_dict = get_xuexin(aditing_html)
    commu_dict = get_communicate(aditing_html)
    family_identity = get_family_identity(aditing_html)
    credit91 = get_credit91(aditing_html)


def main():
    login()
    aditing_html = aditing_detail_html()
    # print(aditing_html)
    parse_aditing_detail(aditing_html)


if __name__ == '__main__':
    main()