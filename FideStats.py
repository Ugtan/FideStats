""" A Python script to find the Fide Events, Tournaments, and Ratings from fide.com"""

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd

Choice ={
          "1": "Fide Events",
          "2": "Tournaments",
          "3": "Ratings"
}

Events = {
            "0": "World Events",
            "1": "European Events",
            "2": "American Zonals",
            "3": "American Events",
            "4": "Asian Events",
            "5": "African Zonals",
            "6": "African Events",
            "7": "Arab Events",
            "8": "Presidential Board / Congress",
            "9": "Other Official Events"

}
Categories = {
                "1": "Top 20 Players",
                "2": "Top 20 Women",
                "3": "Top 20 Juniors",
                "4": "Top 20 Girls"
             }

Variant = {
           "1": "Standard",
           "2": "Rapid",
           "3": "blitz"
        }


def fide_events(soup, event):
    """ To Fetch Fide Events from fide_events"""
    headers = ["Name", "Place", "Start", "End"]
    print("\n\t" + event + "\n")
    data = []
    my_data =[]

    tables = soup.find_all("table",{"align":"center"})[1:]
    for table in tables:
        if str(table.find_all("tr")[0].find("td").text).strip() == str(event):
            tr_tags = table.find_all("tr")[2:]
            for tr_tag in tr_tags:
                td_tags = tr_tag.find_all("td")
                for td in td_tags:
                    data.append(td.text)
            my_data = [data[x:x+4] for x in range(0, len(data),4)]
            print(tabulate(my_data,headers=headers,tablefmt = "fancy_grid"))
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
    """ To get the ratings of top players """
    data = []
    my_data =[]
    headers = ["Rank", "Name"]
    atags = soup.find_all("a", {"class":"tur"})
    for count,atag in enumerate(atags,1):
        if len(data) != 20:
            data.append([count,atag.text])
    print(tabulate(data,headers=headers,tablefmt = "fancy_grid"))

def scrape(url):
    """ To fetch info from the urls """
    response = requests.get(url)
    soup = BeautifulSoup(response.text , "html.parser")
    return soup


def f(catg):
    """ Function to return categories based on catg """
    return {
            '1': 'men',
            '2': 'women',
            '3': 'juniors',
            '4': 'girls'
    }[catg]


def main():

    for i, j in sorted(Choice.items()):
        print(i, j)

    choice = input("\nEnter your choice: ")

    while choice not in map(str, range(4)):
        choice = input("\nWrong choice! Please enter a valid choice! ")

    if choice == "1":
        url = 'https://www.fide.com/calendar/fide-calendar.html'
        soup = scrape(url)
        for i, j in sorted(Events.items()):
            print(i, j)
        event = input("\nEnter your choice! ")

        while event not in map(str, range(10)):
            event = input("\nWrong choice! Please enter a valid choice! ")
        fide_events(soup,Events[event])

    if choice == "2":
        url = 'https://ratings.fide.com/tournament_list.phtml'
        soup = scrape(url)
        tournaments(soup)

    if choice == "3":
        for i, j in sorted(Variant.items()):
            print(i, j)

        variant = input("\nEnter your choice! ")
        while variant not in map(str, range(4)):
            variant = input("\nWrong choice! Please enter a valid choice! ")

        for i, j in sorted(Categories.items()):
            print(i, j)

        catg = input("\nEnter your choice! ")
        while catg not in map(str, range(5)):
            catg = input("\nWrong choice! Please enter a valid choice! ")

        string = ""

        if variant == "1":
            string = f(catg)
        if variant == "2":
            string = str(f(catg)) + "_rapid"
        if variant == "3":
            string = str(f(catg)) + "_blitz"

        url = 'https://ratings.fide.com/top.phtml?list={}'.format(string)
        soup = scrape(url)
        ratings(soup)


if __name__ == '__main__':
    main()
