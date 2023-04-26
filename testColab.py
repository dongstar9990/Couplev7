import shutil
# Mở file1.txt để đọc nội dung
with open('datafv.sql', 'r') as file1:
    content = file1.read()
print(content)
content = content.replace('"', '')
content=content.replace('TEXT' , 'MEDIUMTEXT')
print(content)
# Mở file2.txt để ghi nội dung
with open('demodata.sql', 'w') as file2:
    file2.write(content)
print("hoan thanh")

