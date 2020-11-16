from django.conf import settings
from powernad.API import RelKwdStat

from config.global_variables import dict_
from config.settings import NAVER_SHOP_API, NAVER_KEYWORD_API

import time

import pandas as pd
import requests


def naver_keyword_api(keyword):
    # NAVER_KEYWORD_SEARCH_BASE_URL = NAVER_KEYWORD_API['NAVER_KEYWORD_SEARCH_BASE_URL']
    # # 엑세스 라이센스
    # NAVER_KEYWORD_SEARCH_API_KEY = NAVER_KEYWORD_API['NAVER_KEYWORD_SEARCH_API_KEY']
    # # 비밀키
    # NAVER_KEYWORD_SEARCH_SECRET_KEY = NAVER_KEYWORD_API['NAVER_KEYWORD_SEARCH_SECRET_KEY']
    # # customer_ID
    # NAVER_KEYWORD_SEARCH_CUSTOMER_ID = NAVER_KEYWORD_API['NAVER_KEYWORD_SEARCH_CUSTOMER_ID']
    time.sleep(1)
    relKwdStat = RelKwdStat.RelKwdStat(NAVER_KEYWORD_API['NAVER_KEYWORD_SEARCH_BASE_URL'],
                                       NAVER_KEYWORD_API['NAVER_KEYWORD_SEARCH_API_KEY'],
                                       NAVER_KEYWORD_API['NAVER_KEYWORD_SEARCH_SECRET_KEY'],
                                       NAVER_KEYWORD_API['NAVER_KEYWORD_SEARCH_CUSTOMER_ID'])
    # showDetail = '2' 하면 왜 bug 나오는지 모르겠음
    keyword_data_list = relKwdStat.get_rel_kwd_stat_list(None, hintKeywords=keyword, showDetail='1')
    return keyword_data_list


# **kwargs 써도 될듯 한데??
# 없을 경우에는
def request_api(keywords):
    keyword_dict = dict()
    # 키워드 리스트
    for key_index, keyword in enumerate(keywords):
        print(keyword)
        # 1 - 600위 순위 스토어 목록 가져오기
        each_keyword_api_pull_result = list()

        for start in range(1, 302, 100):
            url = f'https://openapi.naver.com/v1/search/shop?query={keyword}&start={start}&display=100'
            NAVER_SHOP_API_CLIENT_ID = NAVER_SHOP_API["NAVER_SHOP_API_CLIENT_ID"]
            NAVER_SHOP_API_CLIENT_SECRET = NAVER_SHOP_API["NAVER_SHOP_API_CLIENT_SECRET"]
            header = {
                "X-Naver-Client-Id": NAVER_SHOP_API_CLIENT_ID,
                "X-Naver-Client-Secret": NAVER_SHOP_API_CLIENT_SECRET
            }
            try:
                # 실제 개발할 때 초당 10건이상이 되면 Error 발생
                r = requests.get(url, headers=header)
                result = r.json()
                print('첫번째 키워드 검색')
                print('HTTP status code : ', r.status_code)
                # print(start)
                # if start == 101:
                #     time.sleep(1)
            except Exception as ex:
                print('not response 404', ex)
                continue

            for item in result['items']:
                each_keyword_api_pull_result.append(item)

        keyword_dict[keyword] = each_keyword_api_pull_result
    return keyword_dict


def data_cleanup(single, keyword_dict, *company_name):
    try:
        company_name = company_name[0]
        print(company_name)
    except Exception as ex:
        company_name = None
        print('파라미터 company_name 못받음', ex)

    each_keyword_dict = dict()
    not_good_input_data = list()
    company_related_products_list = list()
    company_related_products_info = dict()
    for keyword, keyword_data in keyword_dict.items():
        page = 1
        count = 39
        page_rank = 1
        keyword_item_list = list()
        # 검색량 조회 api request function
        keyword_data_list = naver_keyword_api(keyword)
        monthlyPc = keyword_data_list[0].monthlyPcQcCnt
        monthlyMobile = keyword_data_list[0].monthlyMobileQcCnt
        time.sleep(1)
        for num, item in enumerate(keyword_data):

            item_dict = dict()
            item_dict['rank'] = num
            item_dict['page'] = page
            item_dict['each_page_rank'] = page_rank
            item_dict['keword'] = keyword
            item_dict['PC_search'] = monthlyPc
            item_dict['Mobile_search'] = monthlyMobile
            item_dict['productId'] = item['productId']
            item_dict['title'] = item['title'].replace('<b>', '').replace('</b>', '')
            item_dict['lowPrice'] = item['lprice']
            item_dict['highPrice'] = item['hprice']
            item_dict['mallName'] = item['mallName']
            item_dict['productGroup'] = dict_[item['productType']][0]
            item_dict['productType'] = dict_[item['productType']][1]
            item_dict['brand'] = item['brand']
            item_dict['maker'] = item['maker']
            item_dict['category1'] = item['category1']
            item_dict['category2'] = item['category2']
            item_dict['category3'] = item['category3']
            item_dict['category4'] = item['category4']
            item_dict['image'] = item['image']
            # 회사 관련 검색어
            if company_name is not None and company_name == item['mallName']:
                company_related_products_list.append(item_dict)

            try:
                price_value = int(item['lprice'])
            except Exception as ex:
                print('price value not int type ', ex)
            if type(price_value) != int:
                not_good_input_data.append(item['productId'])
                print(item['title'].replace('<b>', '').replace('</b>', ''))

            page_rank += 1
            keyword_item_list.append(item_dict)
            #             print(item_dict)
            #             print('************')

            if num == count:
                page_rank = 1
                page += 1
                count += 40
        company_related_products_info['company'] = company_related_products_list
        each_keyword_dict[keyword] = keyword_item_list

    #         print(keyword_item_list)
    #         print('************')

    file_path_list = dict()
    complete_result_data = list()
    for keyword, json_data in each_keyword_dict.items():
        # 100개씩 저장된 리스트 합치
        complete_result_data = complete_result_data + json_data
        each_keyword_file_path = settings.MEDIA_ROOT + '/' + keyword + '_result_data.csv'
        file_path_list[keyword] = each_keyword_file_path
        # 키워드별로 엑셀 파일로 저장
        if single != 1:
            pd.json_normalize(json_data).to_csv(each_keyword_file_path,
                                                encoding='utf-8-sig')
    # 전체 키워드 검색어 데이터 엑셀 파일로 저장
    complete_result_pandas_data = pd.json_normalize(complete_result_data)
    # 컬럼 헤더
    complete_result_data_header = complete_result_pandas_data.columns
    complete_result_file_path = settings.MEDIA_ROOT + '/complete_result_pandas_data.csv'
    file_path_list['complete_result_file_path'] = complete_result_file_path
    if single != 1:
        complete_result_pandas_data.to_csv(complete_result_file_path, encoding='utf-8-sig')

    # 지명된 회사 데이터만 따로 뽑기
    if company_name is not None:
        company_related_data = list()
        for company, company_related_product in company_related_products_info.items():
            company_related_data = company_related_data + company_related_product
        file_path_with_company = settings.MEDIA_ROOT + '/' + company_name + 'related_result_data.csv'
        file_path_list['file_name_with_company'] = file_path_with_company
        company_related_result_data = pd.json_normalize(company_related_data)
        company_related_result_data_header = company_related_result_data.columns
        if single != 1:
            company_related_result_data.to_csv(file_path_with_company, encoding='utf-8-sig')

        return [file_path_list, company_related_result_data_header, company_related_data, complete_result_pandas_data]

    return [file_path_list, complete_result_data_header, complete_result_data]


def comma_request_api(keyword, check):
    keyword_dict = dict()
    each_keyword_api_pull_result = list()

    for start in range(1, 302, 100):
        url = f'https://openapi.naver.com/v1/search/shop?query={keyword}&start={start}&display=100'
        header = {
            "X-Naver-Client-Id": NAVER_SHOP_API["NAVER_SHOP_API_CLIENT_ID"],
            "X-Naver-Client-Secret": NAVER_SHOP_API["NAVER_SHOP_API_CLIENT_SECRET"]
        }
        try:
            r = requests.get(url, headers=header)
            result = r.json()
            print('HTTP status code : ', r.status_code, ':::::::::', keyword, check)
            # print(result)
            time.sleep(1)
        except Exception as ex:
            print('not response 404', ex)
            continue
        product_total = result['total']

        for item in result['items']:
            item['total'] = product_total
            each_keyword_api_pull_result.append(item)

    keyword_dict[keyword] = each_keyword_api_pull_result
    # return keyword_dict
    return each_keyword_api_pull_result


def comma_request_data_clean_up(keyword_input_text, keyword_data, *company):
    each_keyword_dict = dict()
    not_good_input_data = list()
    company_related_products_list = list()
    company_related_products_info = dict()
    print(company)
    company = company[0]
    page = 1
    count = 39
    page_rank = 1
    complete_data_list = list()
    # 검색량 조회 api request function
    print('keyword_input_text', keyword_input_text)
    # how_many_search_keyword_info = naver_keyword_api(keyword_input_text)
    # monthlyPc = how_many_search_keyword_info[0].monthlyPcQcCnt
    # monthlyMobile = how_many_search_keyword_info[0].monthlyMobileQcCnt
    monthlyPc = 1000
    monthlyMobile = 10000
    time.sleep(1)
    for num, item in enumerate(keyword_data):
        item_dict = dict()
        item_dict['rank'] = num
        item_dict['page'] = page
        item_dict['each_page_rank'] = page_rank
        item_dict['keword'] = keyword_input_text
        item_dict['PC_search'] = monthlyPc
        item_dict['Mobile_search'] = monthlyMobile
        item_dict['productId'] = item['productId']
        item_dict['total'] = item['total']
        item_dict['title'] = item['title'].replace('<b>', '').replace('</b>', '')
        item_dict['lowPrice'] = item['lprice']
        item_dict['highPrice'] = item['hprice']
        item_dict['mallName'] = item['mallName']
        item_dict['productGroup'] = dict_[item['productType']][0]
        item_dict['productType'] = dict_[item['productType']][1]
        item_dict['brand'] = item['brand']
        item_dict['maker'] = item['maker']
        item_dict['category1'] = item['category1']
        item_dict['category2'] = item['category2']
        item_dict['category3'] = item['category3']
        item_dict['category4'] = item['category4']
        item_dict['image'] = item['image']

        # 입력한 회사 관련 제품들 데이터 리스
        if company is not None and company == item['mallName']:
            company_related_products_list.append(item_dict)

        # 올바르게 기입되지 못한 제품
        try:
            price_value = int(item['lprice'])
        except Exception as ex:
            print('price value not int type ', ex)
        if type(price_value) != int:
            not_good_input_data.append(item['productId'])
            print(item['title'].replace('<b>', '').replace('</b>', ''))

        page_rank += 1
        complete_data_list.append(item_dict)
        if num == count:
            page_rank = 1
            page += 1
            count += 40

    return [company_related_products_list, complete_data_list]
