import pandas as pd
import metapy
import numpy as np
from itertools import chain

def get_m_2_ngrams(input_list, min, max):
    for s in chain(*[get_ngrams(input_list, k) for k in range(min, max+1)]):
        yield ' '.join(s)

def get_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])


pt = pd.read_csv("Positive Terms.csv", encoding='latin1')
nt = pd.read_csv("Negative Terms.csv", encoding='latin1')

# tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
# tok = metapy.analyzers.LowercaseFilter(tok)
# tok = metapy.analyzers.LengthFilter(tok, min=2, max=15)
# tok = metapy.analyzers.Porter2Filter(tok)
# tok = metapy.analyzers.ListFilter(tok, "lemur-stopwords.txt", metapy.analyzers.ListFilter.Type.Reject)
# ana = metapy.analyzers.NGramWordAnalyzer(1, tok)

# with open('Q4_V2.txt') as query_file:
#     g_tokens = []
#     for line in query_file:
#         doc = metapy.index.Document()
#         doc.content(line.strip())
#         unigrams = ana.analyze(doc)
#         tok.set_content(doc.content())
#
#         tokens, counts = [], []
#         for token, count in unigrams.items():
#             counts.append(count)
#             g_tokens.append(token)

with open('Textsource.txt') as query_file:
    g_tokens = []
    strip_list = []
    bow = []
    for line in query_file:
        g_tokens.extend(line.split())

    for s in get_m_2_ngrams(g_tokens, 1, 6):
        bow.append(s)

bow_df = pd.DataFrame(np.array(bow))
bow_df.columns = ['Tokens']
bow_df['count'] = bow_df.groupby('Tokens')['Tokens'].transform('count')

values = bow_df['Tokens']
pt['Match'] = pt['Positive'].isin(values).astype(int)
nt['Match'] = nt['Negative'].isin(values).astype(int)

positive_score = pt['Match'].sum()
negative_score = nt['Match'].sum()

sentiment = positive_score - negative_score

print('Positive Score:', positive_score)
print('Negative Score:', negative_score)
print('Sentiment Score:', sentiment)
