import xml.etree.ElementTree as ET

import sys

def printMeta(pathToFile):
    f = open(pathToFile, mode="r", encoding="utf-8")
    xml = f.read()
    f.close()

    root = ET.fromstring(xml).find('metadata')

    product_terms = {}

    keys = []

    for keyword in root.find('keywords').findall('keyword'):
        if not 'keywords' in keys:
            keys.append('keywords')
        products = list(keyword.get('product').split())
        for product in products:
            if product not in product_terms:
                product_terms[product] = {}
                product_terms[product].update({'keywords': keyword.text})
            else:
                product_terms[product].update({'keywords': product_terms[product].get('keywords') + ', ' + keyword.text})

    for othermeta in root.findall('othermeta'):
        products = list(othermeta.get('product').split())
        for product in products:
            if product not in product_terms:
                product_terms[product] = {}
            product_terms[product].update({othermeta.get('name'): othermeta.get('content')})

            if not othermeta.get('name') in keys:
                keys.append(othermeta.get('name'))



    for product in product_terms:
        print(product + ': \n')
        for key in keys:
            if product_terms[product].get(key) == None:
                print('  ' + key + ': ""\n')
            else:
                print('  ' + key + ': ' + product_terms[product].get(key) + '\n')



if __name__ == "__main__":
    pathToFile = int(sys.argv[1])
    printMeta(pathToFile)

