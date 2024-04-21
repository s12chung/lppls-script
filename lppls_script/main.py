import requests
from urllib.parse import urlencode

def download_data(ticker: str, api_key: str, data_file: str) -> None:
    query = {
        'format': 'CSV',
        'delimiter': ',',
        'order': 'ASC',
        'interval': '1day',
        'outputsize': '1000',
        'symbol': ticker,
        'apikey': api_key
    }
    full_url = f"https://api.twelvedata.com/time_series?{urlencode(query)}"

    response = requests.get(full_url)
    response.raise_for_status()  # Raise an error for bad responses

    with open(data_file, 'wb') as f:
        f.write(response.content)
    print(f"Data for {ticker} downloaded successfully.")

import nbformat
from nbconvert import HTMLExporter

def export_notebook(notebook, output_path: str) -> None:
    nb = nbformat.read(notebook, as_version=4)

    html_exporter = HTMLExporter()
    html_exporter.template_name = 'classic'

    (body, resources) = html_exporter.from_notebook_node(nb)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(body)

from bs4 import BeautifulSoup
import base64
from PIL import Image
from io import BytesIO

def extract_images_from_html(html_file_path: str) -> None:
    with open(html_file_path, 'r') as file:
        html_content = file.read()
    
    img_tags = BeautifulSoup(html_content, 'html.parser').find_all('img')
    
    images = []
    
    for img in img_tags:
        src = img.get('src')
        
        if src.startswith('data:image/png;base64,'):
            image_data = base64.b64decode(src.split('data:image/png;base64,')[1])
            images.append(Image.open(BytesIO(image_data)))

    total_width = max(image.width for image in images)
    total_height = sum(image.height for image in images)
    merged_image = Image.new('RGBA', (total_width, total_height), 'white')

    y_offset = 0
    for image in images:
        x_offset = (total_width - image.width) // 2
        merged_image.paste(image, (x_offset, y_offset), image)
        y_offset += image.height

    merged_image.save(f'{os.path.dirname(html_file_path)}/{no_ext_filename(html_file_path)}.png')

def no_ext_filename(file_path: str) -> str:
    return os.path.splitext(os.path.basename(file_path))[0]

import sys
import os
from importlib import resources

def main():
    if len(sys.argv) != 2:
        print("Usage: lppls-script <ticker>")
        return
    
    symbol = sys.argv[1]
    safe_ticker = symbol.replace('/', '|')

    download_data(symbol, os.environ['TWELVE_API_KEY'], f"./output/{safe_ticker}.csv")

    html_file = f"./output/{safe_ticker}.html"
    os.environ['SAFE_TICKER'] = safe_ticker
    with resources.open_binary(__name__, 'run.ipynb') as file:
        export_notebook(file, html_file)
    extract_images_from_html(html_file)

    os.system(f"open \"./output/{safe_ticker}.png\"")

if __name__ == '__main__':
    main()