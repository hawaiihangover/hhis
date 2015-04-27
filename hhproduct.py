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
        self.description = ''
        self.sizes = []
        self.patterns = set()
        self.cost_map = {}
        self.price_map = {}
        self.supplier = None
        self.products = []
        
        self.namere = ''
        self.magento_attribute_set= ''
        self.magento_category = []
        self.magento_attribute_code = 'size_sto4xl'
        
        
    def __str__(self):
        return self.name
        
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
        
    def _parse_size_segment(self, sheet, row_n, id):
        
        if sheet['A'+str(row_n)].value != id:
            return None
            
        smap = {}
        if len(self.sizes) == 1:
            smap['onesize'] = sheet['B'+str(row_n)].value
            row_n += 1
        else:
            while (sheet['A'+str(row_n)].value == "" or
                   sheet['A'+str(row_n)].value is None or
                   sheet['A'+str(row_n)].value == id):
                if (sheet['B'+str(row_n)].value is None or
                    sheet['B'+str(row_n)].value == ""):
                   break
                szs = sheet['B'+str(row_n)].value.split(',')
                price = sheet['C'+str(row_n)].value
                for s in szs:
                    smap[s] = price
                row_n += 1
            
        return smap, row_n

                
    def parse_sheet(self, sheet):
        
        self.sizes = sheet['B1'].value.split(',')
        self.name = sheet['B2'].value
        self.namere = sheet['B3'].value
        self.description = sheet['B4'].value
        self.magento_attribute_set= sheet['B5'].value
        self.magento_category = sheet['B6'].value.split(',')
        
        row_n = 7
        self.price_map, row_n = self._parse_size_segment(sheet, row_n, 'Price')
        self.cost_map, row_n = self._parse_size_segment(sheet, row_n, 'Cost')
        row_n += 2

        while sheet['A'+str(row_n)].value is not None:
            if (sheet['B'+str(row_n)].value is not None and
                sheet['B'+str(row_n)].value != ""):
                product = Product();
                product.collection = self
                product.parse_row(sheet, row_n)
                self.products.append(product)
            row_n += 1
            
        self._add_patterns()
    
        
class Product(object):
    """ Base Product Class with Basic Common Attributes"""

    def __init__(self):
        
        self.sku = ''
        self.name = ''
        self.pattern = ''
        self.collection = None
        
        self.color = []
        
    def __str__(self):
        return self.sku
        
            
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
        self.pattern = sheet['B'+str(row_n)].value
        
        if self.collection is not None:
            self.name = re.sub('<Pattern>', self.pattern,
                re.sub('<Name>', self.collection.name,
                self.collection.namere))
        

