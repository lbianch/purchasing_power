import json
import os

def read_json(f):
    if isinstance(f, str):
        # If it refers to a filename, need to open and use ``json.load`` 
        if os.path.exists(f):
            with open(f, 'r', encoding='utf-8') as f:
                 return json.load(f)
        # Support for filename input which lacks the `.json` extension
        if not f.lower().endswith('.json') and os.path.exists(f + '.json'):
            return JSON(f + '.json')
        # Assume `str` input is raw JSON
        return json.loads(f)
    # Assume `f` refers to a file-like object
    return json.load(f)
