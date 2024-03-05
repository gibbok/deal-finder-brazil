from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

# Get user input on what to search
search_query = input("Search for: ")
formatted_query = "-".join(search_query.lower().strip().split())
url = f"https://lista.mercadolivre.com.br/%22{formatted_query}%22"

# Send an HTTP request to the server
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive",
}
response = requests.get(url, headers=headers)

# Parse the HTML response
soup = BeautifulSoup(response.text, "html.parser")

## Test using a local file
# with open("./test-data/web-page.html", "r", encoding="utf-8") as f:
#     html_content = f.read()
# soup = BeautifulSoup(html_content, "html.parser")
# pretty_html = soup.prettify()


# Extract money as number from text
def convert_money_text_to_number(str):
    digits = re.findall(r"\d+", str)
    numeric_value = "".join(digits)
    result = float(numeric_value) / 100
    return result


# Search main content
results = soup.find_all("div", class_="ui-search-result__wrapper")

items = []

for div in results:
    h2_tags = div.find("h2")
    money_text_array = div.find("span", class_="andes-money-amount").get_text()
    money = convert_money_text_to_number(money_text_array)
    for h2_tag in h2_tags:
        title = h2_tag.get_text().strip()
        print(title, money)
        items.append([title, money])

# Generate a Data Frame, sort and save result to file system
df = pd.DataFrame(items, columns=["name", "price"])
df_sorted = df.sort_values(by="price")
df_sorted.to_csv(f"./output/{formatted_query}.csv", index=False)

print(df_sorted)
print(f"DataFrame saved to {formatted_query}.csv")
