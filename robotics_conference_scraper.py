from bs4 import BeautifulSoup
import requests
import seaborn as sb
import pandas as pd
import matplotlib.pyplot as plt

#### ROBOSOFT 2024 ####

# daily_programs = [
#     "https://ras.papercept.net/conferences/conferences/ROSO24/program/ROSO24_ContentListWeb_2.html",
#     "https://ras.papercept.net/conferences/conferences/ROSO24/program/ROSO24_ContentListWeb_3.html",
#     "https://ras.papercept.net/conferences/conferences/ROSO24/program/ROSO24_ContentListWeb_4.html",
# ]

# keyword_indx = "https://ras.papercept.net/conferences/conferences/ROSO24/program/ROSO24_KeywordIndexWeb.html"

#### ICRA 2024 ####

daily_programs = [
    "https://ras.papercept.net/conferences/conferences/ICRA24/program/ICRA24_ContentListWeb_1.html",
    "https://ras.papercept.net/conferences/conferences/ICRA24/program/ICRA24_ContentListWeb_2.html",
    "https://ras.papercept.net/conferences/conferences/ICRA24/program/ICRA24_ContentListWeb_3.html",
]

keyword_indx = "https://ras.papercept.net/conferences/conferences/ICRA24/program/ICRA24_KeywordIndexWeb.html"

author_indx = "https://ras.papercept.net/conferences/conferences/ICRA24/program/ICRA24_AuthorIndexWeb.html"


# Unfortunately, uni names are not uniquely identified. I perform a coarse search to eliminate ambiguity. Note that the results are not 100% correct of course.
def clean_university_list(unis):

    for i, item in enumerate(unis):
        if (
            "Technical University of Munich" in item
            or "TU Munich" in item
            or "Technische Universität München" in item
            or "(TUM)" in item
            or item == "TUM"
        ):
            unis[i] = "Technical University of Munich"
        if "ETH" in item:
            unis[i] = "ETH Zurich"
        if "University of California" in item or "UC Berkeley" in item:
            unis[i] = "UC Berkeley"
        if (
            "The Hong Kong University of Science and Technology" in item
            or "Hong Kong University of Science and Technology" in item
        ):
            unis[i] = "The Hong Kong University of Science and Technology"
        if "(CMU)" in item or item == "CMU":
            unis[i] = "Carnegie Mellon University"
        if "Zhejiang University" in item:
            unis[i] = "Zhejiang University"
        if "Shanghai Jiao Tong University" in item:
            unis[i] = "Shanghai Jiao Tong University"
        if "Seoul National University" in item:
            unis[i] = "Seoul National University"
        if (
            "Massachusetts Institute of Technology" in item
            or "(MIT)" in item
            or item == "MIT"
        ):
            unis[i] = "Massachusetts Institute of Technology"
        if "Stanford University" in item:
            unis[i] = "Stanford University"
        if (
            "Chinese University of Hong Kong" in item
            or "The Chinese University of Hong Kong" in item
        ):
            unis[i] = "The Chinese University of Hong Kong"
        if "The University of Tokyo" in item or "University of Tokyo" in item:
            unis[i] = "The University of Tokyo"
        if "Beijing University of Technology" in item:
            unis[i] = "Beijing University of Technology"
        if "Imperial College" in item or "Imperial College London" in item:
            unis[i] = "Imperial College London"
        if "Beihang University" in item:
            unis[i] = "Beihang University"
        if "University of Oxford" in item or "Oxford University" in item:
            unis[i] = "University of Oxford"
        if (
            "Karlsruhe Institute of Technology" in item
            or "(KIT)" in item
            or item == "KIT"
        ):
            unis[i] = "Karlsruhe Institute of Technology"
        if "RWTH" in item or "RWTH Aachen" in item:
            unis[i] = "RWTH Aachen"
        if "Peking University" in item:
            unis[i] = "Peking University"
        if (
            "NTNU - Norwegian University of Science and Technology" in item
            or "NTNU" in item
            or "Norwegian University of Science and Technology" in item
        ):
            unis[i] = "Norwegian University of Science and Technology"
        if "EPFL" in item or "École Polytechnique Fédérale De Lausanne" in item or "Swiss Federal Institute of Technology" in item:
            unis[i] = "École Polytechnique Fédérale De Lausanne (EPFL)"
        if "TU Delft" in item or "Delft University of Technology" in item:
            unis[i] = "Delft University of Technology"
        if "Harbin Institute of Technology" in item:
            unis[i] = "Harbin Institute of Technology"

    return unis


# NOTE I am using the daily program to get the list of contributors. This also includes program chairs and co-chairs. I found that the information under author_index does the same thing.
def get_university_contributors_list():
    university_list, contributors_list = [], []
    for daily_program in daily_programs:

        response = requests.get(daily_program)

        soup = BeautifulSoup(response.content, "html.parser")

        # Find all anchor tags (<a>) with the text "Click to go to the Author Index"
        contributions = soup.find_all("a", {"title": "Click to go to the Author Index"})

        university_list += [
            contribution.parent.findNext("td").text.strip()
            for contribution in contributions
        ]
        contributors_list += [
            contribution.text.strip() for contribution in contributions
        ]

    return clean_university_list(university_list), contributors_list


def get_keywords_list():
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
    sb.set_theme(rc={"figure.figsize": (15, 8.27)})
    sb.set(font_scale=1.3)
    ax = sb.countplot(
        y=list,
        order=pd.Series(list).value_counts().iloc[:15].index,
        color="#485fc7",
        orient="h",
    )
    ax.set_xlabel(xlabel)
    ax.set_title(title, fontsize=20, fontweight="bold", x=0.4, y=1.03)
    ax.get_figure().savefig(filename, bbox_inches="tight")
    plt.clf()


university_list, contributors_list = get_university_contributors_list()
keywords_list = get_keywords_list()


plot(
    university_list,
    "Top 15 Institutions by Contributions",
    "Number of Contributions",
    "university_contributions.png",
)

plot(
    contributors_list,
    "Top 15 Authors by Contributions",
    "Number of Contributions",
    "authors_contribution.png",
)

plot(
    keywords_list,
    "Top 15 Keywords by Contributions",
    "Number of Contributions",
    "keywords_contributions.png",
)
