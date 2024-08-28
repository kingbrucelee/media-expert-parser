import csv
import os
import glob
from bs4 import BeautifulSoup
from collections import Counter

# Przetwarzanie pojedynczego pliku HTML
def process_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    #znacznik content to link oryginalny
    for i in soup.select('meta'):
        if i.get("name") == "og:url":
            link=i.get("content")
    # TODO lepszy sposób pobierania niż selektor CSS
    price = soup.select("div.is-big > span:nth-child(1)")[0].text.replace('\u202f', '')
    
    rows = soup.select('tr.attribute')  # Każdy wiersz specyfikacji ma klasę "attribute"
    data = {}
    # Manualnie dodaję utworzone dodatkowe kolumny
    data['link'] = link
    data['cena'] = price
    for row in rows:
        label_element = row.select_one('th .attribute-name')
        value_element = row.select_one('td .attribute-value')
        
        if label_element and value_element:
            label = label_element.get_text(strip=True)  # Nazwa parametru
            value = value_element.get_text(strip=True)  # Wartość parametru

            data[label] = value

    return data

# Przetworzenie wszystkich plików HTML w danym folderze
def process_all_html_files_in_folder(folder_path):
    all_data = []
    for file_path in glob.glob(os.path.join(folder_path, '*.html')):
        file_data = process_html_file(file_path)
        all_data.append(file_data)

    return all_data

def save_to_csv(all_data, output_file):
    # Nadzbiór nazw wszystkich parametrów
    all_keys = set()
    # Liczenie częstotliwości występowania każdego klucza w danych by ustalić logiczną kolejność
    key_counter = Counter()
    # Priorytetowe klucze w ustalonej kolejności i dodatkowo w osobnym pliku
    key_priority = ['Model smartfona:', 'Seria smartfona:', 'cena', 'link', 'Pamięć wbudowana [GB]:', 'Pamięć RAM:', 'Model Procesora:', 'Pojemność akumulatora [mAh]:', 'Aparat:', 'Wyjście słuchawkowe:', 'Ładowanie bezprzewodowe:', 'Odświeżanie ekranu [Hz]:', 'Wyświetlacz:']
    
    for data in all_data:
        key_counter.update(data.keys())
    non_priority_keys = [key for key, _ in key_counter.most_common() if key not in key_priority]
    all_keys = key_priority + non_priority_keys
    
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(all_keys) 
        for data in all_data:
            row = [data.get(key, '') for key in all_keys]  # Jeśli brakuje klucza, wstaw pustą wartość
            writer.writerow(row)
    
    with open('priority.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(key_priority) 
        for data in all_data:
            row = [data.get(key, '') for key in key_priority]  # Jeśli brakuje klucza, wstaw pustą wartość
            writer.writerow(row)


folder_path = 'phones'  # IMPORTANT: change to your folder_path
output_file = 'output.csv' 

all_data = process_all_html_files_in_folder(folder_path)
save_to_csv(all_data, output_file)

print(f"Dane zostały zapisane do pliku {output_file} oraz priority.csv")
