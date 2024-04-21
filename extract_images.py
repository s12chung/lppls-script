from bs4 import BeautifulSoup
import base64
from PIL import Image
from io import BytesIO
import os
import sys

def save_images_from_html_file(html_file_path):
    # Read HTML content from file
    with open(html_file_path, 'r') as file:
        html_content = file.read()
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all image tags
    img_tags = soup.find_all('img')
    
    # List to hold images
    images = []
    
    # Process each image
    for img in img_tags:
        src = img.get('src')
        
        # Check if it is a base64 image
        if src.startswith('data:image/png;base64,'):
            # Extract base64 string and decode it
            base64_string = src.split('data:image/png;base64,')[1]
            image_data = base64.b64decode(base64_string)
            
            # Create an image from the bytes and append to list
            image = Image.open(BytesIO(image_data))
            images.append(image)

    # Determine the total width and height for the merged image
    total_width = max(image.width for image in images)
    total_height = sum(image.height for image in images)

    # Create a new image with a white background
    merged_image = Image.new('RGBA', (total_width, total_height), 'white')

    # Paste images into the new image, centering horizontally
    y_offset = 0
    for image in images:
        x_offset = (total_width - image.width) // 2
        merged_image.paste(image, (x_offset, y_offset), image)
        y_offset += image.height

    # Save the merged image
    merged_image.save(f'{os.path.dirname(html_file_path)}/{get_filename_without_extension(html_file_path)}.png')

def get_filename_without_extension(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python extract_images.py <html_file_path>")
        sys.exit(1)
    
    html_file_path = sys.argv[1]
    save_images_from_html_file(html_file_path)
