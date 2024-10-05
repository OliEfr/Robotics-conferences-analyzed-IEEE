from bs4 import BeautifulSoup
import requests
import seaborn as sb
import pandas as pd
import matplotlib.pyplot as plt
import pickle

#### 2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)
conference = "IROS 2024"
daily_programs = [
    "https://ras.papercept.net/conferences/conferences/IROS24/program/IROS24_ContentListWeb_1.html",
    "https://ras.papercept.net/conferences/conferences/IROS24/program/IROS24_ContentListWeb_2.html",
    "https://ras.papercept.net/conferences/conferences/IROS24/program/IROS24_ContentListWeb_3.html",
    "https://ras.papercept.net/conferences/conferences/IROS24/program/IROS24_ContentListWeb_4.html",
    "https://ras.papercept.net/conferences/conferences/IROS24/program/IROS24_ContentListWeb_5.html",
]
keyword_indx = "https://ras.papercept.net/conferences/conferences/IROS24/program/IROS24_KeywordIndexWeb.html"

#### 40th Anniversary of the IEEE Conference on Robotics and Automation (ICRA@40)
# conference = "ICRA@40 2024"
# daily_programs = [
#     "https://ras.papercept.net/conferences/conferences/ICRAX24/program/ICRAX24_ContentListWeb_1.html",
#     "https://ras.papercept.net/conferences/conferences/ICRAX24/program/ICRAX24_ContentListWeb_2.html",
#     "https://ras.papercept.net/conferences/conferences/ICRAX24/program/ICRAX24_ContentListWeb_3.html",
#     "https://ras.papercept.net/conferences/conferences/ICRAX24/program/ICRAX24_ContentListWeb_4.html",
# ]
# keyword_indx = "https://ras.papercept.net/conferences/conferences/ICRAX24/program/ICRAX24_KeywordIndexWeb.html"

#### 2024 33rd IEEE International Conference on Robot and Human Interactive Communication (ROMAN)
# conference = " International Conference on Robot and Human Interactive Communication (ROMAN)"
# daily_programs = [
#     "https://ras.papercept.net/conferences/conferences/ROMAN24/program/ROMAN24_ContentListWeb_1.html",
#     "https://ras.papercept.net/conferences/conferences/ROMAN24/program/ROMAN24_ContentListWeb_2.html",
#     "https://ras.papercept.net/conferences/conferences/ROMAN24/program/ROMAN24_ContentListWeb_3.html",
#     "https://ras.papercept.net/conferences/conferences/ROMAN24/program/ROMAN24_ContentListWeb_4.html",
#     "https://ras.papercept.net/conferences/conferences/ROMAN24/program/ROMAN24_ContentListWeb_5.html",
# ]
# keyword_indx = "https://ras.papercept.net/conferences/conferences/ROMAN24/program/ROMAN24_KeywordIndexWeb.html"

#### 2024 IEEE International Conference on Cybernetics and Intelligent Systems (CIS) and IEEE International Conference on Robotics, Automation and Mechatronics (RAM)
# conference = "CIS and RAM"
# daily_programs = [
#     "https://ras.papercept.net/conferences/conferences/CISRAM24/program/CISRAM24_ContentListWeb_2.html",
#     "https://ras.papercept.net/conferences/conferences/CISRAM24/program/CISRAM24_ContentListWeb_3.html",
#     "https://ras.papercept.net/conferences/conferences/CISRAM24/program/CISRAM24_ContentListWeb_4.html",
# ]
# keyword_indx = "https://ras.papercept.net/conferences/conferences/CISRAM24/program/CISRAM24_KeywordIndexWeb.html"

#### 2024 IEEE International Conference on Advanced Intelligent Mechatronics (AIM)
# conference = "International Conference on Advanced Intelligent Mechatronics (AIM)"
# daily_programs = [
#     "https://ras.papercept.net/conferences/conferences/AIM24/program/AIM24_ContentListWeb_2.html",
#     "https://ras.papercept.net/conferences/conferences/AIM24/program/AIM24_ContentListWeb_3.html",
#     "https://ras.papercept.net/conferences/conferences/AIM24/program/AIM24_ContentListWeb_4.html",
# ]
# keyword_indx = "https://ras.papercept.net/conferences/conferences/AIM24/program/AIM24_KeywordIndexWeb.html"

#### 2024 IEEE 20th International Conference on Automation Science and Engineering (CASE)
# conference = (
#     "International Conference on Automation Science and Engineering (CASE)"
# )
# daily_programs = [
#     "https://ras.papercept.net/conferences/conferences/CASE24/program/CASE24_ContentListWeb_2.html",
#     "https://ras.papercept.net/conferences/conferences/CASE24/program/CASE24_ContentListWeb_3.html",
#     "https://ras.papercept.net/conferences/conferences/CASE24/program/CASE24_ContentListWeb_4.html",
# ]
# keyword_indx = "https://ras.papercept.net/conferences/conferences/CASE24/program/CASE24_KeywordIndexWeb.html"


#### International Conference on Ubiquitous Robots (UR) 2024 ####
# conference = "International Conference on Ubiquitous Robots (UR) 2024"
# daily_programs = [
#     "https://ras.papercept.net/conferences/conferences/UR24/program/UR24_ContentListWeb_2.html",
#     "https://ras.papercept.net/conferences/conferences/UR24/program/UR24_ContentListWeb_3.html",
# ]
# keyword_indx = "https://ras.papercept.net/conferences/conferences/UR24/program/UR24_KeywordIndexWeb.html"

#### ARSO 2024 ####
# ARSO website looks a bit different
# TODO implement parsing
# conference = "ARSO_2024"
# daily_programs = [
#     "https://ras.papercept.net/conferences/conferences/ARSO24/program/ARSO24_ContentListWeb_1.html",
#     "https://ras.papercept.net/conferences/conferences/ARSO24/program/ARSO24_ContentListWeb_2.html",
#     "https://ras.papercept.net/conferences/conferences/ARSO24/program/ARSO24_ContentListWeb_3.html",
# ]
# keyword_indx = "https://ras.papercept.net/conferences/conferences/ARSO24/program/ARSO24_KeywordIndexWeb.html"

#### ROBOSOFT 2024 ####
# conference = "ROBOSOFT_2024"
# daily_programs = [
#     "https://ras.papercept.net/conferences/conferences/ROSO24/program/ROSO24_ContentListWeb_2.html",
#     "https://ras.papercept.net/conferences/conferences/ROSO24/program/ROSO24_ContentListWeb_3.html",
#     "https://ras.papercept.net/conferences/conferences/ROSO24/program/ROSO24_ContentListWeb_4.html",
# ]
# keyword_indx = "https://ras.papercept.net/conferences/conferences/ROSO24/program/ROSO24_KeywordIndexWeb.html"

#### ICRA 2024 ####
# conference = "ICRA_2024"
# daily_programs = [
#     "https://ras.papercept.net/conferences/conferences/ICRA24/program/ICRA24_ContentListWeb_1.html",
#     "https://ras.papercept.net/conferences/conferences/ICRA24/program/ICRA24_ContentListWeb_2.html",
#     "https://ras.papercept.net/conferences/conferences/ICRA24/program/ICRA24_ContentListWeb_3.html",
# ]
# keyword_indx = "https://ras.papercept.net/conferences/conferences/ICRA24/program/ICRA24_KeywordIndexWeb.html"


# Unfortunately, institution names are not unique.
# I perform a coarse search to eliminate ambiguity for the most popular unis.
def remove_university_name_ambiguity(unis):

    scraped_unis = unis
    unis = []

    for i, item in enumerate(scraped_unis):
        if (
            "Technical University of Munich" in item
            or "TU Munich" in item
            or "Technische Universität München" in item
            or "(TUM)" in item
            or item == "TUM"  # check equality
        ):
            unis.append("Technical University of Munich")
        if "ETH" in item:
            unis.append("ETH Zurich")
        if "University of California" in item or "UC Berkeley" in item:
            unis.append("UC Berkeley")
        if (
            "The Hong Kong University of Science and Technology" in item
            or "Hong Kong University of Science and Technology" in item
        ):
            unis.append("The Hong Kong University of Science and Technology")
        if "(CMU)" in item or item == "CMU":  # check equality
            unis.append("Carnegie Mellon University")
        if "Zhejiang University" in item:
            unis.append("Zhejiang University")
        if (
            "Shanghai Jiao Tong University" in item
            or "Shanghai Jiaotong Universit" in item
        ):
            unis.append("Shanghai Jiao Tong University")
        if "Seoul National University" in item:
            unis.append("Seoul National University")
        if (
            "Massachusetts Institute of Technology" in item
            or "(MIT)" in item
            or item == "MIT"  # check equality
        ):
            unis.append("Massachusetts Institute of Technology")
        if "Stanford University" in item:
            unis.append("Stanford University")
        if (
            "Chinese University of Hong Kong" in item
            or "The Chinese University of Hong Kong" in item
        ):
            unis.append("The Chinese University of Hong Kong")
        if "The University of Tokyo" in item or "University of Tokyo" in item:
            unis.append("The University of Tokyo")
        if "Beijing University of Technology" in item:
            unis.append("Beijing University of Technology")
        if "Imperial College" in item or "Imperial College London" in item:
            unis.append("Imperial College London")
        if "Beihang University" in item or "BEIHANG UNIVERSITY" in item:
            unis.append("Beihang University")
        if "University of Oxford" in item or "Oxford University" in item:
            unis.append("University of Oxford")
        if (
            "Karlsruhe Institute of Technology" in item
            or "(KIT)" in item
            or item == "KIT"  # check equality
        ):
            unis.append("Karlsruhe Institute of Technology")
        if "RWTH" in item or "RWTH Aachen" in item:
            unis.append("RWTH Aachen")
        if "Peking University" in item:
            unis.append("Peking University")
        if (
            "NTNU - Norwegian University of Science and Technology" in item
            or "NTNU" in item
            or "Norwegian University of Science and Technology" in item
        ):
            unis.append("Norwegian University of Science and Technology")
        if (
            "EPFL" in item
            or "École Polytechnique Fédérale De Lausanne" in item
            or "Swiss Federal Institute of Technology" in item
        ):
            unis.append("École Polytechnique Fédérale De Lausanne (EPFL)")
        if "TU Delft" in item or "Delft University of Technology" in item:
            unis.append("Delft University of Technology")
        if "Harbin Institute of Technology" in item:
            unis.append("Harbin Institute of Technology")
        if "University of Illinois" in item:
            unis.append("University of Illinois")
        if "inria" in item.lower():
            unis.append("INRIA")
        if "German Aerospace Center" in item or "(DLR)" in item:
            unis.append("German Aerospace Center (DLR)")
        if "University of Hamburg" in item or "Uni Hamburg" in item or "Hamburg University" in item:
            unis.append("University of Hamburg")
        if "University of Twente" in item:
            unis.append("University of Twente")
        if "Idiap Research Institute" in item:
            unis.append("Idiap Research Institute")
        if "Lulea University of Technology" in item or "Luleå University of Technology" in item:
            unis.append("Luleå University of Technology")

    return unis


# I am using the daily program to get the list of contributors.
# This includes program chairs and co-chairs.
# The information under .../ICRA24_AuthorIndexWeb.html does the same thing.
# This counts EACH contributor of EACH paper.
# This function is LEGACY
def get_university_contributors_list():
    university_list, contributors_list = [], []
    for daily_program in daily_programs:

        response = requests.get(daily_program)
        soup = BeautifulSoup(response.content, "html.parser")

        with open(
            f'./output/scraped_html/{daily_program.replace("/", "_").replace(":", "_")}',
            mode="wt",
            encoding="utf-8",
        ) as file:
            file.write(soup.prettify())

        # Find all anchor tags (<a>) with the text "Click to go to the Author Index"
        contributions = soup.find_all(
            "a", {"title": "Click to go to the Author Index"}
        )

        university_list += [
            contribution.parent.findNext("td").text.strip()
            for contribution in contributions
        ]
        contributors_list += [
            contribution.text.strip() for contribution in contributions
        ]

    return remove_university_name_ambiguity(university_list), contributors_list


# Gets list of contributors and universities ONLY for papers (no chairs and co-chairs)
# For each paper, each distinct university is only counted ONCE
def get_university_contributors_list_papers_adjusted():
    university_list, contributors_list = [], []
    for daily_program in daily_programs:

        response = requests.get(daily_program)
        soup = BeautifulSoup(response.content, "html.parser")

        with open(
            f'./output/scraped_html/{daily_program.replace("/", "_").replace(":", "_")}',
            mode="wt",
            encoding="utf-8",
        ) as file:
            file.write(soup.prettify())

        # get all papers
        papers = soup.find_all("span", {"class": "pTtl"})

        # get all authors for each paper
        for paper in papers:
            paper_contributors = []
            paper_universities = []

            # get high level DOM element of paper
            paper_tr = paper.parent.parent

            # iterate through next siblings
            element = paper_tr
            while True:

                element = element.next_sibling

                # empty element
                if element == "\n":
                    continue

                # reached end of table == reached end of 'session'
                if element == None:
                    break

                # reached next paper
                new_paper = element.find_all("span", {"class": "pTtl"})
                if len(new_paper) > 0:
                    break

                # author in element
                authors = element.find_all(
                    "a", {"title": "Click to go to the Author Index"}
                )
                # add contributors and universities
                if len(authors) > 0:
                    author = authors[0]
                    paper_contributors.append(author.text.strip())
                    paper_universities.append(
                        author.parent.findNext("td").text.strip()
                    )
                elif len(authors) > 1:
                    print(
                        "Find more than one author in a single tr element. This is unexpected."
                    )
                else:
                    pass

            paper_universities = remove_university_name_ambiguity(
                paper_universities
            )
            # extend only *unique* university names!
            university_list.extend(list(set(paper_universities)))
            contributors_list.extend(paper_contributors)

    return remove_university_name_ambiguity(university_list), contributors_list


def get_keywords_list():
    keywords_list = []

    response = requests.get(keyword_indx)
    soup = BeautifulSoup(response.content, "html.parser")

    with open(
        f'./output/scraped_html/{keyword_indx.replace("/", "_").replace(":", "_")}',
        mode="wt",
        encoding="utf-8",
    ) as file:
        file.write(soup.prettify())

    # get all rows of the table
    rows = soup.find("table", {"class": "kT"}).find_all("tr")
    for row in rows:
        # elements we look for have no attribute
        if bool(row.attrs):
            continue
        else:
            links = row.find_all("a")
            # this is dirty but makes it compatible with the data structures for
            # university_list and contributors_list
            for _ in range(1, len(links)):
                keywords_list.append(links[0].text.strip())

    return keywords_list


def plot(list, title, xlabel, filename):
    sb.set(font_scale=1.3)
    ax = sb.countplot(
        y=list,
        order=pd.Series(list).value_counts().iloc[:15].index,
        color="#485fc7",
        orient="h",
    )
    ax.figure.set_size_inches(20, 8.75)
    ax.set_xlabel(xlabel)
    ax.set_title(title, fontweight="bold", x=0.35, y=1.03)
    plt.gcf().subplots_adjust(left=0.35, right=0.99)
    ax.get_figure().savefig(filename)
    plt.clf()


university_list, contributors_list = (
    get_university_contributors_list_papers_adjusted()
)
keywords_list = get_keywords_list()

# saving .pkl is suboptimal for git, but its quick for now
with open(f"./output/{conference}_data.pkl", "wb") as f:
    pickle.dump(
        {
            "university_list": university_list,
            "contributors_list": contributors_list,
            "keywords_list": keywords_list,
        },
        f,
    )

plot(
    university_list,
    "Top 15 Institutions by Authorships",
    "Number of Authorships",
    f"./output/university_contributions_{conference}.svg",
)

plot(
    contributors_list,
    "Top 15 Authors by Authorships",
    "Number of Authorships",
    f"./output/authors_contributions_{conference}.svg",
)

plot(
    keywords_list,
    "Top 15 Keywords by Contributions",
    "Number of Contributions",
    f"./output/keywords_contributions_{conference}.svg",
)
