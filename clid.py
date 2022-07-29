""" helper functions for caller ID lookups """


def process(apikey, session, subject):
    """perform actual lookup, apikey = API key, s = Requests session"""
    did = str(subject)
    url = "https://cnam.bulkCNAM.com/?id=" + apikey + "&did=" + did
    #    print(url)
    result = session.get(url)
    status = result.status_code
    #    if status != 200:
    #        print("Status: ",status)
    #        print("URL: ",url)
    #        result.raise_for_status()
    return result.text, status


def cleanup(dirty):
    """remove invalid characters from phone number"""
    allowed = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    newstring = ""
    for char in dirty:
        if char in allowed:
            newstring += char
    return newstring
