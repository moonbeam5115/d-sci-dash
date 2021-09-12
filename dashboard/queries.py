#!/usr/bin/env python

from google.cloud import bigquery
from google.oauth2 import service_account
import yaml


key_path = ''
with open("config.yaml", "r") as f:
    try:
        cfg = yaml.safe_load(f)
        key_path = cfg['service_key_path']
    except yaml.YAMLError as exc:
        print(exc)


def query_research_location():
    credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

    query_job = client.query(
        """
        SELECT COUNT(research_org_country_names) AS Number_of_Publications, country
        FROM
            `covid-19-dimensions-ai.data.publications`,
            UNNEST(research_org_country_names) as country
        GROUP BY country
        ORDER BY Number_of_Publications DESC
        LIMIT 6
        """
    )

    results = query_job.result()  # Waits for job to complete.
    location_data = []
    for row in results:
        print("Number of Publications: {}, Country: {} ".format(row.Number_of_Publications, row.country))
        location_data.append((row.Number_of_Publications, row.country))
    output = {'top_locations': location_data}
    return output

def query_funding_organizations():
    credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

    query_job = client.query(
        """
        SELECT COUNT(funder_orgs) as Number_of_Publications, name 
        FROM `covid-19-dimensions-ai.data.publications` p,
            UNNEST(funder_orgs) as funder_id
        JOIN `covid-19-dimensions-ai.data.grid` g ON g.id=funder_id  
        GROUP BY name
        ORDER BY Number_of_Publications DESC
        LIMIT 10
        """
    )

    results = query_job.result()  # Waits for job to complete.
    fund_orgs_data = []
    for row in results:
        print("Number of Publications: {}, Organization: {} ".format(row.Number_of_Publications, row.name))
        fund_orgs_data.append((row.Number_of_Publications, row.name))
    output = {'top_fund_orgs': fund_orgs_data}

    return output

def query_research_organizations():
    credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

    query_job = client.query(
        """
        SELECT COUNT(research_orgs) as Number_of_Publications, name
        FROM `covid-19-dimensions-ai.data.publications` p,
            UNNEST(research_orgs) as research_id
        JOIN `covid-19-dimensions-ai.data.grid` g ON g.id=research_id
        WHERE name IS NOT NULL
        GROUP BY name
        ORDER BY Number_of_Publications DESC
        LIMIT 10
        """
    )

    results = query_job.result()  # Waits for job to complete.
    research_orgs_data = []
    for row in results:
        print("Number of Publications: {}, Organization: {} ".format(row.Number_of_Publications, row.name))
        research_orgs_data.append((row.Number_of_Publications, row.name))

    output = {'top_research_orgs': research_orgs_data}

    return output

def query_researchers():
    credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

    query_job = client.query(
        """
        SELECT COUNT(researcher_id) as Number_of_Publications, CONCAT(a.first_name, ' ', a.last_name) as name
        FROM `covid-19-dimensions-ai.data.publications` p,
            UNNEST(researcher_ids) as researcher_id,
            UNNEST(authors) as a
        WHERE a.first_name IS NOT NULL
        AND a.last_name IS NOT NULL
        GROUP BY name
        ORDER BY Number_of_Publications DESC
        LIMIT 10
        """
    )

    results = query_job.result()  # Waits for job to complete.
    researchers_data = []
    for row in results:
        print("Number of Publications: {}, Researcher: {} ".format(row.Number_of_Publications, row.name))
        researchers_data.append((row.Number_of_Publications, row.name))

    output = {'top_researchers': researchers_data}
    return output

if __name__ == "__main__":
    query_research_location()
    query_funding_organizations()
    query_research_organizations()
    query_researchers()