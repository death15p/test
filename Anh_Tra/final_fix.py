import csv

# Final manual fixes for tricky ones
mapping = {
    "Trà Quế Hoa (Hoa Mộc)": "tra-hoa-moc.jpg",
    "Trà Hoa Oải Hương (Lavender)": "tra-hoa-lavender.jpg",
    "Trà Đậu Biếc Khô": "tra-hoa-dau-biec.jpg",
    "Bột Matcha Uji Ceremonial": "bot-matcha-uji-ceremonial.jpg",
    "Bột Matcha Vụ Xuân Shizuoka": "bot-matcha-vu-xuan-shizuoka.jpg",
}

rows = []
header = []
with open('list_50_loai_tra.csv', mode='r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        rows.append(row)

NAME_IDX = 1
COL1_IDX = 8

for row in rows:
    name = row[NAME_IDX]
    if name in mapping:
        row[COL1_IDX] = mapping[name]

with open('list_50_loai_tra.csv', mode='w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print("Final corrections applied.")
