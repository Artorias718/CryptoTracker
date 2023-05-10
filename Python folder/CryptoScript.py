import requests
from datetime import datetime, timezone
import json
from notion_client import Client


NOTION_TOKEN = "secret_gjCp3sHvEFej1BCt7M75uI720jEXsooWt88KgzgoFeT"
DATABASE_ID = "85bae205522d43b880bb8f2761c7dd81"
cm_secret = "10ea5ef2-9112-493f-bca4-a62cf9751b73"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

headers_cm = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': cm_secret,
}

url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
url_cm = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id='

crypto_list = [1, 1027, 3635, 1839, 6636, 4172, 5426, 5805,
               1556, 2694, 5804, 4705, 6210, 4195, 1975, 3794, 20947]
demo = [1, 1027]


crypto_str = ','.join(map(str, demo))
full_url = url_cm + crypto_str


def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

    res = requests.post(create_url, headers=headers, json=payload)
    print(res.status_code)
    return res

    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"properties": data}

    res = requests.patch(url, json=payload, headers=headers)
    return res


def update_page(page_id: str, data: dict):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"properties": data}

    res = requests.patch(url, json=payload, headers=headers)
    return res


def get_pages(num_pages=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}

    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    results = data["results"]
    return results


def stamp_pages(pages):

    for page in pages[1:]:
        page_id = page["id"]

        props = page["properties"]
        url = props["URL"]["title"][0]["text"]["content"]
        title = props["Title22"]["rich_text"][0]["text"]["content"]
        published = props["Published"]["date"]["start"]
        published = datetime.fromisoformat(published)
        print(url, title, published)


def post_pages(crypto_list):
    res = requests.get(full_url, headers=headers_cm)
    data2 = json.loads(res.text)

    for id in crypto_list:

        data_post = {
            "Code": {"number": id},
            "Crypto": {"title": [{"text": {"content": data2["data"][str(id)]["name"]}}]},
            "Price": {"number": data2["data"][str(id)]["quote"]["USD"]["price"]},
            "Symbol": {"rich_text": [{"text": {"content": data2["data"][str(id)]["symbol"]}}]},
            "Icon": {"files": [{
                "name": "https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png",
                "type": "external",
                "external": {"url": f"https://s2.coinmarketcap.com/static/img/coins/64x64/{str(id)}.png"}}]}

        }
        create_page(data_post)


def get_databse_formatted():

    client = Client(auth="secret_gjCp3sHvEFej1BCt7M75uI720jEXsooWt88KgzgoFeT")
    results = client.databases.query(
        **{
            "database_id": DATABASE_ID,
        }
    ).get("results")

    print(results)


def update_pages():
    pages = get_pages()
    res = requests.get(full_url, headers=headers_cm)
    data2 = json.loads(res.text)
    for page in pages:
        crypto_id = page["properties"]["Code"]["number"]
        # print("3333333333333333333333333333333" + str(page))

        data_post = {
            "Price": {"number": data2["data"][str(crypto_id)]["quote"]["USD"]["price"]}
        }

        update_page(page["id"], data_post)


# create_page(data)
# stamp_pages(pages=get_pages())


# Nome         data2["data"][str(id)]["name"]
# Price        data["data"][str(id)]["quote"]["USD"]["price"]
# Symbol       data2["data"][str(id)]["symbol"]


# get_databse_formatted()
# post_pages(demo)
update_pages()
