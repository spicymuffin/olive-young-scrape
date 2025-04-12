from kiwipiepy import Kiwi
import pickle

MODE = "before"

kiwi = Kiwi()

texts = []

# # read reviews line by line into texts
# with open(f'reviews/{MODE}_date_reviews_2024-12-15.txt', 'r', encoding='utf-8') as f:
#     texts = f.readlines()

d = {}

# read reviews line by line into texts with pickle
with open(f'reviews/sentiment_sorted_reviews_2024-12-15.pickle', 'rb') as f:
    d = pickle.load(f)

for r in d["after_date"]["negative"]:
    texts.append(r["review_processed_text"])

# process texts and extract morphological analysis
processed_texts = {}
for idx, text in enumerate(texts):
    # using analyze to get morphological analysis
    analysis = kiwi.analyze(text)
    # taking the first result of the first analysis
    best_analysis = analysis[0][0]

    # store the results with document-related metadata
    processed_texts[f'doc_{idx}'] = {
        # extracting lex and tag
        'content': [(morph.form, morph.tag) for morph in best_analysis],
        'paper_id': f'ID_{idx}',
        'text_title': f'title_{idx}'
    }

    print(processed_texts[f'doc_{idx}'])

# save processed data as a pickle file
with open(f'LDA-inputs/after_negative_review_morphs.pickle', 'wb') as f:
    pickle.dump(processed_texts, f)
