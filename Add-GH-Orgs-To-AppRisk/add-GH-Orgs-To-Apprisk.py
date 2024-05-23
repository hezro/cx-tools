from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import json
import requests
import csv
import numpy as np
import os


# Call the endpoint to create the GitHub profile with all the Organizations
def add_GH_Integration(driver, group_id, profile_name, gh_token, gh_api_url, gh_org_list):
    url = f'https://app.snyk.io/apprisk/groups/{group_id}/harbor/api/v1/apps/github/profiles'

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://app.snyk.io',
        'priority': 'u=1, i',
        'referer': f'https://app.snyk.io/apprisk/groups/{group_id}/integrations',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }

    cookies = driver.get_cookies()
    snyk_cookies = {}
    for cookie in cookies:
        snyk_cookies[cookie['name']] = cookie['value']

    if is_csv_file(gh_org_list):
        org_list = csv_array(gh_org_list)
    else:
        with open(gh_org_list) as input_file:
            org_list = set(line.strip().lower() for line in input_file)

    data = {
        'name': profile_name,
        'config': {
            'apiUrl': gh_api_url,
            'pullPersonalRepos': False,
            'backstageCatalogToggle': False,
            'organizations': org_list.tolist(),
            'token': gh_token
        }
    }

    try:
        response = requests.post(url, headers=headers,
                                 cookies=snyk_cookies, data=json.dumps(data))
        response.raise_for_status()
        print(f'SUCCESS: Added {profile_name} profile AppRisk integrations!')

    except requests.exceptions.HTTPError as err:
        print(f'HTTP ERROR: {err}')
        raise
    except Exception as e:
        print(f'ERROR: {e}')
        raise

    driver.quit()
    print('Done!')


def is_csv_file(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline()
        return ',' in first_line


def csv_array(repo_file_path):
    with open(repo_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        csv_list = [item.lower() for item in next(csv_reader)]
        return np.array(csv_list)


def main():

    driverPath = ChromeDriverManager().install()
    service = Service(executable_path=driverPath)
    driver = webdriver.Chrome(service=service)

    # Load config file
    try:
        with open('config.json') as f:
            config = json.load(f)
    except IOError:
        print('Please ensure that the config.json file exists')
        return

    # Variables
    group_id = config["group_id"]
    profile_name = config["profile_name"]
    gh_token = config["gh_token"]
    gh_api_url = config["gh_api_url"]
    gh_org_list = config["gh_org_list"]
    loginURL = 'https://app.snyk.io'

    if not os.path.exists(gh_org_list):
        print(f'Please ensure that the {gh_org_list} file exists')
        return

    # Open Chrome to the Snyk login page
    print('Loading Snyk login page....')
    driver.get(loginURL)

    if 'app.snyk.io/login' in driver.current_url:

        print('Please Login to Snyk')
        # Wait until login is successful
        WebDriverWait(driver, timeout=120).until(
            EC.url_contains('app.snyk.io/org/'))

        print(f'Press ENTER to add {profile_name} to AppRisk: ')
        driver.minimize_window()
        # Wait for the user to press ENTER to add the GH profile to AppRisk
        input('>_ ')
        add_GH_Integration(driver, group_id, profile_name,
                           gh_token, gh_api_url, gh_org_list)


if __name__ == "__main__":
    main()
