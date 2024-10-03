import requests

PRODUCT_MICROSERVICE_URL = "http://127.0.0.1:7000/graphql"


def fetch_product_prices(product_ids):
    query = """
        query getProductByIds($ids: [ID!]!) {
            productByIds(ids: $ids) {
                id
                price
            }
        }
    """

    variables = {"ids": product_ids}

    response = requests.post(
        f"{PRODUCT_MICROSERVICE_URL}",
        json={"query": query, "variables": variables}
    )

    data = response.json()['data']['productByIds']

    return {product["id"]: product["price"] for product in data}
