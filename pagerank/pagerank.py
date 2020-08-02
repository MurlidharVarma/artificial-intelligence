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
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # initialize the probability distribution to blank
    prob_dist = {}

    # total pages in corpus
    total_pages_count = len(corpus)

    # number of linked page to current page
    linked_pages_count = len(corpus[page])

    # If there are no links in the current page, then do equal distribution
    if linked_pages_count == 0:
        random_page_prob = 1 / total_pages_count
        linked_page_prob = 0
    else:
        random_page_prob = (1-damping_factor) / total_pages_count
        linked_page_prob = damping_factor / linked_pages_count
    
    # Iterate through each page in corpus, and calculate the probability
    for pg in list(corpus):
        # default probability to random page probability
        prob = random_page_prob

        # if the page pg is one amongst the links inside of current page,
        # then added the linked page probability
        if pg in corpus[page]:
            prob = prob + linked_page_prob

        prob_dist[pg] = prob
    
    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initalize sample rank to blank dictionary
    # This will hold the Page Rank for each page in corpus
    sample_rank = {}

    # get all pages list from corpus
    page_list = list(corpus)

    # select a random page
    selected_page = page_list[random.randint(0, len(page_list)-1)]

    # loop over based on provided sampling number
    for sample_idx in range(0,n):

        # get the probability distribution of selected page
        prob_dist = transition_model(corpus, selected_page, damping_factor)

        # pick a random number between 0 and 1
        rand_num = random.random()

        # initialize range limit to 0
        range_limit = 0

        # iterate over each page in corpus
        # Pick next page based on distribution
        # The way I implemented this as per example below
        #   rand_num - Pick a random number between 0 and 1. Say rand_num is 0.9
        #   I set the range limits based on probability distribution of selected page
        #   e.g for probability distibution <0.5, 0.2, 0.3>, I set ranges as below
        #       rand_num <= 0.5
        #       rand_num <= 0.7 (which is 0.5 + 0.2)
        #       rand_num <= 1.0 (which is 0.5 + 0.2 + 0.3)
        #   and pick the page that satisfies a specific range condition
        for pg in page_list:
            # set the range limit based on probability distribution of page
            range_limit = range_limit + prob_dist[pg]

            # if the rand_num is less or equal to computed range limit, then select it as next page
            if rand_num <= range_limit:
                selected_page = pg
                # increment the visit count of picked page in the sample_rank
                if(selected_page in sample_rank):
                    sample_rank[selected_page] = sample_rank[selected_page] + 1
                else:
                    sample_rank[selected_page] = 1
                break
        

    # normalizing
    for page, visit_count in sample_rank.items():
        sample_rank[page] = sample_rank[page] / n

    return sample_rank 


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # set accuracy value
    accuracy = 0.001

    # initalize iterate rank to blank dictionary
    # This will hold the Page Rank for each page in corpus
    iterate_rank = {}

    # get all pages list from corpus
    page_list = list(corpus)
    page_count = len(page_list)

    # assign equal probabilty to all pages in corpus
    prob = 1 / page_count
    for page in page_list:
        iterate_rank[page] = prob
    
    # compute random link probability
    random_prob = (1 - damping_factor) / page_count

    continueIteration = True

    while continueIteration:
        new_iterate_rank = {}

        # for each page
        for page in page_list:
            # get all the parent pages which contains link to this page
            parent_pages = get_parent_pages(corpus, page)
            
            linked_prob = 0
            # iterate thru each parent page and summate the links probability
            for parent in parent_pages:

                # number of links in the parent page
                no_of_links = len(corpus[parent])

                # if there are no links then consider it has links to all pages including itself
                if no_of_links == 0:
                    no_of_links = page_count

                # compute and summate the calculated probability
                linked_prob = linked_prob + (iterate_rank[parent] / no_of_links)

            # compute new Page Rank
            new_iterate_rank[page] = random_prob + (damping_factor * linked_prob)
        
        shouldContinue = False
        # check if the deviation between previous and new page ranks is within the state accuracy
        # if deviation is within the defined accuracy, then Page Rank has converged and stop further calculation
        for page in page_list:
            if abs(iterate_rank[page] - new_iterate_rank[page]) > accuracy:
                shouldContinue = True
                break
        
        continueIteration = shouldContinue

        # assign iterate_rank to new rank
        iterate_rank = new_iterate_rank.copy()

    # return page rank
    return iterate_rank

def get_parent_pages(corpus, page):
    """
        Returns list of parent pages that has links to provide page
    """
    parent_pages=[]
    for pg, linked_pages in corpus.items():
        if page in linked_pages or len(linked_pages) == 0:
            parent_pages.append(pg)

    return parent_pages

if __name__ == "__main__":
    main()
