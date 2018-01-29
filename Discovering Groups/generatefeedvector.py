import re
import feedparser


def get_words(html):
    # Remove all the HTML tags
    text = re.compile(r'<[^>]+>').sub('', html)
    # Split words by all non-alpha characters
    words = re.compile(r'[^A-Z^a-z]+').split(text)
    # Convert to lowercase
    return [word.lower() for word in words if word != '']


# Returns title and dictionary of word counts for an RSS feed
def get_word_counts(url):
    temp = feedparser.parse(url)
    word_count = dict()
    # Loop over all the entries
    for entry in d.entries:
        summary = entry.summary if 'summary' in entry else entry.description
        # Extract a list of words
        for word in get_words(entry.title + ' ' + entry.summary):
            word_count.setdefault(word, 0)
            word_count[word] += 1
    return temp.feed.title, word_count


appeared_count, word_counts, word_list, feed_list, success, fail = dict(), dict(), list(), [line for line in file('feedlist.txt')], 0, 0
for url in feed_list:
    try:
        title, value = get_word_counts(url)
        word_counts[title] = value
        for word, count in value.items():
            appeared_count.setdefault(word, 0)
            if count > 1:
                appeared_count[word] += 1
        success += 1
    except:
        fail += 1
        print('Failed to parse: ' + url)
print('Successfully parsed %d urls' % success)
print('Failed parsing %d urls' % fail)
for word, count in appeared_count.items():
    fraction = float(count) / len(feedlist)
    if 0.1 < fraction < 0.5:
        word_list.append(word)
output = file('blog_data.txt', 'w')
output.write('Blog')
for word in word_list:
    output.write('\t' + word)
output.write('\n')
for blog, value in word_counts.items():
    output.write(blog)
    for word in word_list:
        output.write('\t' + str(value[word]) if word in value else '0')
    output.write('\n')
