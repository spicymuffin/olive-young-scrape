import requests
import json
import time
import os
import pickle


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

# cookies sent to server (these dont really matter)
cookies = {
    "RB_PCID": "1731401267149179890",
    "SCOUTER": "x18mstbngb3g78",
    "OYSESSIONID": "53fde9fa-136a-45ca-ba75-0f10072831b8",
    "OYSESSIONID": "53fde9fa-136a-45ca-ba75-0f10072831b8",
    "sch_check": "yes",
    "AMP_MKTG_7fbb263808": "JTdCJTdE",
    "_gcl_au": "1.1.921450684.1731401268",
    "_trs_id": "eY767471743212%3E5457",
    "_trs_sid": "G%5B646055565303%5Bg%5B545653561030%3C7675",
    "_trs_flow": "",
    "_gid": "GA1.3.268714859.1731401268",
    "EG_GUID": "c7b25239-6a91-4304-98ee-ce181f3e8b24",
    "_fwb": "113kag16XK1HLfgyWaTRrie.1731401268550",
    "oliveyoung_CID": "a3fbebe4bc20468ba6847d23f4030e14",
    "_tt_enable_cookie": "1",
    "_ttp": "qUsLfr2g-7VTyKL4Gu2T7bpTPpN",
    "recDescNo": "0",
    "_gat": "1",
    "_gat_UA-92021806-9": "1",
    "_gat_UA-181867310-1": "1",
    "productHistory": '[{"goodsNo":"A000000158147","viewCount":5}]',
    "RB_SSID": "lanNe7MYtB",
    "_ga_GMKKBJ29S2": "GS1.1.1731401268.1.1.1731401592.48.0.0",
    "wcs_bt": "s_3ee47970f314:1731401592",
    "_ga_PZZTG1SN65": "GS1.3.1731401269.1.1.1731401593.50.0.0",
    "_ga_D4CXJXVDV8": "GS1.3.1731401268.1.1.1731401594.50.0.0",
    "cto_bundle": "DRRxoV94SCUyRmQ5bXhhNWxOajJaVkRPbkhtYTBvR3ZRb2p6bUpUNjlzSmJWdVdiT2FZM05ib0ZWaFZWTHNVcEVCZk5SZXoyaVNERzIyZWtINlJuMlZ4eGVraWU1d2pZNG5UQm1TM2U3bGdYRWl5N3BhaiUyQnM4NUE1dmw4OXRHN2o0dm92JTJCOUxVcGJrWXFpSkxlVjhUYjFYcnlRVXM3ZXJFY3lRSVUxMWlEQnkxdmRYRzh0YUwlMkJlNlJzb1EyRTJmOUN5WVdHJTJGczJRd1ExYlZ0eEVhdWs0SG5iOTdpc1kxQ3Y1dXlWaFJJM0hpSUROZGM2TzdWT3VXbmNqMHhSREsyUnZPajZtWjVyb0FDRW1zJTJCUk5lclVRRjZLTGdDQSUzRCUzRA",
    "_ga_TTX3Z62VLN": "GS1.1.1731401268.1.1.1731401599.41.0.0",
    "_ga_P9V7281JHW": "GS1.1.1731401284.1.1.1731401599.41.0.0",
    "_ga": "GA1.3.381308420.1731401268",
    "_dd_s": "rum=0&expire=1731402507110",
    "AMP_7fbb263808": "JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJhYmQ5NmFhYy1lMjc4LTRiNTYtOWJlOC01ZGVhMTljNTUxMjMlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzMxNDAxMjY3ODQxJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczMTQwMTYwNzEzOCUyQyUyMmxhc3RFdmVudElkJTIyJTNBMTclN0Q=",
}

# this doesnt matter too much, too
headers = {
    "accept": "*/*",
    "accept-language": "en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4",
    "cache-control": "no-cache",
    # 'cookie': 'RB_PCID=1731401267149179890; SCOUTER=x18mstbngb3g78; OYSESSIONID=53fde9fa-136a-45ca-ba75-0f10072831b8; OYSESSIONID=53fde9fa-136a-45ca-ba75-0f10072831b8; sch_check=yes; AMP_MKTG_7fbb263808=JTdCJTdE; _gcl_au=1.1.921450684.1731401268; _trs_id=eY767471743212%3E5457; _trs_sid=G%5B646055565303%5Bg%5B545653561030%3C7675; _trs_flow=; _gid=GA1.3.268714859.1731401268; EG_GUID=c7b25239-6a91-4304-98ee-ce181f3e8b24; _fwb=113kag16XK1HLfgyWaTRrie.1731401268550; oliveyoung_CID=a3fbebe4bc20468ba6847d23f4030e14; _tt_enable_cookie=1; _ttp=qUsLfr2g-7VTyKL4Gu2T7bpTPpN; recDescNo=0; _gat=1; _gat_UA-92021806-9=1; _gat_UA-181867310-1=1; productHistory=[{"goodsNo":"A000000158147","viewCount":5}]; RB_SSID=lanNe7MYtB; _ga_GMKKBJ29S2=GS1.1.1731401268.1.1.1731401592.48.0.0; wcs_bt=s_3ee47970f314:1731401592; _ga_PZZTG1SN65=GS1.3.1731401269.1.1.1731401593.50.0.0; _ga_D4CXJXVDV8=GS1.3.1731401268.1.1.1731401594.50.0.0; cto_bundle=DRRxoV94SCUyRmQ5bXhhNWxOajJaVkRPbkhtYTBvR3ZRb2p6bUpUNjlzSmJWdVdiT2FZM05ib0ZWaFZWTHNVcEVCZk5SZXoyaVNERzIyZWtINlJuMlZ4eGVraWU1d2pZNG5UQm1TM2U3bGdYRWl5N3BhaiUyQnM4NUE1dmw4OXRHN2o0dm92JTJCOUxVcGJrWXFpSkxlVjhUYjFYcnlRVXM3ZXJFY3lRSVUxMWlEQnkxdmRYRzh0YUwlMkJlNlJzb1EyRTJmOUN5WVdHJTJGczJRd1ExYlZ0eEVhdWs0SG5iOTdpc1kxQ3Y1dXlWaFJJM0hpSUROZGM2TzdWT3VXbmNqMHhSREsyUnZPajZtWjVyb0FDRW1zJTJCUk5lclVRRjZLTGdDQSUzRCUzRA; _ga_TTX3Z62VLN=GS1.1.1731401268.1.1.1731401599.41.0.0; _ga_P9V7281JHW=GS1.1.1731401284.1.1.1731401599.41.0.0; _ga=GA1.3.381308420.1731401268; _dd_s=rum=0&expire=1731402507110; AMP_7fbb263808=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJhYmQ5NmFhYy1lMjc4LTRiNTYtOWJlOC01ZGVhMTljNTUxMjMlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzMxNDAxMjY3ODQxJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczMTQwMTYwNzEzOCUyQyUyMmxhc3RFdmVudElkJTIyJTNBMTclN0Q=',
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000158147&t_page=%ED%86%B5%ED%95%A9%EA%B2%80%EC%83%89%EA%B2%B0%EA%B3%BC%ED%8E%98%EC%9D%B4%EC%A7%80&t_click=%EA%B2%80%EC%83%89%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_search_name=%EC%96%B4%EB%AE%A4%EC%A6%88%ED%8B%B4%ED%8A%B8&t_number=1&dispCatNo=1000001000200060003&trackingCd=Result_1",
    "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}

# params for GET request (this is a python dictionary)

# no. of page from which we are getting the reviews from
page_index = 1

params = {
    "goodsNo": "A000000158147",
    "gdasSort": "01",
    "itemNo": "all_search",
    "pageIdx": str(page_index),
    "colData": "",
    "keywordGdasSeqs": "",
    "type": "100,200",
    "point": "",
    "hashTag": "",
    "optionValue": "",
    "cTypeLength": "0",
}

# GET request to the server (with the cookies and headers and params above)
# we will iterate until response is empty json

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

while True:
    response = requests.get(
        "https://www.oliveyoung.co.kr/store/goods/getGdasNewListJson.do",
        params=params,
        cookies=cookies,
        headers=headers,
    )

    page_index += 1
    params["pageIdx"] = str(page_index)

    # check wether respinse is empty json
    json_text = response.text
    # convert JSON text to a dictionary
    review_data_dict = json.loads(json_text)

    # if the response is empty, break the loop
    if "gdasList" not in review_data_dict.keys():
        print("no more reviews")
        break

    review_data_dict = review_data_dict["gdasList"]

    # iterate over the reviews (in a page) and write them to a file and reviews_list
    for review in review_data_dict:

        # cleaned dict
        cleaned_dict = {}
        cleaned_dict["review_raw_text"] = review["gdasCont"]
        cleaned_dict["review_rating"] = review["gdasScrVal"]
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
                reviews_before_filedump.write(cleaned_dict["review_raw_text"])
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
                reviews_after_filedump.write(cleaned_dict["review_raw_text"])
                reviews_after_filedump.write("\n\n\n")
                reviews_after_filedump.flush()

            reviews_list[1].append(cleaned_dict)

    print(f"added {len(review_data_dict)} reviews to the list (before/after: {review_counter_before}/{review_counter_after})")

if PARAM_SAVE_REVIEWS_TO_FILEDUMP:
    # close the files
    reviews_before_filedump.close()
    reviews_after_filedump.close()

print("pickling reviews...")
if PARAM_PICKLE_REVIEWS:
    with open(REVIEWS_FOLDER + "/" + BEFORE_DATE_FOLDER + "/scraped_reviews_" + time.strftime('%Y-%m-%d', time.localtime(DATE_OBJ)) + ".pickle", "wb") as f:
        pickle.dump(reviews_list, f)
