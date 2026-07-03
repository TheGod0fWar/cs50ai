import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    transition = {}
    if corpus[page]:
        i = len(corpus[page])

        print("i", i)
        d_factor = damping_factor / i
        print("d", d_factor)
        rest_factor = (1 - damping_factor) / len(corpus)
        print("rest", rest_factor)

        for site in corpus:
            transition[site] = rest_factor

        for obj in corpus[page]:
            print("obj", obj)
            transition[obj] += d_factor

        return transition
    else:
        factor = 1 / len(corpus)
        for obj in corpus:
            transition[obj] = factor
        return transition

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.
    """
    new_page = random.choice(list(corpus.keys()))
    result = {}

    for _ in range(n):
        # HIER IST DIE TRICKREICHE STELLE: 
        # In jeder Runde die Listen frisch leeren, damit das alte Gedächtnis gelöscht wird!
        pages = []
        weight = []
        
        rank = transition_model(corpus, new_page, damping_factor)
        for key, value in rank.items():
            pages.append(key)
            weight.append(value)

        # Wählt die nächste Seite basierend NUR auf den aktuellen Gewichten
        new_page = random.choices(pages, weights=weight, k=1)[0]
        
        # Zählen für das Endergebnis
        if new_page not in result:
            result[new_page] = 1 / n
        else:
            result[new_page] += 1 / n

    return result


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result = {}
    N = len(corpus.keys())
    for page in corpus:
        result[page] = 1 / N

    while True:
        new_rank = {}
        for p in corpus:
            basis = (1 - damping_factor) / N

            link_summe = 0

            for i in corpus:
                if p in corpus[i]:
                    links = len(corpus[i])
                    link_summe += result[i] / links
                elif len(corpus[i]) == 0:
                    link_summe += result[i] / N
            new_rank[p] = basis + (link_summe * damping_factor)

        konvergiert = True

        for page in corpus:
            diffrence = abs(new_rank[page] - result[page])
            if diffrence >= 0.001:
                konvergiert = False
        result = new_rank

        if konvergiert:
            break

    return result


if __name__ == "__main__":
    main()
