import json
import random
import time
import copy
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

datetime_format = "%Y-%m-%dT%H:%M:%S"
base_url = "https://huggingface.co"
base_org_url = "https://huggingface.co/organizations?p={page_idx}"
output_dir = Path("data/")
if not output_dir.is_dir():
    output_dir.mkdir(parents=True)


def get_companies_with_models(idx):
    tmp_url = base_org_url.format(page_idx=idx)
    page = requests.get(tmp_url)
    assert page.status_code == 200
    soup = BeautifulSoup(page.text, "html.parser")

    orgs = soup.find_all(
        "article",
        class_="overview-card-wrapper group sm:flex items-center overflow-hidden",
    )
    companies = []
    for org in orgs:
        details = org.find("div", class_="text-sm text-gray-400 truncate")
        details_str = " ".join(details.get_text().split())
        try:
            model_count = int(details_str.split("•")[1].split(" ")[1])
        except Exception as e:
            model_count = None
        if "company" in details_str and model_count:
            company_name = org.find(
                "h4", class_="font-semibold flex items-center md:text-lg"
            ).get_text()
            company_url = base_url + org.find("a", href=True)["href"]
            companies.append({"company_name": company_name, "company_url": company_url})

    return companies


def get_team_member_metadata(url):
    team_member_page = requests.get(url)
    assert team_member_page.status_code == 200
    team_member_parsed = BeautifulSoup(team_member_page.text, "html.parser")
    # scrape info about their profile
    personal_info = team_member_parsed.find(
        "section",
        class_="pt-8 border-gray-100 md:col-span-5 lg:col-span-4 xl:col-span-3 md:border-r border-gray-100 md:bg-gradient-to-l md:from-gray-50-to-white md:pr-6",
    )
    name = (
        personal_info.find("h1", class_="text-2xl font-bold flex items-center")
        .get_text()
        .strip()
    )
    team_member_metadata = {
        "username": name,
        "user_url": url,
        "homepage": None,
        "github": None,
        "twitter": None,
        "interests": None,
    }
    links = personal_info.find_all("a", class_="hover:underline truncate", href=True)
    for link in links:
        if "twitter" in link["href"]:
            team_member_metadata["twitter"] = link["href"]
        elif "github" in link["href"]:
            team_member_metadata["github"] = link["href"]
        else:
            team_member_metadata["homepage"] = link["href"]

    interests = personal_info.find("div", class_="mb-6 truncate")
    if interests and interests.get_text().strip() != "None yet":
        team_member_metadata["interests"] = interests.get_text().strip()

    # get some info about their work
    stats = team_member_parsed.find_all("span", class_="ml-3 font-normal text-gray-400")
    categories = ["space_count", "model_count", "dataset_count"]
    if len(stats) == 2:
        stats.insert(0, None)
    for stat, cat in zip(stats, categories):
        try:
            count = int(stat.get_text().strip())
        except Exception as e:
            count = 0

        team_member_metadata[cat] = count

    # retrieve latest work commitment
    if team_member_parsed.find_all("time"):
        time_updates = [
            datetime.strptime(time_div["datetime"], datetime_format)
            for time_div in team_member_parsed.find_all("time")
        ]
        time_updates.sort(reverse=True)
        team_member_metadata["last_updated"] = time_updates[0].strftime(datetime_format)
    else:
        team_member_metadata["last_updated"] = None

    return team_member_metadata


def add_company_metadata(company):
    """Flag company with visible info."""
    company_page = requests.get(company["company_url"])
    assert company_page.status_code == 200
    soup = BeautifulSoup(company_page.text, "html.parser")

    # add company profile info
    company.update(
        {
            "company_homepage": None,
            "company_github": None,
            "company_twitter": None,
            "company_domain": None,
        }
    )
    company_profile = soup.find(
        "div",
        class_="sm:flex items-baseline space-y-0.5 sm:space-y-0 sm:space-x-3 text-smd mb-2 sm:mb-0",
    )
    if company_profile:
        links = company_profile.find_all(
            "a", class_="text-gray-600 hover:underline", href=True
        )
        for link in links:
            if "github" in link["href"]:
                company["company_github"] = link["href"]
            elif "twitter" in link["href"]:
                company["company_twitter"] = link["href"]
            else:
                company["company_homepage"] = link["href"]
                company["company_domain"] = urlparse(link["href"]).netloc
    else:
        print("No company profile found for {}".format(company["company_name"]))

    team_members = []
    team_member_divs = soup.find_all(
        "a",
        class_="flex-none block -mr-2 border-2 border-white dark:border-gray-950 rounded-full w-11 h-11 overflow-hidden bg-gray-100",
        href=True,
    )
    for team_member_div in team_member_divs:
        team_member_url = base_url + team_member_div["href"]
        team_member_metadata = get_team_member_metadata(team_member_url)
        team_members.append(team_member_metadata)

    company["team"] = team_members


def update_team_members_df(company, df_dict):
    for team_member in company["team"]:
        row = {**team_member, **company}
        del row["team"]
        row["reached_out"] = False
        row["talked"] = False
        df_dict.append(row)


def fetch_active_companies_with_models():
    """Fetch all companies with models, and that have at least one employee
    with Github/Twitter/Website info."""
    output_company_file = output_dir.joinpath("active_companies_with_models.json")
    output_user_file = output_dir.joinpath("active_team_members.csv")
    page_count = 88
    df_dict = []
    output_companies = []
    for i in tqdm(range(page_count)):
        companies = get_companies_with_models(i)
        for company in companies:
            add_company_metadata(company)
            if len(company["team"]) > 0:
                company["member_count"] = len(company["team"])
                output_companies.append(company)
                update_team_members_df(company, df_dict)

                time.sleep(2 * random.random())
        time.sleep(5 * random.random() + 3)

        # save at each step
        df = pd.DataFrame.from_dict(df_dict)
        df.to_csv(output_user_file)
        with open(output_company_file, "w") as f:
            json.dump(output_companies, f)
    print("Done scraping data for {} companies".format(len(output_companies)))


def fetch_companies():
    output_file = "huggingface_customers.json"
    page_count = 53
    companies = []
    for i in tqdm(range(page_count)):
        tmp_url = base_org_url.format(page_idx=i)
        page = requests.get(tmp_url)
        assert page.status_code == 200
        soup = BeautifulSoup(page.text, "html.parser")

        # retrieve all companies from the organization pages
        company_titles = soup.find_all(
            "h4", class_="font-semibold flex items-center md:text-lg"
        )
        for company_title in company_titles:
            try:
                companies.append(str(company_title).split('title="')[1].split('">')[0])
            except Exception as e:
                print(e, str(company_title))

        # save updated companies
        with open(output_file, "w") as f:
            json.dump(companies, f)

        # wait for a small, random amount of time
        time.sleep(5 * random.random() + 3)
    print(
        f"Done collecting names of {len(companies)} organizations customers of Hugging face."
    )


def fetch_companies_no_models():
    full_output_file = "huggingface_customers_full.json"
    output_file = "huggingface_companies_wo_models.json"
    page_count = 53
    full_companies = {}
    companies_wo_models = []
    for i in tqdm(range(page_count)):
        tmp_url = base_org_url.format(page_idx=i)
        page = requests.get(tmp_url)
        assert page.status_code == 200
        soup = BeautifulSoup(page.text, "html.parser")
        organizations = soup.find_all("div", class_="overflow-hidden leading-tight")

        for organization in organizations:
            # find the org name
            org_name = organization.find(
                "h4", class_="font-semibold flex items-center md:text-lg"
            )
            # extract the organization name
            try:
                name = str(org_name).split('title="')[1].split('">')[0]
                full_companies[name] = {}
            except Exception as e:
                print(e, str(org_name))
                continue

            org_metadata = organization.find(
                "div", class_="text-sm text-gray-400 truncate"
            )
            if org_metadata:
                org_type = org_metadata.find("span", class_="capitalize")
                if org_type:
                    full_companies[name]["type"] = org_type.get_text()

        # save updated companies
        with open(full_output_file, "w") as f:
            json.dump(full_companies, f)
        with open(output_file, "w") as f:
            json.dump(companies_wo_models, f)

        # wait for a small, random amount of time
        time.sleep(5 * random.random() + 3)
    print(
        f"Done collecting names of {len(companies_wo_models)} companies without models."
    )


if __name__ == "__main__":
    fetch_active_companies_with_models()
