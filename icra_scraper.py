from bs4 import BeautifulSoup
import requests
import seaborn as sb
import pandas as pd


daily_programs = [
    "https://ras.papercept.net/conferences/conferences/ICRA24/program/ICRA24_ContentListWeb_1.html",
    "https://ras.papercept.net/conferences/conferences/ICRA24/program/ICRA24_ContentListWeb_2.html",
    "https://ras.papercept.net/conferences/conferences/ICRA24/program/ICRA24_ContentListWeb_3.html",
]

author_indx = "https://ras.papercept.net/conferences/conferences/ICRA24/program/ICRA24_AuthorIndexWeb.html"


keyword_indx = "https://ras.papercept.net/conferences/conferences/ICRA24/program/ICRA24_KeywordIndexWeb.html"

# NOTE I am using the daily program to get the list of contributors. This also includes program chairs and co-chairs. I found that the information under author_index does the same thing.
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

def get_keywords_dict():
    keywords_list = []

    response = requests.get(keyword_indx)
    soup = BeautifulSoup(response.content, "html.parser")
    # get all rows of table
    rows = soup.find("table", {"class": "kT"}).find_all("tr")
    for row in rows:
        # elements we look for have no attribute
        if bool(row.attrs):
            continue
        else:
            as_ = row.find_all("a")
            # this is dirty but it makes it compatible with the data structures for authors and institutions
            for _ in range(1, len(as_)):
                keywords_list.append(as_[0].text.strip())

    return keywords_list

def plot(list, title, xlabel, filename):
    sb.set_theme(rc={'figure.figsize':(15,8.27)})
    sb.set(font_scale=1.3) 
    ax = sb.countplot(y=list, order=pd.Series(list).value_counts().iloc[:15].index, color="#485fc7", orient="h")
    ax.set_xlabel(xlabel)
    ax.set_title(title, fontsize=20, fontweight='bold', x=.4, y=1.03)
    ax.get_figure().savefig(filename ,bbox_inches='tight')

university_list, contributors_list = get_university_contributors_list()
keywords_list = get_keywords_dict()




plot(university_list, "Top 15 Institutions by Contributions", "Number of Contributions", "university_contributors.png")

plot(contributors_list, "Top 15 Authors by Contributions", "Number of Contributions", "authors_contributors.png")

plot(keywords_list, "Top 15 Keywords by Contributions", "Number of Contributions", "keywords_contributors.png")