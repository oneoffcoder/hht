import json
import re

def get_citations(s):
    a = re.findall(r'\[.*?\]', s)
    b = [c.replace('[', '').replace(']', '') for c in a]
    b = [c.split(',') for c in b]
    b = [[item.strip() for item in c] for c in b]
    
    return {x: y for x, y in zip(a, b)}

def update_citations(cits, bibs):
    u = {k: ','.join([bibs[c] for c in v])
            for k, v in cits.items()}
    return {k: f':cite:`{v}`' for k, v in u.items()}

def update_text(text, bibcits):
    t = text
    for k, v in bibcits.items():
        t = t.replace(k, v)
    return t

def update_event(event, bibs):
    def get_era(event):
        yr = event['date']['yr']
        era = -1 * yr if event['date']['era'] == 0 else yr
        return era

    text = event['txt']

    citations = get_citations(text)
    event['txt'] = update_text(text, update_citations(citations, bibs)) if len(citations) > 0 else text
    event['era'] = get_era(event)

    return event

def get_events():
    bibs = {bib['id']: bib['key'] 
            for bib in json.load(open('bibliography.json', 'r'))}
    events = json.load(open('events.json', 'r'))
    return [update_event(e, bibs) for e in events]

def get_eras():
    eras = json.load(open('eras.json', 'r'))

    data = []

    for item in eras:
        start, stop = item['era']['start'], item['era']['stop']
        keywords = [keyword['word'] for keyword in item['keywords']]
        keywords = [f'* ``{w}``' for w in keywords]
        keywords = '\n'.join(keywords)
        
        if start < 0:
            stem = f't{abs(start):04}BC'
            fname = f'{stem}.rst'
            b = f'{abs(start)}'
            e = f'{abs(stop)}'
            title = f'{b} to {e} BC'
        else:
            stem = f't{start:04}AD'
            fname = f'{stem}.rst'
            b = f'{start}'
            e = f'{stop}'
            title = f'{b} to {e} AD'

        data.append({
            'toc_entry': '   ' + stem,
            'title': title,
            'keywords': keywords,
            'fname': fname,
            'start': start,
            'stop': stop
        })

    return data