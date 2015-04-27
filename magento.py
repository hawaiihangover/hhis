import collections
import csv
from hhproduct import *

class MagentoFace(object):

    HEADER_v1 =  ['sku', '_store', '_attribute_set', '_type', 
                   '_category', '_root_category', '_product_websites',
                   'cabanaset_chad', 'cabanaset_minh', 'color', 'cost', 
                   'country_of_manufacture', 'created_at', 'custom_design',
                   'custom_design_from', 'custom_design_to', 
                   'custom_layout_update', 'description', 'em_deal', 
                   'em_featured', 'em_hot', 'euro_size', 'gallery', 
                   'gift_message_available', 'has_options', 'image', 
                   'image_label', 'manufacturer', 'media_gallery', 
                   'meta_description', 'meta_keyword', 'meta_title', 
                   'minimal_price', 'msrp', 'msrp_display_actual_price_type', 
                   'msrp_enabled', 'name', 'news_from_date', 'news_to_date', 
                   'options_container', 'page_layout', 'pattern_chad', 'price', 
                   'required_options', 'short_description', 'size_6mto14', 
                   'size_boardshorts', 'size_sarong', 'size_sto4xl', 
                   'small_image', 'small_image_label', 'special_from_date', 
                   'special_price', 'special_to_date', 'status', 'tax_class_id', 
                   'thumbnail', 'thumbnail_label', 'updated_at', 'url_key', 
                   'url_path', 'visibility', 'weight', 'qty', 'min_qty', 
                   'use_config_min_qty', 'is_qty_decimal', 'backorders', 
                   'use_config_backorders', 'min_sale_qty', 
                   'use_config_min_sale_qty', 'max_sale_qty', 
                   'use_config_max_sale_qty', 'is_in_stock', 
                   'notify_stock_qty', 'use_config_notify_stock_qty', 
                   'manage_stock', 'use_config_manage_stock', 
                   'stock_status_changed_auto', 'use_config_qty_increments', 
                   'qty_increments', 'use_config_enable_qty_inc', 
                   'enable_qty_increments', 'is_decimal_divided', 
                   '_links_related_sku', '_links_related_position', 
                   '_links_crosssell_sku', '_links_crosssell_position', 
                   '_links_upsell_sku', '_links_upsell_position', 
                   '_associated_sku', '_associated_default_qty', 
                   '_associated_position', '_tier_price_website', 
                   '_tier_price_customer_group', '_tier_price_qty', 
                   '_tier_price_price', '_group_price_website', 
                   '_group_price_customer_group', '_group_price_price', 
                   '_media_attribute_id', '_media_image', '_media_lable', 
                   '_media_position', '_media_is_disabled', 
                   '_super_products_sku', '_super_attribute_code', 
                   '_super_attribute_option', '_super_attribute_price_corr']
               
    SIMPLE_TEMPLATE = ['','','','simple','','','base','','','','','','','default/em0080',
                       '','','','','0','0','0','','','0','0','','','','','','','','','',
                       'Use config','Use config','','','','Product Info Column','','','25.0000','0',
                       '','','','','S','','','','','','1','0','','','','','','1','9.0000',
                       '0.0000','0.0000','1','0','0','1','1.0000','1','0.0000','1','0',
                       '0.0000','1','0','1','1','1','0.0000','1','0','0','','','','','',
                       '','','','','all','2','20.0000','12.5000','all','2','14.0000','',''
                       '','','','','','','','']
    
    CONFIGURABLE_TEMPLATE = ['','','','configurable','',"Default Category",'base','','','','','','',
                            'default/em0080','','','','','0','0','0','','','0','1','','','','',
                            '','','','','','Use config','Use config','','','','Product Info Column',
                            '','','','1','','','','','','','','','','','1','0','','','','','','4',
                            '','0.0000','0.0000','1','0','0','1','1.0000','1','0.0000','1','1',
                            '','1','0','1','0','1','0.0000','1','0','0','','','','','','','','',
                            '','all','2','20.0000','12.5000','all','2','14.0000','','','','',
                            '','','','','']
    
    def __init__(self):
        self.magento_product_file = 'magento_product_test.csv'
        
        
    def create_data(self, product):
        
        szs = product.collection.sizes
        cat = product.collection.magento_category
        
        cp_linecount = max(len(szs), len(cat))
        cp = [None] * cp_linecount
        cp[0] = list(self.CONFIGURABLE_TEMPLATE)
        if szs <= 1:
            cp[0][self.HEADER_v1.index('_type')] = 'simple'
        for i in range(1, len(cp)):
            cp[i] = [''] * 190
            
        min_price = min(product.collection.price_map.values())
        
        cp[0][self.HEADER_v1.index('_attribute_set')] = product.collection.magento_attribute_set
        cp[0][self.HEADER_v1.index('sku')] = product.sku
        cp[0][self.HEADER_v1.index('name')] = product.name
        cp[0][self.HEADER_v1.index('pattern_chad')] = product.pattern
        cp[0][self.HEADER_v1.index('price')] = min_price
        cp[0][self.HEADER_v1.index('short_description')] = product.name
        cp[0][self.HEADER_v1.index('url_key')] = re.sub(' ', '-', product.name.lower())
        cp[0][self.HEADER_v1.index('url_path')] = re.sub(' ', '-', product.name.lower()) + '.html'
        
        for i, c in enumerate(cat):
            cp[i][self.HEADER_v1.index('_category')] = c
            cp[i][self.HEADER_v1.index('_root_category')] = 'Default Category'

        for i, s in enumerate(szs):
            cp[i][self.HEADER_v1.index('_super_products_sku')] = product.sku + '-' + s
            cp[i][self.HEADER_v1.index('_super_attribute_code')] = product.collection.magento_attribute_code
            cp[i][self.HEADER_v1.index('_super_attribute_option')] = s
            price_adj = product.collection.price_map[s] - min_price
            if price_adj > 0:
                cp[i][self.HEADER_v1.index('_super_attribute_price_corr')] = price_adj
            
            sp = list(self.SIMPLE_TEMPLATE)
            sp[self.HEADER_v1.index('sku')] = product.sku + '-' + s
            sp[self.HEADER_v1.index('_attribute_set')] = product.collection.magento_attribute_set
            sp[self.HEADER_v1.index('name')] = product.name
            sp[self.HEADER_v1.index('pattern_chad')] = product.pattern
            sp[self.HEADER_v1.index('price')] = product.collection.price_map[s]
            sp[self.HEADER_v1.index(product.collection.magento_attribute_code)] = s
            sp[self.HEADER_v1.index('url_key')] = re.sub(' ', '-', product.name.lower())
            sp[self.HEADER_v1.index('url_path')] = re.sub(' ', '-', product.name.lower()) + '.html'
            sp[self.HEADER_v1.index('short_description')] = product.name
            
            cp.append(sp)
            
        return cp
            
    
    def write_data(self, txt_data):
        
        with open(self.magento_product_file, 'w') as csv_write_file:
            gwriter = csv.writer(csv_write_file, delimiter=',',
                                 quotechar='"', quoting=csv.QUOTE_MINIMAL)
            gwriter.writerow(self.HEADER_v1)
            for r in txt_data:
                gwriter.writerow(r)
        
