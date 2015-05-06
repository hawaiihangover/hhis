import collections
import csv
from hhproduct import *

class NeweggFace(object):

    BasicItem_HEADER= ['Seller Part #','Manufacturer','Manufacturer Part # / ISBN',
                       'UPC','Related Seller Part#','Website Short Title',
                       'Bullet Description','Product Description','Item Length',
                       'Item Width','Item Height','Item Weight','Packs Or Sets',
                       'Item Condition','Item Package','Shipping Restriction',
                       'Currency','MSRP','MAP','CheckoutMAP','Selling Price',
                       'Shipping','Inventory','Activation Mark','Action',
                       'Item Images','Prop 65','Country Of Origin',
                       'Prop 65 - Motherboard','Age 18+ Verification',
                       'Choking Hazard 1','Choking Hazard 2','Choking Hazard 3',
                       'Choking Hazard 4']
                               
    MensCasualShirt_HEADER = ['MensShirtsBrand','MensShirtsModel',
                              'MensShirtsSize','MensShirtsType','MensShirtsColor',
                              'MensShirtsColorMapping','MensShirtsAge','MensShirtsOccasion',
                              'SportsGlobalSportsTeam','SportsGlobalSportsLeague',
                              'MensShirtsFeatures']
                              
    ChildrensSwimwear_HEADER = ['ChildrensSwimwearBrand','ChildrensSwimwearModel',
                                'ChildrensSwimwearSize','ChildrensSwimwearType',
                                'ChildrensSwimwearColor','ChildrensSwimwearColorMapping',
                                'ChildrensSwimwearGender','ChildrensSwimwearAge',
                                'SportsGlobalSportsTeam','SportsGlobalSportsLeague']
    
    def __init__(self):
        self.newegg_product_file = 'rakuten_new_product_test.csv'

    def create_data(self, collection):
    
        dr = []
               
        for p in collection:
            for v in p:
                cp = [None] * len(self.MensCasualShirt_HEADER)
            
                cp[self.MensCasualShirt_HEADER.index('Seller Part #')] = v.sku
                cp[self.MensCasualShirt_HEADER.index('Manufacturer')] = collection.supplier.name
                cp[self.MensCasualShirt_HEADER.index('UPC')] = v.upc
                cp[self.MensCasualShirt_HEADER.index('Website Short Title')] = p.title
                cp[self.MensCasualShirt_HEADER.index('Bullet Description')] = collection.rakuten_features.replace('|', '^^')
                cp[self.MensCasualShirt_HEADER.index('Product Description')] = collection.rakuten_description
                cp[self.MensCasualShirt_HEADER.index('Item Weight')] = v.weight
                cp[self.MensCasualShirt_HEADER.index('Packs Or Sets')] = 1
                cp[self.MensCasualShirt_HEADER.index('Item Condition')] = 'New'
                cp[self.MensCasualShirt_HEADER.index('Selling Price')] = v.price
                cp[self.MensCasualShirt_HEADER.index('Shipping')] = 'Default'
                cp[self.MensCasualShirt_HEADER.index('Inventory')] = 10 #default inventory
                cp[self.MensCasualShirt_HEADER.index('Item Images')] = p.image + ',' + p.alt_images.replace('|',',')
                
                if collection.newegg_template == 'ChildrensSwimwear':
                    cp[self.MensCasualShirt_HEADER.index('ChildrensSwimwearSize')] = v.size
                    cp[self.MensCasualShirt_HEADER.index('ChildrensSwimwearType')] = p.newegg_type
                    cp[self.MensCasualShirt_HEADER.index('ChildrensSwimwearGender')] = p.newegg_gender
                    cp[self.MensCasualShirt_HEADER.index('ChildrensSwimwearAge')] = p.newegg_age
                
                dr.append(cp)
            
        return dr
    
    
    def write_data(self, txt_data):
    
        with open(self.newegg_product_file, 'w') as csv_write_file:
            gwriter = csv.writer(csv_write_file, delimiter=',',
                                 quotechar='\'', quoting=csv.QUOTE_MINIMAL)
            gwriter.writerow(self.SKU_HEADER)
            for r in txt_data:
                gwriter.writerow(r)
