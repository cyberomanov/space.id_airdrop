import json

import requests


def get_addresses(path: str = 'address.txt') -> list:
    with open(path) as file:
        lines = file.readlines()
    return [line.rstrip() for line in lines]


def get_token(address: str) -> float:
    data = {
        "operationName": "AirdropDetail",
        "variables": {"addr": address.lower()},
        "query": "query AirdropDetail($addr: String!) {\n  AirDropDetail(addr: $addr) {\n    exists\n    "
                 "bnbThreeDigit\n    bnbFourDigit\n    arbThreeDigit\n    arbFourDigit\n    holdingTime\n    "
                 "daysToExpiry\n    setPrimaryName\n    voyageCount\n    voyage1\n    voyage2\n    voyage3\n    "
                 "bothBnbArb\n    recordsRole\n    tokenAmount\n    galxeOat\n    __typename\n  }\n}"
    }
    response = requests.post(url=f"https://graphigo.prd.space.id/query", json=data)
    result = json.loads(response.content)['data']['AirDropDetail']
    if result['exists']:
        return int(result['tokenAmount']) / 1_000_000_000_000_000_000
    else:
        return 0.0


def main():
    total_amount = 0.0
    for address in get_addresses():
        amount = get_token(address=address)
        total_amount += amount
        print(f"{address}: {amount:.2f}.")
    print(f"total: {total_amount:.2f}.")


if __name__ == '__main__':
    main()
