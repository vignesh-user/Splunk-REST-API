import urllib.request, urllib.parse, urllib.error
import httplib2
import re

baseurl = 'https://<ip-address>:8089'
Authorization_token = "Splunk <API-token>

# ------------ Search Query ------------

searchQuery = 'index=_internal | head 10'

# ---------------------------------------

# Remove leading and trailing whitespace from the search
searchQuery = searchQuery.strip()

# If the query doesn't already start with the 'search' keyword it adds search keyword at the start
if not (searchQuery.startswith('search') or searchQuery.startswith("|")):
    searchQuery = 'search ' + searchQuery
print(searchQuery)

# Run the search.
response = (httplib2.Http(disable_ssl_certificate_validation=True).request(baseurl + '/services/search/jobs','POST',
    headers={'Authorization': Authorization_token},body=urllib.parse.urlencode({'search': searchQuery}))[1])

sid = response.decode().split('<sid>')[1].split('</sid>')[0]
print(f"Search ID = {sid}")

# Check job status
print(f"Search Job in Progress for {sid}...")

while True:
    status_response = (httplib2.Http(disable_ssl_certificate_validation=True).request(baseurl + f'/services/search/jobs/{sid}/?output_mode=json','GET',
    headers={'Authorization': Authorization_token}))
    # print(status_response)
    true_pattern = r'isDone":true'
    false_pattern = r'isDone":false'
    if re.search(true_pattern, str(status_response)):
        print(f"Search Job is Completed for {sid}\n")
        break

# Search Result
search_result = (httplib2.Http(disable_ssl_certificate_validation=True).request(baseurl + f'/services/search/jobs/{sid}/results?output_mode=json','GET',
    headers={'Authorization': Authorization_token}))

print(search_result)
