from bs4 import BeautifulSoup
import requests
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from institutions_synonyms import *
from rig_partners import AFFILIATION_SYNONYMS

plot_n_top = 15

#### 2025 IEEE International Conference on Robotics and Automation (ICRA)
conference = "ICRA 2025"
daily_programs = [
    "https://ras.papercept.net/conferences/conferences/ICRA25/program/ICRA25_ContentListWeb_1.html",
    "https://ras.papercept.net/conferences/conferences/ICRA25/program/ICRA25_ContentListWeb_2.html",
    "https://ras.papercept.net/conferences/conferences/ICRA25/program/ICRA25_ContentListWeb_3.html"    
    
]
keyword_indx = "https://ras.papercept.net/conferences/conferences/ICRA25/program/ICRA25_KeywordIndexWeb.html"


def normalize_names(unis):
    normalized = []
    for raw in unis:
        raw_norm = raw.strip()
        hit = None
        for key, matchers in AFFILIATION_SYNONYMS.items():
            # stop at the first matcher that returns True
            if any(fn(raw_norm) for fn in matchers):
                # print(raw_norm)
                hit = key
                break
        normalized.append(hit if hit is not None else raw_norm)
    return normalized


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
                # print(new_paper)
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

            paper_universities = normalize_names(
                paper_universities
            )
            # extend only *unique* university names!
            university_list.append(list(set(paper_universities)))
            contributors_list.append(paper_contributors)

    return university_list, contributors_list



def plot(list, title, xlabel, filename):
    sb.set(font_scale=1.3)
    ax = sb.countplot(
        y=list,
        order=pd.Series(list).value_counts().iloc[:plot_n_top].index,
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


def count_rig_papers(university_list):

    # The set of canonical RIG keys, e.g. {"TUM", "KIT", ...}
    rig_keys = set(AFFILIATION_SYNONYMS.keys())

    count = 0
    for paper_unis in university_list:
        # If any normalized affiliation is one of our RIG keys, count this paper
        if any(aff in rig_keys for aff in paper_unis):
            count += 1
        else:
            pass
            # print(paper_unis)

    return count

print("RIG has contributed to {0} out of {1} papers at ICRA25".format(count_rig_papers(university_list), len(university_list)))

def count_papers_per_partner(university_list):

    # Initialize counts for every RIG partner to zero
    counts = {key: 0 for key in AFFILIATION_SYNONYMS.keys()}

    for paper_keys in university_list:
        for univ in paper_keys:
            if univ in counts:
                counts[univ] += 1

    return counts

partner_counts = count_papers_per_partner(university_list)

# Print results
total = 0
for partner, cnt in partner_counts.items():
    print(f"{partner}: {cnt}")
    total += cnt

print(total)


def plot_partner_counts_horizontal(partner_counts):
    """
    Create a horizontal seaborn bar plot of number of papers per RIG partner.

    Parameters
    ----------
    partner_counts : dict[str, int]
        Mapping from RIG partner key to the number of papers they appear in.
    """
    # Prepare data sorted by count descending
    partners = sorted(partner_counts, key=lambda k: partner_counts[k], reverse=True)
    counts = [partner_counts[p] for p in partners]

    # Set a clean whitegrid theme
    sns.set_theme(style="whitegrid")
    sns.set_color_codes("pastel")

    plt.figure(figsize=(8, 10))
    sns.barplot(x=counts, y=partners, orient="h")  # horizontal bars
    plt.xlabel("Number of Papers")
    plt.ylabel("RIG Partner")
    # plt.title("Number of Papers per RIG Partner")
    plt.tight_layout()
    plt.savefig("RIGatICRA.png")
    plt.show()

plot_partner_counts_horizontal(partner_counts)