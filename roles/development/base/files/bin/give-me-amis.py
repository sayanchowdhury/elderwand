#!/usr/bin/env python3.4

import requests
import fedfind

DATAGREPPER_URL = 'https://apps.fedoraproject.org/datagrepper/raw'
def _get_data_from_datagrepper(compose_id):
    params = {
        'category': 'fedimg',
        'topic': 'org.fedoraproject.prod.fedimg.image.upload',
        'contains': compose_id,
        'rows_per_page': 100,
    }

    resp = requests.get(DATAGREPPER_URL, params=params)
    print resp

print _get_data_from_datagrepper('Fedora-25-20161023.n.0')
