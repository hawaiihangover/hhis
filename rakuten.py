import collections
import csv
from hhproduct import *

class RakutenFace(object):

    SKU_HEADER = ['seller-id','gtin','isbn','mfg-name','mfg-part-number',
                  'asin','seller-sku','title','description','main-image',
                  'additional-images','weight','features','listing-price',
                  'msrp','category-id','keywords','product-set-id',
                  'Age Gender','Apparel Material','Apparel Size','Baby Sizes',
                  'Bra Accessories Type','Bra Cup Sizes','Bra Type',
                  'Chest Size','Chest Size Range','Children Suit Sizes',
                  'Closure Type','Color','Color Class','Dress Type',
                  'Fit Type','Foot Style','Gift Set','Hooded','Inseam Size',
                  'Leg Type','Leg Warmers','Lingerie Type','Lining',
                  'Neck Circumference Range','Neck Style','Occasion',
                  'One Piece Style','Outerwear Styles','Padding','Pajama Style',
                  'Pant Size','Pant Style','Pants Type','Pattern Style',
                  'Profession','Regional Size Classification','Set',
                  'Shapewear & Slips Type','Shirts & Tops Size','Size Modifier',
                  'Skirt/Dress Length','Skirts Style','Sleeve Length',
                  'Sleeve Style','Sock Length','Sock Size','Sock Style',
                  'Sock Type','Suit Bottoms','Suit Fit','Suit Length',
                  'Suit Sets','Suit Sizes','Suit Style','Suit Tops',
                  'Swim Bottom Styles','Swim Top Styles','Swimwear Material',
                  'Swimwear Type','Theme','Top Style','Undergarment Style',
                  'Undergarment Type','Underpants Type','Undershirt Type',
                  'Underwear Type','Waist Size','Waistlines','Wire']
              
    LIST_HEADER = ['ListingId','ProductId','ProductIdType','ItemCondition',
                   'Price','MAP','MAPType','Quantity','OfferExpeditedShipping',
                   'Description','ShippingRateStandard','ShippingRateExpedited',
                   'ShippingLeadTime','OfferTwoDayShipping','ShippingRateTwoDay',
                   'OfferOneDayShipping','ShippingRateOneDay',
                   'OfferLocalDeliveryShippingRates','ReferenceId']

    SELLER_ID = 42953142
    
    def __init__(self):
        self.rakuten_new_product_file = 'rakuten_new_product_test.csv'
        self.rakuten_list_product_file = 'rakuten_list_product_test.csv'
                
        
    def create_data(self, collection):
    
        dr = []
               
        for p in collection:
            for v in p:
                cp = [None] * len(self.SKU_HEADER)        
                
                cp[self.SKU_HEADER.index('seller-id')] = self.SELLER_ID
                cp[self.SKU_HEADER.index('gtin')] = v.upc
                cp[self.SKU_HEADER.index('mfg-name')] = collection.supplier.name
                cp[self.SKU_HEADER.index('mfg-part-number')] = v.mfg_num
                cp[self.SKU_HEADER.index('seller-sku')] = v.sku
                cp[self.SKU_HEADER.index('title')] = p.name
                cp[self.SKU_HEADER.index('description')] = ''#'"' + collection.rakuten_description + '"'
                cp[self.SKU_HEADER.index('main-image')] = p.image
                cp[self.SKU_HEADER.index('additional-images')] = p.alt_images
                cp[self.SKU_HEADER.index('weight')] = v.weight
                cp[self.SKU_HEADER.index('features')] = collection.rakuten_features
                cp[self.SKU_HEADER.index('listing-price')] = v.price
                cp[self.SKU_HEADER.index('category-id')] = collection.rakuten_cat_id
                cp[self.SKU_HEADER.index('keywords')] = '|'.join(p.collection.tags)
                cp[self.SKU_HEADER.index('product-set-id')] = p.sku

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
