import requests
import json
import math

def get_data():
    headers = {
        'authority': 'api.crexi.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ka;q=0.6',
        'client-timezone-offset': '4',
        'content-type': 'application/json',
        'mixpanel-distinct-id': '$device:18dbb749267b7a-0f8df5c52fe631-26001851-100200-18dbb749267b7a',
        'origin': 'https://www.crexi.com',
        'referer': 'https://www.crexi.com/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    json_data = {
        'count': 60,
        'mlScenario': 'Recombee-Recommendations',
        'offset': 0,
        'userId': '$device:18dbb749267b7a-0f8df5c52fe631-26001851-100200-18dbb749267b7a',
        'sortDirection': 'Descending',
        'sortOrder': 'rank',
        'includeUnpriced': True,
    }

    s = requests.Session()
    response = s.post('https://api.crexi.com/assets/search', headers=headers, json=json_data).json()

    totalCount = response.get("totalCount")

    if totalCount is None:
        return "[!] No Items!"
    
    total_pages = math.ceil(totalCount / 60)
    
    all_elements = []

    with open("result.json", "w", encoding="utf-8") as file_json:
        for i in range(total_pages):
            offset = f'{i * 60}'
            json_data['offset'] = offset

            response = s.post('https://api.crexi.com/assets/search', headers=headers, json=json_data).json()

            block = response.get("data")
            if block is None:
                print("[!] No data found in the API response.")
                break
            
            for el in block:
                name = el.get("name", "None")
                price = el.get("askingPrice", "None")
                broker_name = el.get("brokerName", "None")
                address = el.get("fullAddress", "None")
                id = el.get("id", "None")
                description = el.get("description", "None")

                element_list = {
                    "Name" : name,
                    "Price" : price,
                    "Broker_Name" : broker_name,
                    "Address" : address,
                    "Description" : description,
                    "Id" : id
                }
                all_elements.append(element_list) 

        # with open("result.json", "w") as file_json:
        #     json.dump(all_elements, file_json, indent=4, ensure_ascii=False)

        json.dump(all_elements, file_json, indent=4, ensure_ascii=False)
        file_json.write('\n')  # Write a newline character to separate each JSON object

def main():
    get_data()

if __name__ == "__main__":
    main()