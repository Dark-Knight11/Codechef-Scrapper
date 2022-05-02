import requests
from bs4 import BeautifulSoup
import pandas as pd

#---------------------------------------------------------------------------------------------------#
#--------------------------------------Enter Problem Codes here-------------------------------------#
#---------------------------------------------------------------------------------------------------#
codes = ['ENGXOR', 'BENCHP', 'OLYRANK', 'ALBOFACE']
#---------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------#


# function for removing html tags
def remove_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(['style', 'script']):
        data.decompose()
    return ' '.join(soup.stripped_strings)


# loading the data from excel sheet
df = pd.read_excel('data.xlsx')
df1 = df[['name', 'username', 'Timestamp']]

if __name__ == '__main__':
    r = []
    # looping through username and problem codes
    for username, name in zip(df.username, df.name):
        print(f"Fetching {name}'s data...")
        page = requests.get(f"https://www.codechef.com/users/{username}")
        soup = BeautifulSoup(page.content, 'html.parser')
        div = soup.find_all(
            'section', {'class': 'rating-data-section problems-solved'})
        pb_codes = remove_tags(str(div))
        dc = {}
        for code in codes:
            val = 'FALSE'
            if code in pb_codes:
                val = 'TRUE'
            dc[code] = val
        r.append(dc)

    mn = []
    for code in codes:
        g = []
        for res in r:
            g.append(res.get(code))
        mn.append(g)
    dc = {**{'Name': df1.name}, **dict(zip(codes, mn))}

    # Writing the data to excel sheet
    df = pd.DataFrame(dc)
    df.to_excel('datasheet.xlsx', index=False)
