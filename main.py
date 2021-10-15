print("Hello World")
print("This is another Hello World")
import json

data = [json.loads(line) for line in open('News_Category_Dataset_v2.json', 'r')]
for i in data:
    print(i)
        
