def process_text(texts):
    """
    set texts
    """
    try:
        texts.remove('')
    except: # if "" is not found in the set, ignore the error
        pass

    texts = map( lambda x: x, texts)
    result = list()
    for item in texts:
        result.append('-'.join(item.split(' ')).lower())

    # remove null value
    try:
        result.remove('null')
    except: # if no 'null' value found, then ignore the error
        pass

    return result
