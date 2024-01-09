from urllib.request import urlopen
import xml.etree.ElementTree as ET
import argparse


def fetch_papers(url):
    """Fetches papers from the arXiv API and returns abstracts as a list of strings."""
    response = urlopen(url)  # urllib.request.
    data = response.read().decode("utf-8")
    root = ET.fromstring(data)
    print(f"> fetched papers from '{url}'")

    papers_list = []
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
        paper_info = f"Title: {title}\nSummary: {summary}\n"
        papers_list.append(paper_info)
    return papers_list


def save_papers(papers_list, path_to_papers):
    with open(path_to_papers, "w") as txt:
        for paper in papers_list:
            txt.write(f"{paper}\n")
    print(f"> saved plain text papers to '{path_to_papers}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        type=str,
        help="link to arxiv query",
        nargs="?",
        default="http://export.arxiv.org/api/query?search_query=ti:llama&start=0&max_results=70",
    )
    parser.add_argument(
        "--out",
        type=str,
        help="output directory to save the plain text paper summaries to",
        nargs="?",
        default="./data/papers.txt",
    )
    args = parser.parse_args()

    papers_list = fetch_papers(url=args.url)
    save_papers(papers_list=papers_list, path_to_papers=args.out)
