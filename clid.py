""" helper functions for caller ID lookups """

licensetext = """
Copyright 2020-2022 Gregory A. Broiles

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

abouttext = """
This program accepts a ten digit NANP telephone number and performs a Caller ID lookup using the service provided by Bulk Solutions LLC (https://bulkvs.com) and returns the results of that lookup, if any.

The author of this program (Gregory A. Broiles) is not compensated in any way for usage of this program or Bulk Solutions LLC's service.

The author offers no warranty, express or implied regarding the accuracy of results returned by this software or Bulk Solutions LLC's service.

"""


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
