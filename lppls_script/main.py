import requests
from urllib.parse import urlencode

def download_data(ticker: str, api_key: str, data_path: str, opts={}) -> None:
    query = {
        'format': 'CSV',
        'delimiter': ',',
        'order': 'ASC',
        'interval': '1day',
        'outputsize': opts['outputsize'],
        'symbol': ticker,
        'apikey': api_key
    }
    full_url = f"https://api.twelvedata.com/time_series?{urlencode(query)}"

    response = requests.get(full_url)
    response.raise_for_status()

    with open(data_path, 'wb') as f:
        f.write(response.content)

import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor

def export_notebook(notebook, output_path: str) -> None:
    nb = nbformat.read(notebook, as_version=4)

    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb)

    html_exporter = HTMLExporter()
    html_exporter.template_name = 'classic'
    (body, resources) = html_exporter.from_notebook_node(nb)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(body)

from bs4 import BeautifulSoup
import base64
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

TEXT_HEIGHT = 50
TOP_IMAGE_ADJUST = 120

def image_from_html(ticker: str, html_file_path: str, image_path: str) -> None:
    with open(html_file_path, 'r') as file:
        html_content = file.read()
    img_tags = BeautifulSoup(html_content, 'html.parser').find_all('img')
    
    images = []
    for img in img_tags:
        src = img.get('src')
        
        if src.startswith('data:image/png;base64,'):
            image_data = base64.b64decode(src.split('data:image/png;base64,')[1])
            images.append(Image.open(BytesIO(image_data)))
    
    if len(images) > 1:
        desired_width = images[1].width - TOP_IMAGE_ADJUST
        scale_ratio =  desired_width / images[0].width
        images[0] = images[0].resize((desired_width, int(images[0].height * scale_ratio)), Image.Resampling.LANCZOS)

    total_width = max(image.width for image in images)
    total_height = sum(image.height for image in images) + TEXT_HEIGHT
    merged_image = Image.new('RGBA', (total_width, total_height), 'white')

    font = ImageFont.load_default(30)
    ImageDraw.Draw(merged_image).text(((total_width - font.getlength(ticker)) / 2, 10), ticker, fill="black", font=font)

    y_offset = TEXT_HEIGHT
    for image in images:
        x_offset = (total_width - image.width) // 2
        merged_image.paste(image, (x_offset, y_offset), image)
        y_offset += image.height

    merged_image.save(image_path)

def no_ext_filename(file_path: str) -> str:
    return os.path.splitext(os.path.basename(file_path))[0]

import argparse
from importlib import resources
import os

def main():
    parser = argparse.ArgumentParser(description="Log Periodic Power Law Singularity (LPPLS) Model Script")

    parser.add_argument('ticker', type=str, help='Ticker to process data with')
    parser.add_argument('--data-size', type=int, default= 730, help='Data size (default: 730, ~2 years for seasonality and efficency)')

    args = parser.parse_args()
    run(args.ticker, {
        'outputsize': args.data_size
    })

def run(ticker: str, data_opts={}):
    safe_ticker = ticker.replace('/', '|')

    extras_path ="./lppls-extras"
    os.makedirs(extras_path, exist_ok=True)
    data_path = f"{extras_path}/{safe_ticker}.csv"
    html_path = f"{extras_path}/{safe_ticker}.html"
    image_path = f"./{safe_ticker}.png"

    download_data(ticker, os.environ['TWELVE_API_KEY'], data_path, data_opts)
    os.environ['SAFE_TICKER'] = safe_ticker
    with resources.open_binary(__name__, 'run.ipynb') as file:
        export_notebook(file, html_path)
    image_from_html(ticker, html_path, image_path)

    os.system(f"open \"{image_path}\"")

if __name__ == '__main__':
    main()