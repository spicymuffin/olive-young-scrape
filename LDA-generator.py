# 문서별 주제 분포에서 확률이 가장 높은 주제를 출력하기 위한 함수
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis
from gensim.models import CoherenceModel
import matplotlib.pyplot as plt
from gensim import models
from gensim.corpora import Dictionary
import pickle
import os

NUM_TOPICS = 20

DIRNAME = "LDA-outputs"

BEFOREORAFTER = "after"
POSITIVEORNEGATIVEORCOMBINED = "combined"

CALCULATE_SCORES = False

# NNG for common nouns, NNP for proper nouns, VA for adjectives
acceptable_tags = ['VA', 'NNG', 'NNP']
TAGS_STR = "_".join(acceptable_tags)

INPUT_NAME = f"{BEFOREORAFTER}_{POSITIVEORNEGATIVEORCOMBINED}_review_morphs.pickle"
OUTPUT_DIR_NAME = f"{BEFOREORAFTER}_{POSITIVEORNEGATIVEORCOMBINED}_{TAGS_STR}_{NUM_TOPICS:02d}"
OUTPUT_NAME = f"{OUTPUT_DIR_NAME}"

# make folder in /LDA-outputs for the output files
if not os.path.exists(f"{DIRNAME}/{OUTPUT_DIR_NAME}"):
    os.makedirs(f"{DIRNAME}/{OUTPUT_DIR_NAME}")


def get_highest_topic(topic_list):
    highest_topic = 100
    highest_prob = 0
    for topic, prob in topic_list:
        if prob > highest_prob:
            highest_prob = prob
            highest_topic = topic
    return highest_topic, highest_prob


def get_adjective_words(morphs):
    global acceptable_tags
    adjective_words = []
    for word, tag in morphs:
        if tag in acceptable_tags:
            adjective_words.append(word)
    return adjective_words


total_morphs = pickle.load(
    open(f'LDA-inputs/{INPUT_NAME}', 'rb'))

type(total_morphs)
total_morphs.keys()
len(total_morphs)
print(total_morphs["doc_0"]["paper_id"])


# 3가지 정보를 별도 리스트 변수에 저장
documents = []
article_ids = []
text_titles = []
for key in total_morphs:
    documents.append(get_adjective_words(
        total_morphs[key]['content']))  # get only adjectives
    article_ids.append(total_morphs[key]['paper_id'])
    text_titles.append(total_morphs[key]['text_title'])

print(documents[0])

# 사용자 불용어 사전을 별도 파일로 저장
f_stop = open('stop_words.txt', 'r', encoding='utf-8')
stop_words = [word.strip() for word in f_stop.readlines()]
f_stop.close()

# 불용어 제거 => 불용어 사전
docs_filtered = [[term for term in doc if term not in stop_words]
                 for doc in documents]

print(docs_filtered[0])

# create a dictionary representation of the documents
dictionary = Dictionary(docs_filtered)

# filter out words that occur in less than 10 documents or more than 10% of the documents
dictionary.filter_extremes(no_below=10, no_above=0.1)

# DTM 생성
DTM = []
for doc in docs_filtered:
    bow = dictionary.doc2bow(doc)
    DTM.append(bow)

print(dictionary.token2id)

print('Number of unique tokens: %d' % len(dictionary))
print('Number of documents: %d' % len(DTM))
print(DTM[0])


lda_model = models.ldamodel.LdaModel(corpus=DTM, num_topics=NUM_TOPICS,
                                     id2word=dictionary, alpha='auto', eta='auto', iterations=1000)


TOPIC_ID = 0
NUM_TOPIC_WORDS = 10
lda_model.show_topic(TOPIC_ID, NUM_TOPIC_WORDS)


for topic_id in range(lda_model.num_topics):
    word_probs = lda_model.show_topic(topic_id, NUM_TOPIC_WORDS)
    print("Topic ID: {}".format(topic_id))
    for word, prob in word_probs:
        print("\t{}\t{}".format(word, prob))
    print("\n")

# get_highest_topic 함수 정의


def get_highest_topic(topics_list):
    # topics_list에서 확률이 가장 높은 주제를 찾음
    # 확률 기준으로 정렬하여 최대값 선택
    hi_topic, hi_prob = max(topics_list, key=lambda x: x[1])
    return hi_topic, hi_prob


# 10개의 문서를 순회하며 주제 출력
for i in range(10):
    print(article_ids[i])  # 문서 ID 출력
    print(text_titles[i][:50] + "...")  # 문서 제목을 50자까지만 출력하고 나머지는 생략

    # 문서의 주제 분포 가져오기
    topics_list = lda_model.get_document_topics(
        DTM[i], minimum_probability=0.05)
    print(topics_list)  # 주제 분포 출력

    # topics_list가 비어 있는 경우 처리
    if not topics_list:
        print("No topics found for this document.\n")
        continue  # 다음 문서로 넘어감

    # 확률이 가장 높은 주제 찾기
    hi_topic, hi_prob = get_highest_topic(topics_list)
    print(
        f"The most covered topic is Topic {hi_topic} and percentage is {hi_prob:.2f}\n")

if CALCULATE_SCORES:

    # -------------------------> perplexity

    lda_model.log_perplexity(DTM)

    start1 = 3
    limit1 = 50
    step1 = 5
    perplexity_scores = []
    for num_topics in range(start1, limit1, step1):
        model = models.ldamodel.LdaModel(DTM, num_topics=num_topics,
                                        id2word=dictionary, alpha='auto', eta='auto', iterations=100)
        perplexity_scores.append(model.log_perplexity(DTM))

    x = range(start1, limit1, step1)
    plt.plot(x, perplexity_scores)
    plt.xlabel("Num Topics")
    plt.ylabel("Log Perplexity scores")
    plt.legend(("Log Perplexity"), loc='best')
    plt.savefig(f"{DIRNAME}/{OUTPUT_DIR_NAME}/{OUTPUT_NAME}_logperplexityscore.png",
                dpi=300, bbox_inches="tight")

    # -------------------------> coherence


    def compute_coherence_values_umass(dictionary, corpus, texts, limit, start=2, step=3):
        coherence_values = []
        for num_topics in range(start, limit, step):
            model = models.ldamodel.LdaModel(corpus, num_topics=num_topics,
                                            id2word=dictionary, alpha='auto', eta='auto')
            coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary,
                                            coherence='u_mass', topn=30)
            coherence_values.append(coherencemodel.get_coherence())

        return coherence_values


    start1 = 3
    limit1 = 63
    step1 = 3
    coherence_values_umass = compute_coherence_values_umass(
        dictionary=dictionary, corpus=DTM, texts=docs_filtered, start=start1, limit=limit1, step=step1)

    x = range(start1, limit1, step1)
    plt.plot(x, coherence_values_umass)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score: u_mass")
    plt.legend(("coherence_values"), loc='best')
    plt.savefig(f"{DIRNAME}/{OUTPUT_DIR_NAME}/{OUTPUT_NAME}_coherence_score_u_mass.png",
                dpi=300, bbox_inches="tight")


    # -------------------------> coherence c_v

    def compute_coherence_values_cv(dictionary, corpus, texts, limit, start=2, step=3):

        coherence_values = []
        for num_topics in range(start, limit, step):
            model = models.ldamodel.LdaModel(corpus, num_topics=num_topics,
                                            id2word=dictionary, alpha='auto', eta='auto')
            coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary,
                                            coherence='c_v', topn=20)
            coherence_values.append(coherencemodel.get_coherence())

        return coherence_values


    coherence_values_cv = compute_coherence_values_cv(
        dictionary=dictionary, corpus=DTM, texts=docs_filtered, start=start1, limit=limit1, step=step1)

    x = range(start1, limit1, step1)
    plt.plot(x, coherence_values_cv)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score: c_v")
    plt.legend(("coherence_values"), loc='best')
    plt.savefig(f"{DIRNAME}/{OUTPUT_DIR_NAME}/{OUTPUT_NAME}_coherence_score_cv.png",
                dpi=300, bbox_inches="tight")

prepared_data = gensimvis.prepare(lda_model, DTM, dictionary)
# pyLDAvis.enable_notebook()
pyLDAvis.display(prepared_data)
pyLDAvis.save_html(
    prepared_data, f"{DIRNAME}/{OUTPUT_DIR_NAME}/{OUTPUT_NAME}_LDA_vis.html")
