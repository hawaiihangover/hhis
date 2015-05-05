from hhproduct import *
from rakuten import *

palmwave = Supplier()
palmwave.parse_excel('Palmwave.xlsm')

mf = RakutenFace()

for c in palmwave:
    mf.rakuten_new_product_file = c.name + '.csv'
    dl = mf.create_data(c)
    mf.write_data(dl)
