import csv
import json
import re

def clean_price(price_str):
    if not price_str:
        return "По запросу"
    # Extract first price if multiple are present
    price = price_str.split(',')[0].strip()
    # Extract numbers
    numbers = re.findall(r'\d+', price)
    if numbers:
        return numbers[0]
    return "По запросу"

def transform_csv_to_js():
    courses = []
    
    with open('ksu.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            if not row['название']:  # Skip empty rows
                continue
                
            course = {
                'title': row['название'].strip(),
                'link': row['ссылка'].strip(),
                'price': clean_price(row['цена с ведением , без ведения']),
                'lessons': row['количество уроков'],
                'duration': row['длительность'],
                'access': row['доступ'],
                'comment': row['комментарий']
            }
            courses.append(course)
    
    # Read the existing HTML file
    with open('index.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Replace the coursesData placeholder with actual data
    js_data = f"const coursesData = {json.dumps(courses, ensure_ascii=False, indent=4)};"
    new_html = re.sub(
        r'const coursesData = \[([\s\S]*?)\];',
        js_data,
        html_content
    )
    
    # Write the updated HTML file
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(new_html)

if __name__ == '__main__':
    transform_csv_to_js() 