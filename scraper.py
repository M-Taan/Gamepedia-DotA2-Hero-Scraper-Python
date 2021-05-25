from bs4 import BeautifulSoup
import requests


# Getting the designated url

def get_url(url):
    request = requests.get(url).text
    soup = BeautifulSoup(request, 'lxml')
    return soup


# Using find_all function to get the divs that contain all hero names and loop through them
# Enter each hero page link

def scrape(soup):
    heroes = soup.find_all('div', class_='heroentry')
    attributes = {}
    temp_list = []
    for hero in heroes:
        hero_name = hero.find('div', class_='heroentrytext').text
        hero_pageLink = hero.div.a['href']
        full_url = "https://dota2.fandom.com" + hero_pageLink
        request2 = requests.get(full_url).text
        inside_soup = BeautifulSoup(request2, 'lxml')

        # The table is divided into 2 parts
        attrs_ = inside_soup.find('table', class_='evenrowsgray')
        attr_table1 = attrs_.find('tbody')
        stats = attr_table1.find_all('td')
        for stat in stats:
            temp_list.append(stat.text.replace(' ', '').rstrip("\n"))

        # The 2nd table attributes retrieval
        attrs2_ = inside_soup.find('table', class_='oddrowsgray')
        attr_table2 = attrs2_.find('tbody')
        stats2 = attr_table2.find_all('td')
        for stat2 in stats2:
            temp_list.append(stat2.text.replace(' ', '').rstrip("\n"))

        attributes[hero_name] = temp_list
        temp_list = []

    return attributes


# Enter the data
url = 'https://dota2.fandom.com/wiki/Dota_2_Wiki'
soup = get_url(url)
scraped_data = scrape(soup)

print(scraped_data)

# Indexing:
'''
Dictionary Key = Hero Name

0: Strength
1: Agility
2: Intelligence
3: Health
4: Health regen
5: Mana
6: Mana regen
7: Armor
8: Att/sec
9: Damage
10: Magic resistance
11: Movement speed
12: Attack speed
13: Turn rate
14: Vision range
15: Attack range
16: Projectile speed
17: Attack animation
18: Base attack time
19: Damage block
20: Collision size
21: Legs
22: Gib type

'''
