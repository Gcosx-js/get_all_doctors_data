import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


####################################################
#                                                   #
#            ### ATTENTION ###                      #
#                                                   #
#    !    FOR EDUCATIONAL PURPOSE ONLY     !        #
#                                                   #
####################################################

def get_page_data(url):
    html_text = requests.get(url).text
    # get list that contains the profiles
    regex_model = re.compile(r'<h3><a href="(/az/h%C9%99kiml%C9%99r/[^"]+)">')
    doctors_profiles = set(re.findall(regex_model, html_text))
    page_data = []
    # Get all doctor profiles in web page & parse it
    for profil in doctors_profiles:
        profile_text = requests.get('https://hekimtap.az' + profil + '/%C9%99laq%C9%99').text
        soup = BeautifulSoup(profile_text, 'html.parser')
        fullname = soup.find('h2', itemprop='name').text.replace('"', '')
        mobilphone = soup.find('p', class_='color_text mobile_version').text.strip()
        href_pattern = re.compile(r'<a\s+href="(/az/h%C9%99kiml%C9%99r\?speciality=[^"]+)">([^<]+)</a>', re.IGNORECASE)
        speciality_matches = href_pattern.findall(profile_text)
        speciality = speciality_matches[0][1] if speciality_matches else 'Not found'
        page_data.append([fullname, mobilphone, speciality])
        print('Data which is parsed : ',fullname, mobilphone, speciality)
    print('Page passed')
    
    return page_data

all_data = [] # only page 1 (first page) parsing like that
all_data.extend(get_page_data('https://hekimtap.az/az/h%C9%99kiml%C9%99r'))

# get all web page data among [2-35] 
for page_num in range(2, 36):
    page_url = f'https://hekimtap.az/az/h%C9%99kiml%C9%99r?page={page_num}'
    page_data = get_page_data(page_url)
    print(page_data)
    all_data.extend(page_data)
# Collect all data in CSV file with dataframe type
data_df = pd.DataFrame(all_data, columns=['Full name', 'Mobile phone', 'Speciality'])
data_df.to_csv('data.csv', index=False)