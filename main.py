import csv
from bs4 import BeautifulSoup

# Zmień na swoją nazwę
file_path = "b.html"

with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

rows = soup.select('tr.attribute')  # Każdy wiersz specyfikacji ma klasę "attribute"
data = {}
for row in rows:
    label_element = row.select_one('th .attribute-name')
    value_element = row.select_one('td .attribute-value')
    
    if label_element and value_element:
        label = label_element.get_text(strip=True)  # Nazwa parametru (np. Model procesora)
        value = value_element.get_text(strip=True)  # Wartość parametru (np. Qualcomm Snapdragon 860)
        
        data[label] = value

with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(data.keys())  # Nagłówki kolumn (np. Model Procesora, Pamięć RAM itp.)
    writer.writerow(data.values())  # Wartości (np. Qualcomm Snapdragon 860, 6 GB itp.)

print("Dane zostały zapisane do pliku output.csv.")

