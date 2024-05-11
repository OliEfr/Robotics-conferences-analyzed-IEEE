from bs4 import BeautifulSoup
import requests


daily_programs = [
    "https://ras.papercept.net/conferences/conferences/ICRA24/program/ICRA24_ContentListWeb_1.html",
    "https://ras.papercept.net/conferences/conferences/ICRA24/program/ICRA24_ContentListWeb_2.html",
    "https://ras.papercept.net/conferences/conferences/ICRA24/program/ICRA24_ContentListWeb_3.html",
]

author_indx = [
    "https://ras.papercept.net/conferences/conferences/ICRA24/program/ICRA24_AuthorIndexWeb.html"
]

keyword_indx = [
    "https://ras.papercept.net/conferences/conferences/ICRA24/program/ICRA24_KeywordIndexWeb.html"
]

# NOTE I am using the daily program to get the list of contributors. There is alternatively the author_index page that is more accurate.
def get_university_contributors_list():
    university_list, contributors_list = [], []
    for daily_program in daily_programs:

        response = requests.get(daily_program)

        soup = BeautifulSoup(response.content, "html.parser")

        # Find all anchor tags (<a>) with the text "Click to go to the Author Index"
        contributions = soup.find_all(
            "a", {"title": "Click to go to the Author Index"}
        )

        university_list += [
            contribution.parent.findNext("td").text.strip()
            for contribution in contributions
        ]
        contributors_list += [
            contribution.text.strip()
            for contribution in contributions
        ]

    return university_list, contributors_list


university_list, contributors_list = get_university_contributors_list()
print(contributors_list.count("Levine, Sergey"))
print(contributors_list.count("Abbeel, Pieter"))
print(contributors_list.count("Haddadin, Sami"))

