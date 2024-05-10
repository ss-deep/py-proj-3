import csv

melon_dict={}

class Melon:

    def __init__(self,melon_id,common_name,price,image_url,color,seedless):
        self.melon_id=melon_id
        self.common_name=common_name
        self.price=price
        self.image_url=image_url
        self.color=color
        self.seedless=seedless

    def __repr__(self):
        return (f"<Melon {self.melon_id}, {self.common_name}>")
    
    def price_str(self):
        return f"${self.price:.2f}"
    
def find_melon(melon_id):
    return melon_dict[melon_id]

def all_melons():
    return list(melon_dict.values())

with open('starter/melons.csv') as f:
    rows=csv.DictReader(f)
    for row in rows:
        melon_id=row['melon_id']
        melon=Melon(melon_id,row['common_name'],float(row['price']),row['image_url'],row['color'],eval(row['seedless']))
        melon_dict[melon_id]=melon

# print(find_melon('cren'))
# print(melon_dict)
