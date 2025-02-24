import requests
from lxml import html

try:
    import config
except ImportError:
    print("Please create a config file.")

def get_page(url):
    response = requests.get(url)
    
    # Parse the HTML
    tree = html.fromstring(response.content)

    # Find the table element
    table = tree.xpath('/html/body/div[3]/div[2]/table')

    if table:
        rows = table[0].xpath('.//tr')
        
        results = []
        for row in rows:
            cells = row.xpath('.//td | .//th')
            cell_text = [cell.text_content().strip() for cell in cells]
            
            if len(cell_text) >= 3:
                results.append({
                    "last_name": cell_text[0],
                    "first_name": cell_text[1],
                    "status": cell_text[2]
                })
            else:
                results.append(cell_text)
        
        return results
    else:
        return "Table not found at the given XPath."

def check_table(table, last_name, first_name):
    for item in table:
        if item["last_name"] == last_name and item["first_name"] == first_name:
            print(item["status"])
        else:
            print("User not found on the table.")

# Main loop of the code
check_table(get_page(config.url), config.last_name, config.first_name)