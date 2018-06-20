""" A Python script to find the Fide Events, Tournaments, and Ratings from fide.com"""

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

Choice ={
          "1": "Fide Events",
          "2": "Tournaments",
          "3": "Ratings"
        }

Categories = {
                "1": "Top 100 Players",
                "2": "Top 100 Women",
                "3": "Top 100 Juniors",
                "4": "Top 100 Girls"
             }
Modes = {
           "1": "Standard",
           "2": "Rapid",
           "3": "blitz"
        }

def scrape(url):
    """ To fetch info from the urls """
    response = requests.get(url)
    soup = BeautifulSoup(response.text , "html.parser")
    return soup

def fide_events(soup):
    """ To Fetch Fide Events from fide_events"""
    headers = ["Name", "Place", "Start", "End"]

    tables = soup.find_all("table",{"align":"center"})[1:]
    for table in tables:
        data = []
        my_data =[]
        trs = table.find_all("tr")[0]
        td = trs.find("td")
        print(td.text)
        tr_tags = table.find_all("tr")[2:]
        for tr_tag in tr_tags:
            td_tags = tr_tag.find_all("td")
            for td in td_tags:
                data.append(td.text)

        my_data = [data[x:x+4] for x in range(0, len(data),4)]
        if my_data != [] :
            print(tabulate(my_data,headers=headers,tablefmt = "fancy_grid"))
        else:
            break
def tournaments(soup):
    """" To Fetch tournament info from the soup object """

    data = []
    my_data =[]
    headers = ["Event Name", "City","Federation","Start", "End"]
    table = soup.find("table",{"align":"center"})
    tr_tags = table.find_all("tr")[2:]
    for tr_tag in tr_tags:
        td_tags = tr_tag.find_all("td")[2:]
        for td in td_tags:
            data.append(td.text)

    my_data = [data[x:x+5] for x in range(0, len(data),5)]
    print(tabulate(my_data,headers=headers,tablefmt = "fancy_grid"))

def ratings(soup):
    data = []
    my_data =[]
    headers = ["Rank", "Name"]
    #headers = ["Rank", "Name", "Title","Country","Rating", "Games", "B-Year"]
    atags = soup.find_all("a", {"class":"tur"})
    for count,atag in enumerate(atags,1):
        data.append([count,atag.text])

    print(tabulate(data,headers=headers,tablefmt = "fancy_grid"))


def f(catg):
    """ Function to return categories based on catg """
    return {
            '1': 'men',
            '2': 'women',
            '3': 'juniors',
            '4': 'girls'
    }[catg]

def main():

    print(Choice)
    choice = input("Enter your choice!")

    while choice not in ["1","2","3"]:
        print("Wrong choice! Please enter a valid choice!")
        choice = input("Enter your choice!")

    if choice == "1":
        url = 'https://www.fide.com/calendar/fide-calendar.html'
        soup = scrape(url)
        fide_events(soup)

    if choice == "2":
        url = 'https://ratings.fide.com/tournament_list.phtml'
        soup = scrape(url)
        tournaments(soup)

    if choice == "3":
        print(Modes)
        mode = input("Enter your choice!")

        while mode not in ["1","2","3"]:
            print("Wrong choice! Please enter a valid choice!")
            mode = input("Enter your choice!")
        print(Categories)
        catg = input("Enter your choice!")

        while catg not in ["1","2","3","4"]:
            print("Wrong choice! Please enter a valid choice!")
            catg = input("Enter your choice!")

        string = ""

        if mode == "1":
            string = f(catg)
        if mode == "2":
            string = str(f(catg)) + "_rapid"
        if mode == "3":
            string = str(f(catg)) + "_blitz"

        url = 'https://ratings.fide.com/top.phtml?list={}'.format(string)
        soup = scrape(url)
        ratings(soup)


if __name__ == '__main__':
    main()
