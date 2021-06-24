import os

files = []
directories = []
for r, d, f in os.walk('./import'):
    if d:
        directories = d
    for file in f:
        if '.xml' in file:
            files.append(file)

print(files)