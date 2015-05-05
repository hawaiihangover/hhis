#Provide an overall solution to manage products.
# 1. Create flat file format for uploading purpose.
# 2. Generate feeds to upload to various system.
# 3. Provide image manipulations prior to uploading.
# 4. Sync inventory

from os.path import basename, splitext
import openpyxl as exl
import re


class Supplier(object):
    
    def __init__(self):
        
        self._data = None
        self.name = ''
        self.collections = []
        self.patterns = set()
        
    def __str__(self):
        return self.name
        
    def __iter__(self):
        return iter(self.collections)
        
    def product_count(self):
        count = 0
        for c in self.collections:
            count += c.product_count()
            
        return count
        
    def find_products(self, sku=None, exp=None):
        match_list = []
        for c in self.collections:
            match_list.extend(c.find_products(sku, exp))
        
        return match_list
        
    def _add_patterns(self):
        tms = set()
        
        for c in self.collections:
            tms = tms.union(c.patterns)
            
        self.patterns = tms
        
        
    def parse_excel(self, file_name):
    
        """ Parse Hawaii Hangover Spreadsheet Catalog.
        A single file currently represents one supplier,
        each sheet in the workbook contains details a collection
        of products.
        """
    
        self.name = splitext(basename(file_name))[0]
        self._data = exl.load_workbook(file_name)
        
        for sheet_name in self._data.get_sheet_names():
            sheet = self._data.get_sheet_by_name(sheet_name)
            
            collection = Collection()
            collection.supplier = self
            collection.parse_sheet(sheet)
            self.collections.append(collection)
            
        self._add_patterns()


class Collection(object):

    def __init__(self):
    
        self.name = ''
        self.title = ''
        self.patterns = set()
        self.supplier = None
        self.products = []
        self.tags = []
        
        self.namere = ''
        
        self.magento_description = ''
        self.magento_attribute_set= ''
        self.magento_category = []
        self.magento_attribute_code = ''
        
        self.rakuten_description = ''
        self.rakuten_features = ''
        self.rakuten_age_gender = ''
        self.rakuten_material = ''
        self.rakuten_cat_id = ''
        self.rakuten_top_style = ''
        
        
    def __str__(self):
        return self.name
        
    def __iter__(self):
        return iter(self.products)
        
    def _add_patterns(self):
        for p in self.products:
            self.patterns.add(p.pattern)
            
    def find_products(self, sku=None, exp=None):
        match_list = []
        for p in self.products:
            if p.find_product(sku, exp):
                match_list.append(p)
                
        return match_list


    def product_count(self):
        return len(self.products)
        

    def locate_row(self, sheet, text):
        i = 1
        while sheet['A'+str(i)].value != text:
            i += 1
        return i

                
    def parse_sheet(self, sheet):
        
        self.name = sheet.title
        self.title = sheet['B2'].value
        self.namere = sheet['B3'].value
        
        self.magento_description = sheet['F4'].value
        self.magento_attribute_set= sheet['F2'].value
        self.magento_category = sheet['F3'].value.split(',')
        
        self.rakuten_description = sheet['I2'].value
        self.rakuten_features = sheet['I3'].value
        self.rakuten_age_gender = sheet['I4'].value
        self.rakuten_material = sheet['I5'].value
        self.rakuten_cat_id = sheet['I6'].value
        self.rakuten_top_style = sheet['I7'].value

        sku_row = self.locate_row(sheet, 'SKU') + 1
               
        while sheet['A'+str(sku_row)].value is not None:
            if (sheet['C'+str(sku_row)].value is not None and
                sheet['C'+str(sku_row)].value != ""):
                product = Product()
                product.collection = self
                sku_row = product.parse_row(sheet, sku_row)
                self.products.append(product)
            else:
                sku_row += 1
            
        self._add_patterns()
    
        
class Product(object):
    """ Base Product Class with Basic Common Attributes"""

    def __init__(self):
        
        self.sku = ''
        self.name = ''
        self.pattern = ''
        self.collection = None
        self.color = []
        self.tags = []
        self.variations = []
        self.image = ''
        self.alt_images = ''
        
    def __str__(self):
        return self.sku
        
    def __iter__(self):
        return iter(self.variations)
    
    def find_product(self, sku=None, exp=None):
        if sku is not None:
            return self.sku == sku
            
        if re is not None:
            if (re.search(exp, self.sku) is not None or
                re.search(exp, self.name) is not None):
                return True

        return False

    def parse_row(self, sheet, row_n):
        
        self.sku = sheet['A'+str(row_n)].value
        self.pattern = sheet['C'+str(row_n)].value
        self.image = sheet['J'+str(row_n)].value
        self.alt_images = sheet['K'+str(row_n)].value
        
        if self.collection is not None:
            namere = self.collection.namere
            
            if '<Name>' in namere:
                namere = re.sub('<Name>', self.collection.name, namere)
            if '<Pattern>' in namere:
                namere = re.sub('<Pattern>', self.pattern, namere)
            if '<Material>' in namere:
                namere = re.sub('<Material>', self.collection.rakuten_material, namere)
                
            self.name = namere
        
        row_n += 1
        while sheet['B'+str(row_n)].value is not None:
            variation = Variation()
            variation.product = self
            variation.parse_var(sheet, row_n)
            self.variations.append(variation)
            row_n += 1
            
        return row_n


class Variation(object):
    
    def __init__(self):
        
        self.sku = ''
        self.price = ''
        self.cost = ''
        self.weight = ''
        self.upc = ''
        self.size = ''
        self.mfg_num = ''
        self.product = None
        
    
    def __str__(self):
        print self.sku
        
        
    def parse_var(self, sheet, row_n):
        
        self.sku = sheet['B'+str(row_n)].value
        self.size = sheet['D'+str(row_n)].value
        self.price = sheet['E'+str(row_n)].value
        self.cost = sheet['F'+str(row_n)].value
        self.weight = sheet['G'+str(row_n)].value
        self.upc = sheet['H'+str(row_n)].value
        self.mfg_num = sheet['I'+str(row_n)].value
