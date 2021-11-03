#test
def download(url, num_retries=2):
    import urllib.request 
    import urllib.error    
    print('Downloading:', url)
    try:
        html = urllib.request.urlopen(url).read()
    except urllib.error.URLError as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
            # recursively retry 5xx HTTP errors
                return download(url, num_retries-1)
    return html
