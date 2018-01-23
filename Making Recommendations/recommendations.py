import math


# A dictionary of movie critics and their ratings of a small set of movies
critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 3.5
    },
    'Michael Phillips': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.0,
        'Superman Returns': 3.5,
        'The Night Listener': 4.0
    },
    'Claudia Puig': {
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'The Night Listener': 4.5,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5
    },
    'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 3.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 2.0
    },
    'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'The Night Listener': 3.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5
    },
    'Toby': {
        'Snakes on a Plane': 4.5,
        'You, Me and Dupree': 1.0,
        'Superman Returns': 4.0
    }
}


# Returns the list of shared items
def __get_shared_items(data, person1, person2):
    result = dict()
    for item in data[person1]:
        if item in data[person2]:
            result[item] = 1
    return result


def __summation(data, shared_items, user, power=1):
    return sum([data[user][item] ** power for item in shared_items])


def __summation_product(data, shared_items, person1, person2):
    return sum([data[person1][item] * data[person2][item] for item in shared_items])


# Returns a distance based similarity score fro 2 users
def euclidean_distance(data, person1, person2):
    # If there is no ratings in common return 0
    if not len(__get_shared_items(data, person1, person2)):
        return 0
    # Add up the squares of all the differences
    result = sum([(data[person1][item] - data[person2][item]) ** 2 for item in data[person1] if item in data[person2]])
    return 1 / (1 + result)


# Returns a pearson correlation coefficient for 2 users
def pearson_correlation(data, person1, person2):
    shared_items = __get_shared_items(data, person1, person2)
    # Find the number of items
    n = len(shared_items)
    # If there is no ratings in common return 0
    if not n:
        return 0
    # Add up all the ratings
    sum1, sum2 = __summation(data, shared_items, person1), __summation(data, shared_items, person2)
    # Sum up the squares
    sum1_square, sum2_square = __summation(data, shared_items, person1, 2), __summation(data, shared_items, person2, 2)
    # Sum up the products
    sum_products = __summation_product(data, shared_items, person1, person2)
    # Calculate the pearson score
    numerator = sum_products - (sum1 * sum2 / n)
    denominator = math.sqrt((sum1_square - pow(sum1, 2) / n) * (sum2_square - pow(sum2, 2) / n))
    return 0 if not denominator else numerator / denominator


# Returns the best matches for a person from dataset.
# Number of results and similarity function are optional parameters
def top_matches(data, person, n=5, similarity=pearson_correlation):
    return sorted([(similarity(data, person, other), other) for other in data if other != person], reverse=True)[0:n]


# Returns recommendations for a user based on weighted average of all other user's ratings
def get_recommendations(data, person, similarity=pearson_correlation):
    totals, similarity_sums = dict(), dict()
    for other in data:
        # Don't compare me to myself
        if other == person:
            continue
        similarity_score = similarity(data, person, other)
        # Ignore similarity scores that are less than 0
        if similarity_score <= 0:
            continue
        for item in data[other]:
            # Only score movies i haven't seen
            if item not in data[person] or not data[person][item]:
                totals.setdefault(item, 0)
                # Similarity * score
                totals[item] += (data[other][item] * similarity_score)
                similarity_sums.setdefault(item, 0)
                similarity_sums[item] += similarity_score
    # Return the normalized sorted list
    return sorted([(total / similarity_sums[item], item) for item, total in totals.items()], reverse=True)


def transform_data(data):
    result = dict()
    for person in data:
        for item in data[person]:
            result.setdefault(item, dict())
            # Flip item and person
            result[item][person] = data[person][item]
    return result


def calculate_similar_items(data, n=10):
    # Create a dictionary of items showing which other items they are most similar to.
    result = dict()
    # Invert the data matrix to be item-centric.
    temp = transform_data(data)
    count = 0
    for item in temp:
        # Status updates for large datasets.
        count += 1
        if not count % 100:
            print('%d\t%d' % (count, len(temp)))
        # Find the most similar items to this one
        scores = top_matches(temp, item, n=n, similarity=euclidean_distance)
        result[item] = scores
    return result


def get_recommended_items(data, item_based_data, user):
    user_ratings, scores, total_similarity = data[user], dict(), dict()
    # Loop over items rated by this user
    for (item, rating) in user_ratings.items():
        # Loop over items similar to this one
        for (similarity, item2) in item_based_data[item]:
            # Ignore if this user has already rated this item
            if item2 in user_ratings:
                continue
            # Weighted sum of rating times similarity
            scores.setdefault(item2, 0)
            scores[item2] += (similarity * rating)
            # Sum of all the similarities
            total_similarity.setdefault(item2, 0)
            total_similarity[item2] += similarity
    # Divide each total score by total weighting to get an average
    return sorted([(score / total_similarity[item], item) for (item, score) in scores.items()], reverse=True)


if __name__ == '__main__':
    # print(euclidean_distance(critics, 'Lisa Rose', 'Gene Seymour'))
    # print(pearson_correlation(critics, 'Lisa Rose', 'Gene Seymour'))
    # print(top_matches(critics, 'Toby', n=3))
    # print(get_recommendations(critics, 'Toby'))
    # print(get_recommendations(critics, 'Toby', similarity=euclidean_distance))
    # print(top_matches(transform_data(critics), 'Superman Returns'))
    # print(get_recommendations(transform_data(critics), 'Just My Luck'))
    # print(calculate_similar_items(critics))
    print(get_recommended_items(critics, calculate_similar_items(critics), 'Toby'))

