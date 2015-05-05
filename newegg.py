import collections
import csv
from hhproduct import *

class NeweggFace(object):

    MensCasualShirt_HEADER = ['Seller Part #','Manufacturer','Manufacturer Part # / ISBN',
                              'UPC','Related Seller Part#','Website Short Title',
                              'Bullet Description','Product Description','Item Length',
                              'Item Width','Item Height','Item Weight','Packs Or Sets',
                              'Item Condition','Item Package','Shipping Restriction',
                              'Currency','MSRP','MAP','CheckoutMAP','Selling Price',
                              'Shipping','Inventory','Activation Mark','Action',
                              'Item Images','Prop 65','Country Of Origin',
                              'Prop 65 - Motherboard','Age 18+ Verification',
                              'Choking Hazard 1','Choking Hazard 2','Choking Hazard 3',
                              'Choking Hazard 4','MensShirtsBrand','MensShirtsModel',
                              'MensShirtsSize','MensShirtsType','MensShirtsColor',
                              'MensShirtsColorMapping','MensShirtsAge','MensShirtsOccasion',
                              'SportsGlobalSportsTeam','SportsGlobalSportsLeague',
                              'MensShirtsFeatures']
    
    def __init__(self):
        self.rakuten_new_product_file = 'rakuten_new_product_test.csv'
        self.rakuten_list_product_file = 'rakuten_list_product_test.csv'
                
        
    def create_data(self, collection):
    
        dr = []
               
        for p in collection:
            for v in p:
                if collection.newegg_template == 'MensCasualShort':
                    cp = [None] * len(self.MensCasualShirt_HEADER)
                
                    cp[self.MensCasualShirt_HEADER.index('Seller Part #')] = v.sku
                    cp[self.MensCasualShirt_HEADER.index('Manufacturer')] = collection.supplier.name
                    cp[self.MensCasualShirt_HEADER.index('UPC')] = v.upc
                    cp[self.MensCasualShirt_HEADER.index('Website Short Title')] = p.title
                    cp[self.MensCasualShirt_HEADER.index('Bullet Description')] = collection.rakuten_features.replace('|', '^^')
                    cp[self.MensCasualShirt_HEADER.index('Product Description')] = collection.rakuten_description
                    cp[self.MensCasualShirt_HEADER.index('Item Weight')] = ''#'"' + collection.rakuten_description + '"'
                    cp[self.MensCasualShirt_HEADER.index('Packs Or Sets')] = p.image
                    cp[self.MensCasualShirt_HEADER.index('Item Condition')] = p.alt_images
                    cp[self.MensCasualShirt_HEADER.index('weight')] = v.weight
                    cp[self.MensCasualShirt_HEADER.index('features')] = collection.rakuten_features
                    cp[self.MensCasualShirt_HEADER.index('listing-price')] = v.price
                    cp[self.MensCasualShirt_HEADER.index('category-id')] = collection.rakuten_cat_id
                    cp[self.MensCasualShirt_HEADER.index('keywords')] = '|'.join(p.collection.tags)
                    cp[self.MensCasualShirt_HEADER.index('product-set-id')] = p.sku

                cp[self.SKU_HEADER.index('Age Gender')] = p.collection.rakuten_age_gender
                cp[self.SKU_HEADER.index('Apparel Material')] = p.collection.rakuten_material
                if collection.rakuten_cat_id == '16756':
                    cp[self.SKU_HEADER.index('Shirts & Tops Size')] = v.size
                else:
                    cp[self.SKU_HEADER.index('Apparel Size')] = v.size
                cp[self.SKU_HEADER.index('Color')] = p.pattern
                cp[self.SKU_HEADER.index('Occasion')] = '|'.join(['Wedding','Bridesmaid','Engagament',
                    "Valentine's Day",'Casual','Halloween','Christmas','Dress','Guest of Wedding',
                    'Beach','Holiday','Mother of Bride','Spring','Summer','Prom'])
                cp[self.SKU_HEADER.index('Pattern Style')] = 'Floral'
                
                dr.append(cp)
            
        return dr
    
    
    def write_data(self, txt_data):
    
        with open(self.rakuten_new_product_file, 'w') as csv_write_file:
            gwriter = csv.writer(csv_write_file, delimiter='\t',
                                 quotechar='\'', quoting=csv.QUOTE_MINIMAL)
            gwriter.writerow(self.SKU_HEADER)
            for r in txt_data:
                gwriter.writerow(r)
