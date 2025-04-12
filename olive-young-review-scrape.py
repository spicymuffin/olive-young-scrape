import requests
import json
import time
import os
import pickle
import sys
import re
import random

DATE = "2023/07/30"
# we sort reviews before and after this date (30th of july 2023)
DATE_OBJ = time.mktime(time.strptime(DATE, "%Y/%m/%d"))

# folder where reviews will be stored
REVIEWS_FOLDER = "reviews"
# folder before TIME
BEFORE_DATE_FOLDER = f"before-{time.strftime('%Y-%m-%d', time.localtime(DATE_OBJ))}"
AFTER_DATE_FOLDER = f"after-{time.strftime('%Y-%m-%d', time.localtime(DATE_OBJ))}"

BEFORE_DATE_FILEDUMP_NAME = f"reviews-before-{time.strftime('%Y-%m-%d', time.localtime(DATE_OBJ))}.txt"
AFTER_DATE_FILEDUMP_NAME = f"reviews-after-{time.strftime('%Y-%m-%d', time.localtime(DATE_OBJ))}.txt"

# folder in which the this .py file is located
FILE_DIR = os.path.dirname(os.path.realpath(__file__))
print(FILE_DIR)

PARAM_SAVE_INDIVIDUAL_REVIEWS = False
PARAM_SAVE_REVIEWS_TO_FILEDUMP = False
PARAM_PICKLE_REVIEWS = True

SCRAPE_DATA = True
LOAD_REVIEW_PICKLE = True

BEFORE_DATE_FILEDUMP_PATH = os.path.join(
    FILE_DIR, REVIEWS_FOLDER, BEFORE_DATE_FILEDUMP_NAME)
AFTER_DATE_FILEDUMP_PATH = os.path.join(
    FILE_DIR, REVIEWS_FOLDER, AFTER_DATE_FILEDUMP_NAME)

print("putting reviews before " + time.strftime('%Y-%m-%d',
      time.localtime(DATE_OBJ)) + " in " + BEFORE_DATE_FOLDER)
print("putting reviews after " + time.strftime('%Y-%m-%d',
      time.localtime(DATE_OBJ)) + " in " + AFTER_DATE_FOLDER)

# create folder if it does not exist
if not os.path.exists(REVIEWS_FOLDER):
    os.makedirs(REVIEWS_FOLDER)

if not os.path.exists(REVIEWS_FOLDER + "/" + BEFORE_DATE_FOLDER):
    os.makedirs(REVIEWS_FOLDER + "/" + BEFORE_DATE_FOLDER)

if not os.path.exists(REVIEWS_FOLDER + "/" + AFTER_DATE_FOLDER):
    os.makedirs(REVIEWS_FOLDER + "/" + AFTER_DATE_FOLDER)

cookies = {
    'RB_PCID': '1731401267149179890',
    'SCOUTER': 'x18mstbngb3g78',
    'sch_check': 'yes',
    'AMP_MKTG_7fbb263808': 'JTdCJTdE',
    '_gcl_au': '1.1.921450684.1731401268',
    '_trs_id': 'eY767471743212%3E5457',
    'EG_GUID': 'c7b25239-6a91-4304-98ee-ce181f3e8b24',
    '_fwb': '113kag16XK1HLfgyWaTRrie.1731401268550',
    'oliveyoung_CID': 'a3fbebe4bc20468ba6847d23f4030e14',
    '_tt_enable_cookie': '1',
    'recDescNo': '0',
    'liveCommerce': '4e0284c80390e070db0a7973b6480cd5d78792d6e664b66c8a6a437d37a05bac',
    'NetFunnel_Main': '',
    '_ttp': 'qUsLfr2g-7VTyKL4Gu2T7bpTPpN.tt.2',
    '_gid': 'GA1.3.1726424000.1734185816',
    'productHistory': '[{"goodsNo":"A000000158147","viewCount":17},{"goodsNo":"A000000209877","viewCount":1},{"goodsNo":"A000000206335","viewCount":1},{"goodsNo":"A000000183564","viewCount":1},{"goodsNo":"A000000106052","viewCount":1},{"goodsNo":"A000000208152","viewCount":1},{"goodsNo":"A000000204450","viewCount":2},{"goodsNo":"A000000014206","viewCount":1}]',
    'RB_SSID': 'pbeSCZThsg',
    'wcs_bt': 's_3ee47970f314:1734185867',
    '_ga_GMKKBJ29S2': 'GS1.1.1734185816.6.1.1734185867.9.0.0',
    '_ga_PZZTG1SN65': 'GS1.3.1734185816.5.1.1734185868.8.0.0',
    'cto_bundle': 'p7txbV94SCUyRmQ5bXhhNWxOajJaVkRPbkhtYTR3YThsMiUyRlpaRnMyQmVQblB0aHZ3UjA4ZDlUMDNWJTJGTW1IZGQyNG9xVGhhQTBJUnpjTVh2JTJGWklSU3NzRWFTaDdTZFNaNE9uSWpENmUycTVPWUZWVXdWMXJwUk5sdlByaWtrbzRZVGpBeUlEZG1yTEdnWlFrWmkxRElvM2lib0NzcnpEVU5LZ1ZvQU5LYWZ2YTlFR2lqcUdPb2hINW9aeUsyVzdaYjZrNEluNkFVbSUyQlB6VGhnUHJqSHdVTFpBUUJnZnNVS0xPdUtaNEZvSngwT1kxdjhqMiUyRkhJUTAlMkJ6cjNQOURmWCUyRlhZOHV4VkhZZ3BMcmNsRzZqSEgyUWlIdnZLTHVhc0VNYjdjSUJGRXVOOU5wVSUyQmw1dVNSM05pRTk5NXBvbXpHZDRMQzAxdw',
    '_ga_D4CXJXVDV8': 'GS1.3.1734185816.5.1.1734185868.8.0.0',
    'OYSESSIONID': 'fc4b66d0-3b84-4883-8384-816a0f24c584',
    'OYSESSIONID': 'fc4b66d0-3b84-4883-8384-816a0f24c584',
    '_ga_TTX3Z62VLN': 'GS1.1.1734193207.7.0.1734193207.60.0.0',
    '_ga_P9V7281JHW': 'GS1.1.1734193207.7.0.1734193207.60.0.0',
    '_ga': 'GA1.3.381308420.1731401268',
    'AMP_7fbb263808': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJhYmQ5NmFhYy1lMjc4LTRiNTYtOWJlOC01ZGVhMTljNTUxMjMlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzM0MTkzMjAxNDY4JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczNDE5NDI3NjQ0OSUyQyUyMmxhc3RFdmVudElkJTIyJTNBMTgyJTdE',
    '_gat_UA-92021806-9': '1',
    '_dd_s': 'rum=0&expire=1734195394164',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
    'cache-control': 'no-cache',
    # 'cookie': 'RB_PCID=1731401267149179890; SCOUTER=x18mstbngb3g78; sch_check=yes; AMP_MKTG_7fbb263808=JTdCJTdE; _gcl_au=1.1.921450684.1731401268; _trs_id=eY767471743212%3E5457; EG_GUID=c7b25239-6a91-4304-98ee-ce181f3e8b24; _fwb=113kag16XK1HLfgyWaTRrie.1731401268550; oliveyoung_CID=a3fbebe4bc20468ba6847d23f4030e14; _tt_enable_cookie=1; recDescNo=0; liveCommerce=4e0284c80390e070db0a7973b6480cd5d78792d6e664b66c8a6a437d37a05bac; NetFunnel_Main=; _ttp=qUsLfr2g-7VTyKL4Gu2T7bpTPpN.tt.2; _gid=GA1.3.1726424000.1734185816; productHistory=[{"goodsNo":"A000000158147","viewCount":17},{"goodsNo":"A000000209877","viewCount":1},{"goodsNo":"A000000206335","viewCount":1},{"goodsNo":"A000000183564","viewCount":1},{"goodsNo":"A000000106052","viewCount":1},{"goodsNo":"A000000208152","viewCount":1},{"goodsNo":"A000000204450","viewCount":2},{"goodsNo":"A000000014206","viewCount":1}]; RB_SSID=pbeSCZThsg; wcs_bt=s_3ee47970f314:1734185867; _ga_GMKKBJ29S2=GS1.1.1734185816.6.1.1734185867.9.0.0; _ga_PZZTG1SN65=GS1.3.1734185816.5.1.1734185868.8.0.0; cto_bundle=p7txbV94SCUyRmQ5bXhhNWxOajJaVkRPbkhtYTR3YThsMiUyRlpaRnMyQmVQblB0aHZ3UjA4ZDlUMDNWJTJGTW1IZGQyNG9xVGhhQTBJUnpjTVh2JTJGWklSU3NzRWFTaDdTZFNaNE9uSWpENmUycTVPWUZWVXdWMXJwUk5sdlByaWtrbzRZVGpBeUlEZG1yTEdnWlFrWmkxRElvM2lib0NzcnpEVU5LZ1ZvQU5LYWZ2YTlFR2lqcUdPb2hINW9aeUsyVzdaYjZrNEluNkFVbSUyQlB6VGhnUHJqSHdVTFpBUUJnZnNVS0xPdUtaNEZvSngwT1kxdjhqMiUyRkhJUTAlMkJ6cjNQOURmWCUyRlhZOHV4VkhZZ3BMcmNsRzZqSEgyUWlIdnZLTHVhc0VNYjdjSUJGRXVOOU5wVSUyQmw1dVNSM05pRTk5NXBvbXpHZDRMQzAxdw; _ga_D4CXJXVDV8=GS1.3.1734185816.5.1.1734185868.8.0.0; OYSESSIONID=fc4b66d0-3b84-4883-8384-816a0f24c584; OYSESSIONID=fc4b66d0-3b84-4883-8384-816a0f24c584; _ga_TTX3Z62VLN=GS1.1.1734193207.7.0.1734193207.60.0.0; _ga_P9V7281JHW=GS1.1.1734193207.7.0.1734193207.60.0.0; _ga=GA1.3.381308420.1731401268; AMP_7fbb263808=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJhYmQ5NmFhYy1lMjc4LTRiNTYtOWJlOC01ZGVhMTljNTUxMjMlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzM0MTkzMjAxNDY4JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczNDE5NDI3NjQ0OSUyQyUyMmxhc3RFdmVudElkJTIyJTNBMTgyJTdE; _gat_UA-92021806-9=1; _dd_s=rum=0&expire=1734195394164',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000158147&t_page=%ED%86%B5%ED%95%A9%EA%B2%80%EC%83%89%EA%B2%B0%EA%B3%BC%ED%8E%98%EC%9D%B4%EC%A7%80&t_click=%EA%B2%80%EC%83%89%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_search_name=%EC%96%B4%EB%AE%A4%EC%A6%88%ED%8B%B4%ED%8A%B8&t_number=1&dispCatNo=1000001000200060003&trackingCd=Result_1',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

# params for GET request (this is a python dictionary)

# no. of page from which we are getting the reviews from
page_index = 1
points = [2, 6, 4, 10, 8]
types = [100, 200]
# 001 to 032
item_nos = ["001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012", "013", "014", "015",
            "016", "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032"]

# shuffle the item_nos bc if they are in order, the server might block us
#random.shuffle(item_nos)

params = {
    "goodsNo": "A000000158147",
    "gdasSort": "01",
    "itemNo": "all_search",
    "pageIdx": str(page_index),
    "colData": "",
    "keywordGdasSeqs": "",
    "type": "",
    "point": "",
    "optionValue": "",
    "cTypeLength": "0",
}

# GET request to the server (with the cookies and headers and params above)
# we will iterate until response is empty json

review_counter = 0

if SCRAPE_DATA:
    reviews_list = [[], []]

    if PARAM_SAVE_REVIEWS_TO_FILEDUMP:
        reviews_before_filedump = open(
            BEFORE_DATE_FILEDUMP_PATH,
            "w",
            encoding="utf-8")

        reviews_after_filedump = open(
            AFTER_DATE_FILEDUMP_PATH,
            "w",
            encoding="utf-8")

    review_counter_before = 0
    review_counter_after = 0

    for item_no in item_nos:
        for type in types:
            for point in points:
                print(f"                      item_no\ttype\tpoint")
                print(f"scraping reviews for: {item_no}\t{type}\t{point}")
                while True:
                    params["pageIdx"] = str(page_index)
                    params["point"] = str(point)
                    params["type"] = str(type)
                    params["itemNo"] = item_no
                    params["optionValue"] = params["goodsNo"] + \
                        ":" + params["itemNo"]

                    # print(params)

                    response = requests.get(
                        "https://www.oliveyoung.co.kr/store/goods/getGdasNewListJson.do",
                        params=params,
                        cookies=cookies,
                        headers=headers,
                    )

                    # check wether respinse is empty json
                    json_text = response.text
                    # convert JSON text to a dictionary
                    review_data_dict = json.loads(json_text)
                    # remove all newlines
                    json_text = json_text.replace("\n", "")

                    # if the response is empty, break the loop
                    if ("gdasList" not in review_data_dict.keys()) or (len(review_data_dict["gdasList"]) == 0):
                        print(
                            f"\n\nno more reviews for option set, added {review_counter} reviews to the list")
                        review_counter = 0
                        f = open("response.json", "w", encoding="utf-8")
                        f.write(json_text)
                        f.close()
                        break

                    review_data_dict = review_data_dict["gdasList"]

                    # iterate over the reviews (in a page) and write them to a file and reviews_list
                    for review in review_data_dict:

                        review_counter += 1

                        # cleaned dict
                        cleaned_dict = {}
                        cleaned_dict["review_raw_text"] = review["gdasCont"]
                        cleaned_dict["review_rating"] = int(
                            int(review["gdasScrVal"]) / 2)
                        cleaned_dict["review_item"] = review["itemNm"]
                        cleaned_dict["user_nicknm"] = review["mbrNickNm"]

                        cleaned_dict["review_date"] = time.mktime(
                            time.strptime(review["dispRegDate"], "%Y.%m.%d"))

                        # print(cleaned_dict["review_date"] < DATE_OBJ)
                        # print(time.strftime('%d-%m-%Y', time.localtime(cleaned_dict['review_date'])), time.strftime('%d-%m-%Y', time.localtime(DATE_OBJ)))

                        # check if review is before or after DATE
                        if cleaned_dict["review_date"] < DATE_OBJ:
                            review_counter_before += 1

                            if PARAM_SAVE_INDIVIDUAL_REVIEWS:
                                # make a file in the folder before DATE
                                f = open(REVIEWS_FOLDER + "/" + BEFORE_DATE_FOLDER + "/" +
                                         f"{time.strftime('%Y-%m-%d', time.localtime(cleaned_dict['review_date']))}-{review_counter_before}-{review['mbrNickNm']}.txt", "w", encoding="utf-8")
                                f.write(cleaned_dict["review_raw_text"])
                                f.close()

                            if PARAM_SAVE_REVIEWS_TO_FILEDUMP:
                                reviews_before_filedump.write(
                                    cleaned_dict["review_raw_text"])
                                reviews_before_filedump.write("\n\n\n")
                                reviews_before_filedump.flush()

                            reviews_list[0].append(cleaned_dict)

                        else:
                            review_counter_after += 1

                            if PARAM_SAVE_INDIVIDUAL_REVIEWS:
                                # make a file in the folder after DATE
                                f = open(REVIEWS_FOLDER + "/" + AFTER_DATE_FOLDER + "/" +
                                         f"{time.strftime('%Y-%m-%d', time.localtime(cleaned_dict['review_date']))}-{review_counter_after}-{review['mbrNickNm']}.txt", "w", encoding="utf-8")
                                f.write(cleaned_dict["review_raw_text"])
                                f.close()

                            if PARAM_SAVE_REVIEWS_TO_FILEDUMP:
                                reviews_after_filedump.write(
                                    cleaned_dict["review_raw_text"])
                                reviews_after_filedump.write("\n\n\n")
                                reviews_after_filedump.flush()

                            reviews_list[1].append(cleaned_dict)

                        print(".", end="", flush=True)

                    page_index += 1

                page_index = 1
                time.sleep(0)

                params["pageIdx"] = str(page_index)
                params["point"] = "10"
                response = requests.get(
                    "https://www.oliveyoung.co.kr/store/goods/getGdasNewListJson.do",
                    params=params,
                    cookies=cookies,
                    headers=headers,
                )

    if PARAM_SAVE_REVIEWS_TO_FILEDUMP:
        # close the files
        reviews_before_filedump.close()
        reviews_after_filedump.close()

    print("pickling raw reviews...")
    if PARAM_PICKLE_REVIEWS:
        exit(1)
        with open(REVIEWS_FOLDER + "/scraped_reviews_" + time.strftime('%Y-%m-%d', time.localtime()) + ".pickle", "wb") as f:
            pickle.dump(reviews_list, f)

# preprocess the reviews

reviews = None

if LOAD_REVIEW_PICKLE:
    with open("reviews/scraped_reviews_2024-12-15.pickle", "rb") as f:
        reviews = pickle.load(f)

sentiment_sorted_reviews = {
    "before_date": {
        "positive": [],
        "negative": []
    },

    "after_date": {
        "positive": [],
        "negative": []
    }
}

before_date_reviews = ""
after_date_reviews = ""

# i = 0 for before_date, i = 1 for after_date
j = 0

for i in range(2):
    for review in reviews[i]:
        # remove html tags
        filtered_content = re.sub(
            r'<br\s*/?>', '\n', review['review_raw_text'])
        # replace multiple spaces with single space
        filtered_content = re.sub(r'\s+', ' ', filtered_content)
        # replace newlines with space
        filtered_content = re.sub(r'\n', ' ', filtered_content)

        # store the filtered content back to the review
        review['review_processed_text'] = filtered_content

        # store the review in the sentiment_sorted_reviews dict
        if review["review_rating"] >= 4:
            sentiment_sorted_reviews["after_date" if i == 1 else "before_date"]["positive"].append(
                review)
        elif review["review_rating"] <= 2:
            sentiment_sorted_reviews["after_date" if i == 1 else "before_date"]["negative"].append(
                review)

        # store the review in the before_date_reviews or after_date_reviews
        if i == 0:
            before_date_reviews += filtered_content + "\n"
        else:
            after_date_reviews += filtered_content + "\n"

# print stats
print("before Date:")
print("positive Reviews: ", len(
    sentiment_sorted_reviews["before_date"]["positive"]))
print("negative Reviews: ", len(
    sentiment_sorted_reviews["before_date"]["negative"]))
print("positive review ratio: ", len(sentiment_sorted_reviews["before_date"]["positive"]) / (len(
    sentiment_sorted_reviews["before_date"]["negative"]) + len(sentiment_sorted_reviews["before_date"]["positive"])))
print("negative review ratio: ", len(sentiment_sorted_reviews["before_date"]["negative"]) / (len(
    sentiment_sorted_reviews["before_date"]["negative"]) + len(sentiment_sorted_reviews["before_date"]["positive"])))
print("after Date:")
print("positive Reviews: ", len(
    sentiment_sorted_reviews["after_date"]["positive"]))
print("negative Reviews: ", len(
    sentiment_sorted_reviews["after_date"]["negative"]))
print("positive review ratio: ", len(sentiment_sorted_reviews["after_date"]["positive"]) / (len(
    sentiment_sorted_reviews["after_date"]["negative"]) + len(sentiment_sorted_reviews["after_date"]["positive"])))
print("negative review ratio: ", len(sentiment_sorted_reviews["after_date"]["negative"]) / (len(
    sentiment_sorted_reviews["after_date"]["negative"]) + len(sentiment_sorted_reviews["after_date"]["positive"])))

# write the reviews to a pickle file
with open("reviews/sentiment_sorted_reviews_2024-12-15.pickle", "wb") as f:
    pickle.dump(sentiment_sorted_reviews, f)

# write the reviews to a file
with open(f"{REVIEWS_FOLDER}/before_date_reviews_2024-12-15.txt", "w", encoding="utf-8") as f:
    f.write(before_date_reviews)

with open(f"{REVIEWS_FOLDER}/after_date_reviews_2024-12-15.txt", "w", encoding="utf-8") as f:
    f.write(after_date_reviews)
