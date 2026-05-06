import csv
import os
import re
import unicodedata

def remove_accents(input_str):
    if not input_str:
        return ""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    result = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    replacements = {'đ': 'd', 'Đ': 'd'}
    for k, v in replacements.items():
        result = result.replace(k, v)
    return result

def normalize_name(name):
    # Remove content in parentheses for main name
    clean_name = re.sub(r'\(.*?\)', '', name)
    clean_name = remove_accents(clean_name).lower()
    clean_name = re.sub(r'[^a-z0-9\s]', '', clean_name)
    return clean_name.strip()

# List all image files
image_extensions = ('.jpg', '.jpeg', '.png', '.webp')
image_files = [f for f in os.listdir('.') if f.lower().endswith(image_extensions)]

# Load CSV
rows = []
header = []
with open('list_50_loai_tra.csv', mode='r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        rows.append(row)

NAME_IDX = 1
COL1_IDX = 8

def get_score(name, filename):
    filename_clean = remove_accents(os.path.splitext(filename)[0]).lower()
    filename_clean = re.sub(r'[^a-z0-9]', ' ', filename_clean)
    
    name_words = set(name.split())
    file_words = set(filename_clean.split())
    
    # Intersection of words
    common = name_words.intersection(file_words)
    return len(common)

for row in rows:
    product_name = row[NAME_IDX]
    norm_name = normalize_name(product_name)
    
    best_match = ""
    max_score = 0
    
    # Try exact slug match first
    slug = norm_name.replace(' ', '-')
    for img in image_files:
        img_slug = os.path.splitext(img)[0].replace(' ', '-').lower()
        if slug == img_slug:
            best_match = img
            max_score = 999
            break
            
    if max_score < 999:
        for img in image_files:
            score = get_score(norm_name, img)
            if score > max_score:
                max_score = score
                best_match = img
    
    # Minimum score to consider a match (at least 2 words matching)
    if max_score >= 2:
        row[COL1_IDX] = best_match
    else:
        # Special case for 1 word matches or specific patterns
        if "Atiso" in product_name and any("atiso" in f.lower() for f in image_files):
             for img in image_files:
                 if "atiso" in img.lower():
                     row[COL1_IDX] = img
                     break
        elif "Biếu Tết" in product_name:
             for img in image_files:
                 if "biet-tet" in img.lower():
                     row[COL1_IDX] = img
                     break
        else:
             row[COL1_IDX] = ""

# Write back to CSV
with open('list_50_loai_tra.csv', mode='w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print("Done processing CSV with fuzzy matching.")
