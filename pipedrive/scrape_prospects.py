import time
import random
import string

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from soupsieve import select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
base_url = "https://www.pipedrive.com"

with open("chrome-user-agents.txt", "r") as f:
    user_agents = f.readlines()

opts = Options()
opts.add_argument(f"user-agent={user_agents[4]}")

name_generator = lambda x: "".join(random.choice(string.ascii_lowercase) for _ in range(x))
email_generator = lambda x: name_generator(x)+"@gmail.com"
pwd_generator = lambda x: name_generator(x)+"X1!"
phone_generator = lambda x: "6"+"".join(random.choice(string.digits) for _ in range(8))

element_wait_finder = lambda x: WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, x))
    )

element_clickable_finder = lambda x: WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, x))
    )

def main():
    """Automatize using pipedrive"""
    driver.get(base_url)
    
    # accept cookies on page
    accept_cookies_btn_xpath='//*[@id="onetrust-accept-btn-handler"]'
    accept_cookies_btn = element_wait_finder(accept_cookies_btn_xpath)
    accept_cookies_btn.click()

    # start signup for free trial
    free_trial_btn_xpath= '//*[@id="__next"]/section[1]/div/div/div[1]/div[1]/div[3]/div/div/button'
    free_trial_btn = element_wait_finder(free_trial_btn_xpath)
    free_trial_btn.click()
    
    enter_email_xpath = '//*[@id="__next"]/div/div[2]/div/form/div/div/input'
    enter_email_input = element_wait_finder(enter_email_xpath)
    generated_email = email_generator(10)
    enter_email_input.send_keys(generated_email)
    
    signup_continue_btn_xpath = '//*[@id="__next"]/div/div[2]/div/form/button'
    signup_continue_btn = element_wait_finder(signup_continue_btn_xpath)
    signup_continue_btn.click()
    
    enter_name_xpath = '//*[@id="__next"]/section/div/div/div/div/form/div[4]/div/div/div/input'
    enter_name_input = element_wait_finder(enter_name_xpath)
    generated_name = name_generator(10)
    enter_name_input.send_keys(generated_name)
    
    enter_mdp_xpath = '//*[@id="__next"]/section/div/div/div/div/form/div[5]/div/div/div/input'
    enter_mdp_input = element_wait_finder(enter_mdp_xpath)
    generated_mdp = pwd_generator(10)
    enter_mdp_input.send_keys(generated_mdp)
    
    enter_phone_xpath = '//*[@id="__next"]/section/div/div/div/div/form/div[6]/div/div/div[2]/div/div/div/input'
    enter_phone_input = element_wait_finder(enter_phone_xpath)
    generated_phone = phone_generator(10)
    enter_phone_input.send_keys(generated_phone)
    
    continue_to_role_xpath = '//*[@id="__next"]/section/div/div/div/div/form/div[8]/button'
    continue_to_role_btn = element_wait_finder(continue_to_role_xpath)
    continue_to_role_btn.click()
    
    # finalize subscription
    dropdown_role_xpath = '//*[@id="__next"]/section/div/div/div/div/form/div[3]/div/div/div[1]'
    dropdown_role_btn = element_wait_finder(dropdown_role_xpath)
    dropdown_role_btn.click()
    
    dropdown_role_select_xpath = '//*[@id="__next"]/section/div/div/div/div/form/div[3]/div/div/div[2]/div'
    dropdown_role_select_btn = element_clickable_finder(dropdown_role_select_xpath)
    dropdown_role_select_btn.click()
    
    dropdown_experience_xpath = '//*[@id="__next"]/section/div/div/div/div/form/div[4]/div/div/div[1]'
    dropdown_experience_btn = element_wait_finder(dropdown_experience_xpath)
    dropdown_experience_btn.click()
    
    dropdown_experience_select_xpath = '//*[@id="__next"]/section/div/div/div/div/form/div[4]/div/div/div[2]'
    dropdown_experience_select_btn = element_clickable_finder(dropdown_experience_select_xpath)
    dropdown_experience_select_btn.click()
    
    goal_select_xpath = '//*[@id="__next"]/section/div/div/div/div/form/div[5]/div/div/button[1]'
    goal_select_btn = element_wait_finder(goal_select_xpath)
    goal_select_btn.click()
    
    finalize_singup_xpath = '//*[@id="__next"]/section/div/div/div/div/form/div[6]/button'
    finalize_signup_btn = element_wait_finder(finalize_singup_xpath)
    finalize_signup_btn.click()
    
    company_name_xpath = '//*[@id="__next"]/section/div/div/div/div/form/div[3]/div/div/div/input'
    company_name_input = element_wait_finder(company_name_xpath)
    generated_company_name = name_generator(10)
    company_name_input.send_keys(generated_company_name)
    
    dropdown_company_kind_xpath = '//*[@id="__next"]/section/div/div/div/div/form/div[4]/div/div/div[1]'
    dropdown_company_kind_btn = element_wait_finder(dropdown_company_kind_xpath)
    dropdown_company_kind_btn.click()
    
    dropdown_company_select_xpath = '//*[@id="__next"]/section/div/div/div/div/form/div[4]/div/div/div[2]/div'
    dropdown_company_select = element_clickable_finder(dropdown_company_select_xpath)
    dropdown_company_select.click()
    
    dropdown_activity_sector_xpath = '//*[@id="__next"]/section/div/div/div/div/form/div[5]/div/div/div[1]'
    dropdown_activity_sector_btn = element_wait_finder(dropdown_activity_sector_xpath)
    dropdown_activity_sector_btn.click()
    
    dropdown_activity_select_xpath = '//*[@id="__next"]/section/div/div/div/div/form/div[5]/div/div/div[2]/div'
    dropdown_activity_select_btn = element_clickable_finder(dropdown_activity_select_xpath)
    dropdown_activity_select_btn.click()
    
    users_count_xpath = '//*[@id="__next"]/section/div/div/div/div/form/div[6]/div[2]/div/button[1]'
    users_count_btn = element_wait_finder(users_count_xpath)
    users_count_btn.click()
    
    subscribe_btn_xpath = '//*[@id="__next"]/section/div/div/div/div/form/div[7]/button'
    subscribe_btn = element_wait_finder(subscribe_btn_xpath)
    subscribe_btn.click()
    
    goto_leads_btn_xpath = '//*[@id="froot-nav"]/nav/div[1]/a'
    goto_leads_btn = element_wait_finder(goto_leads_btn_xpath)
    goto_leads_btn.click()
    
    goto_prospect_btn_xpath = '//*[@id="main-content"]/div[1]/nav/div[1]/div[1]/a[5]'
    goto_prospect_btn = element_wait_finder(goto_prospect_btn_xpath)
    goto_prospect_btn.click()
    
    try:
        activate_prospect_xpath = '//*[@id="main-content"]/main/div[1]/div[2]/div/div[3]/div/button'
        activate_prospect_btn = element_wait_finder(activate_prospect_xpath)
        activate_prospect_btn.click()
    except Exception as e:
        activate_prospect_xpath = '//*[@id="main-content"]/main/div[1]/div[3]/div/div[3]/div/button'
        activate_prospect_btn = element_wait_finder(activate_prospect_xpath)
        activate_prospect_btn.click()

    
    confirm_activate_prospect_xpath = '/html/body/div[14]/div[2]/footer/div[2]/button[2]'
    confirm_activate_prospect_btn = element_wait_finder(confirm_activate_prospect_xpath)
    confirm_activate_prospect_btn.click()

    try:
        start_prospecting_xpath = '//*[@id="main-content"]/main/div[1]/div[2]/div/div/div[2]/button'
        start_prospecting_btn = element_wait_finder(start_prospecting_xpath)
        start_prospecting_btn.click()
    except:
        start_prospecting_xpath = '//*[@id="main-content"]/main/div[1]/div[3]/div/div/div[2]/button'
        start_prospecting_btn = element_wait_finder(start_prospecting_xpath)
        start_prospecting_btn.click()
    
    # define prospecting variables
    lead_role_keyword_input_xpath = '/html/body/div[16]/div[2]/div/div/div/div/div[1]/div[2]/div[3]/div/div/input'
    lead_role_keyword_input = element_wait_finder(lead_role_keyword_input_xpath)
    role_keywords = ["infrastructure", "end-user", "desktop"]
    for role_keyword in role_keywords:
        lead_role_keyword_input.send_keys(role_keyword, Keys.ENTER)
    
    # extend variable set
    add_another_variable_btn_xpath = '/html/body/div[16]/div[2]/div/div/div/div/div[1]/div[3]/a'
    add_another_variable_btn = element_wait_finder(add_another_variable_btn_xpath)
    add_another_variable_btn.click()
    
    responsability_dropdown_xpath = '/html/body/div[16]/div[2]/div/div/div/div/div[1]/div[3]/div[2]/div/span'
    responsability_dropdown_input = element_wait_finder(responsability_dropdown_xpath)
    responsabilities = ["Middle-Management", "Top-Tier Leadership", "Executive Level"]
    for responsability in responsabilities:
        responsability_dropdown_input.send_keys(responsability, Keys.ENTER)
        time.sleep(100)
    
    add_another_variable_btn.click()
    
    change_country_selector_xpath = '/html/body/div[17]/div[2]/div/div/div/div/div[1]/div[4]/div[1]/div/span'
    change_country_selector_btn = element_wait_finder(change_country_selector_xpath)
    change_country_selector_btn.click()
    
    select_country_xpath = '//*[@id="downshift-22-item-2"]/span'
    select_country_btn = element_wait_finder(select_country_xpath)
    select_country_btn.click()
    
    enter_countries_input_xpath = '/html/body/div[17]/div[2]/div/div/div/div/div[1]/div[4]/div[2]/div/span'
    enter_countries_input = element_wait_finder(enter_countries_input_xpath)
    countries = ["United States", "Canada"]
    for country in countries:
        enter_countries_input.send_keys(country, Keys.ENTER)
        enter_countries_input.clear()
        
    
    
    

    time.sleep(30)

    driver.quit()


if __name__ == "__main__":
    main()