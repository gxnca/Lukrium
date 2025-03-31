import requests
import json

def correct_price(price):
    string_price = str(price)
    if len(string_price) >= 3:
        formatted_price = string_price[:-2] + '.' + string_price[-2:]
    else:
        formatted_price = "0," + string_price.zfill(2)

    return formatted_price

def get_data_from_api():
    product_list = []

    for index in range(1, 100):
        url = f"https://api.kabaz.pt/search/1/indexes/*/queries?x-algolia-agent=Algolia for JavaScript (4.22.1); Browser (lite); instantsearch.js (4.64.1); react (18.2.0); react-instantsearch (7.5.3); react-instantsearch-core (7.5.3); next.js (14.1.0); JS Helper (3.16.2)&x-algolia-api-key=af829a38ce6dba053305865877cedd1d&x-algolia-application-id=8E3T7T6L1N&ssr=false"
        headers = {
            "User-Agent": "Chromium v134, Not:A-Brand v24, Microsoft Edge v134",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6bnVsbCwic3ViIjoiZWsxNDB3d2ZqeXJ4Mm1rNCIsImlhdCI6MTc0MzI2Njc5MSwiZXhwIjoxNzQ1ODU4NzkxfQ.tIRm6PTptI0LBlSiVwkP2sB33JgRahye0UjuQer8j3U",
            "Content-Type": "application/json"
        }
        body = {
            "requests": [
                {
                    "indexName": "Products",
                    "params": f"clickAnalytics=true&facets=%5B%22brand.slug%22%2C%22hierarchicalCategories.lvl0%22%2C%22product.hasPromotion%22%2C%22product.id%22%2C%22storeGroup%22%2C%22tags%22%5D&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=34&maxValuesPerFacet=24&page={index}&query=&tagFilters=&userToken=anonymous-e0cf968c-467c-443d-9280-a8b98388f043"
                }
            ]
        }

        response = requests.post(url, headers=headers, json=body)

        if response.status_code == 200:
            data = response.json()

            if "results" in data:
                products = data["results"][0]["hits"]

                for product in products:
                    name = product.get("product", {}).get("name", "No Name")
                    price = product.get("product", {}).get("price", "No Price")
                    brand = product.get("brand", {}).get("slug", "No Brand")

                    product_list.append({"name": name, "price": correct_price(price), "brand": brand})
        else:
            print(f"Failed to fetch data for index {index}. Status code: {response.status_code}")

    with open("products.json", "w", encoding="utf-8") as json_file:
        json.dump(product_list, json_file, indent=4, ensure_ascii=False)

    print(f"Fetched data for {len(product_list)} products.")
