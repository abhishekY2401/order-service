import requests

PRODUCT_MICROSERVICE_URL = "http://127.0.0.1:7000/graphql"


def fetch_product_prices(product_ids, token):
    query = """
        query getProductByIds($ids: [ID!]!) {
            productByIds(ids: $ids) {
                id
                price
            }
        }
    """

    variables = {"ids": product_ids}

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(
        f"{PRODUCT_MICROSERVICE_URL}",
        json={"query": query, "variables": variables},
        headers=headers
    )

    if response.status_code != 200:
        raise Exception(f"Error fetching product prices: {response.text}")

    data = response.json().get('data', {}).get('productByIds', [])

    return {product["id"]: product["price"] for product in data}
