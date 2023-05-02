import datetime
import requests
import json

#NY Times API Info
api_key = "YOUR_API_KEY"
article_search_endpoint = "https://api.nytimes.com/svc/search/v2/articlesearch.json?api-key=" + api_key

def response_test(word, year):
    # Set up query params:
    # Search query
    q="&q=" + word
    # Format the year for the API call
    year_begin = "&begin_date=" + str(year) + "0101"
    year_end = "&end_date=" + str(year) + "1231"

    # Add query params to API call
    request_endpoint = article_search_endpoint + q + year_begin + year_end

    # Return the number of articles
    article_response = str(requests.get(request_endpoint).json()["response"]["meta"]["hits"])
    print(article_response)


# Get the number of articles in the New York Times in a given year containing a word
def get_articles_count(word, year):
    # Set up query params:
    # Search query
    q="&q=" + word
    # Format the year for the API call
    year_begin = "&begin_date=" + str(year) + "0101"
    year_end = "&end_date=" + str(year) + "1231"

    # Add query params to API call
    request_endpoint = article_search_endpoint + q + year_begin + year_end

    # Return the number of articles
    try:
        numberOfArticles = int(requests.get(request_endpoint).json()['response']['meta']['hits'])
        success = True
    except KeyError:
        print("Key Error hit; Likely hit API call limit for the next minute.")
        numberOfArticles = 0
        success = False
    return (numberOfArticles, success)


# Find the year over year prevalence of a word in the New York Times
def get_word_prevalence_by_year(word, years_back):
    curr_yr = datetime.datetime.now().year
    years = [curr_yr]

    # Get range of years to look at
    for i in range(years_back):
        years.append(curr_yr - i)

    # Dictionary to hold prevalence data
    word_prevalence_data = {}

    for year in years:
        # Get the number of hits from article search word in the year
        article_count = get_articles_count(word, year)
        # If the API call was successful
        if article_count[1]:
            word_prevalence_data[year] = article_count[0]
        else:
            #early return
            return word_prevalence_data

    return word_prevalence_data


if __name__ == '__main__':
    search_term_prevalence = get_word_prevalence_by_year("obesity", 3)

    print("Year over year prevalence of the word 'obesity' in the New York Times:")

    for year in search_term_prevalence:
        print(str(year) +  ": " + str(search_term_prevalence[year]))
