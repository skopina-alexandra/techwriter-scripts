import xml.etree.ElementTree as ET

f = open('input.txt', mode="r", encoding="utf-8")
xml = f.read()
f.close()
# Parse the XML
root = ET.fromstring(xml)

# Create a dictionary to store the output
output_dict = {}

# Iterate over the XML elements
for element in root:
    if element.tag == "keydef":
        keys = element.attrib['keys']
        href = element.attrib['href']
        try:
            locales = element.attrib['locale'].split()
        except:
            locales = ['default']

        for locale in locales:
            if locale in output_dict:
                output_dict[locale][keys] = href
            else:
                output_dict[locale] = {keys: href}

# Print the output
for locale, keys_dict in output_dict.items():
    print(f'{locale}:')
    for keys, href in keys_dict.items():
        print(f'    {keys}: {href}')