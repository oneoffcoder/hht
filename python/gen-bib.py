import json

with open('bibliography.json', 'r') as f:
    bibs = json.load(f)

keys = [bib['key'] for bib in bibs]

print(len(keys))
print(len(set(keys)))

citations = []
for source in bibs:
    stype = source['type']
    key = source['key']
    title = source['title']
    year = str(source['year'])
    
    authors = ' and '.join(source['author']) if 'author' in source else None
    publisher = source['publisher'] if 'publisher' in source else None
    url = source['url'] if 'url' in source else None

    cite = f'@{stype}'
    cite += '{'
    cite += key
    cite += ',year={' + year + '}'
    cite += ',title={' + title + '}'
    if authors is not None:
        cite += ',author={' + authors + '}'
    if publisher is not None:
        cite += ',publisher={' + publisher + '}'
    if url is not None:
        cite += ',url={' + url + '}'
    cite += '}'

    print(cite)
    citations.append(cite)

with open('refs.bib', 'w') as f:
    c = '\n'.join(citations)
    f.write(c)