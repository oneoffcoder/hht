import json
from hht import get_events, get_eras

def create_rst(era, events):
    def get_date(event):
        yr = event['date']['yr']
        mm = event['date']['mm']
        dd = event['date']['dd']

        if mm > 0 and dd > 0:
            return f'``{mm}-{dd}-{yr}``: '
        if mm > 0:
            return f'``{mm}-{yr}``: '
        return ''

    with open(era['fname'], 'w') as f:
        f.write(era['title'])
        f.write('\n')
        f.write('=' * len(era['title']))
        
        f.write('\n\n')
        f.write('Keywords')
        f.write('\n')
        f.write('-' * len('Keywords'))
        f.write('\n\n')
        f.write(era['keywords'])
        
        f.write('\n\n')
        f.write('Events')
        f.write('\n')
        f.write('-' * len('Events'))
        f.write('\n\n')

        for e in events:
            d = get_date(e)
            f.write('* ' +  d + e['txt'])
            f.write('\n')

events = get_events()
eras = get_eras()

for i, era in enumerate(eras):
    start = era['start']
    stop = era['stop']
    era_events = list(filter(lambda e: start <= e['era'] < stop, events))
    create_rst(era, era_events)