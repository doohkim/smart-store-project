import pandas as pd
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from search.apis import request_api, data_cleanup, comma_request_api, comma_request_data_clean_up


class SingleKeywordSearchAPIView(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        data = {
            "hello": "hello"
        }
        Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data)
        # keyword_list = request.data.get('keyword', None).split(',')
        keyword = request.data.get('keyword', None)
        company_name = request.data.get('company', None)
        print('company_name', company_name)
        print(company_name == '')
        print(company_name == False)

        if keyword == '':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if company_name == '':
            company_name = None

        if keyword is None:
            return Response({'keyword 데이터 가져오기 실패'}, status=status.HTTP_404_NOT_FOUND)
        keyword_list = [keyword]

        if company_name is None:
            result = request_api(keyword_list)
            file_path_list, complete_result_data_header, complete_result_data = data_cleanup(1, result)
            data = {
                'complete_result_data_header': complete_result_data_header,
                "complete_result_data": complete_result_data
            }
            return Response(data=data, status=status.HTTP_200_OK)

        else:
            result = request_api(keyword_list)
            file_path_list, company_related_result_data_header, company_related_data, \
            complete_result_data = data_cleanup(1, result, company_name)

            data = {
                'company_related_result_data_header': company_related_result_data_header,
                "company_related_data": company_related_data
            }
            return Response(data=data, status=status.HTTP_200_OK)


class MultiKeywordSearchAPIView(GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        keyword_file = request.FILES['file']
        keywords_df = pd.read_excel(keyword_file)
        keywords = list(keywords_df['키워드'])
        result = request_api(keywords)

        file_path_list, complete_result_data_header, complete_result_data = data_cleanup(2, result)
        data = {
            'file_path_list': file_path_list,
            'complete_result_data_header': complete_result_data_header,
            "complete_result_data": complete_result_data
        }
        return Response(data=data, status=status.HTTP_200_OK)


class TestMultiKeywordSearchAPIView(GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        keyword_file = request.FILES['file']

        keywords_df = pd.read_excel(keyword_file)
        keywords = list(keywords_df['키워드'])
        try:
            company = list(keywords_df['회사'])
        except Exception as ex:
            print('not found company')

        data = {
            "keywords": keywords
        }
        return Response(data=data, status=status.HTTP_200_OK)


class SingleZeroKeywordSearchAPIView(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        keyword_input_text = request.data.get('keyword', None)
        company_name = request.data.get('company', None)
        if keyword_input_text == '':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if company_name == '':
            company_name = None

        if company_name is None:
            check = '0000000000000제로 키워드 검색 한거'
            keyword_data = comma_request_api(keyword_input_text, check)
            company_related_products_list, complete_data_list = comma_request_data_clean_up(keyword_input_text,
                                                                                            keyword_data,
                                                                                            company_name)
            data = {
                # 'complete_data_header': complete_data_header,
                'complete_result_data': complete_data_list
            }

            return Response(data=data, status=status.HTTP_200_OK)
        elif company_name is not None:
            check = '0000000000000 컴퍼니 컴퍼니 키워드 검색 한거'
            keyword_data = comma_request_api(keyword_input_text, check)
            company_related_products_list, complete_data_list = comma_request_data_clean_up(keyword_input_text,
                                                                                            keyword_data,
                                                                                            company_name)
            data = {
                # 'company_related_data_header': company_related_data_header,
                'complete_result_data': company_related_products_list
            }
            return Response(data=data, status=status.HTTP_200_OK)

        else:
            data = {
                'result': 'not intended work===side effect almost 404'
            }
            return Response(data=data, status=status.HTTP_200_OK)


class SingleFirstKeywordSearchAPIView(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        keyword_input_text = request.data.get('keyword', None)
        company_name = request.data.get('company', None)
        if keyword_input_text == '':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if company_name == '':
            company_name = None

        if company_name is None:
            check = '11111111111111 키워드 검색 한거'
            keyword_data = comma_request_api(keyword_input_text, check)
            company_related_products_list, complete_data_list = comma_request_data_clean_up(keyword_input_text,
                                                                                            keyword_data,
                                                                                            company_name)
            data = {
                # 'complete_data_header': complete_data_header,
                'complete_result_data': complete_data_list
            }

            return Response(data=data, status=status.HTTP_200_OK)
        elif company_name is not None:
            check = '0000000000000제로 키워드 검색 한거'
            keyword_data = comma_request_api(keyword_input_text, check)
            company_related_products_list, complete_data_list = comma_request_data_clean_up(keyword_input_text,
                                                                                            keyword_data,
                                                                                            company_name)
            data = {
                # 'company_related_data_header': company_related_data_header,
                'complete_result_data': company_related_products_list
            }
            return Response(data=data, status=status.HTTP_200_OK)

        else:
            data = {
                'result': 'not intended work===side effect almost 404'
            }
            return Response(data=data, status=status.HTTP_200_OK)


class SingleSecondKeywordSearchAPIView(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        keyword_input_text = request.data.get('keyword', None)
        company_name = request.data.get('company', None)
        if keyword_input_text == '':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if company_name == '':
            company_name = None

        if company_name is None:
            check = '2222222222제로 키워드 검색 한거'
            keyword_data = comma_request_api(keyword_input_text, check)
            company_related_products_list, complete_data_list = comma_request_data_clean_up(keyword_input_text,
                                                                                            keyword_data,
                                                                                            company_name)
            data = {
                # 'complete_data_header': complete_data_header,
                'complete_result_data': complete_data_list
            }

            return Response(data=data, status=status.HTTP_200_OK)
        elif company_name is not None:
            check = '0000000000000제로 키워드 검색 한거'
            keyword_data = comma_request_api(keyword_input_text, check)
            company_related_products_list, complete_data_list = comma_request_data_clean_up(keyword_input_text,
                                                                                            keyword_data,
                                                                                            company_name)
            data = {
                # 'company_related_data_header': company_related_data_header,
                'complete_result_data': company_related_products_list
            }
            return Response(data=data, status=status.HTTP_200_OK)

        else:
            data = {
                'result': 'not intended work===side effect almost 404'
            }
            return Response(data=data, status=status.HTTP_200_OK)


class SingleThirdKeywordSearchAPIView(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        keyword_input_text = request.data.get('keyword', None)
        company_name = request.data.get('company', None)
        if keyword_input_text == '':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if company_name == '':
            company_name = None

        if company_name is None:
            check = '3333333제로 키워드 검색 한거'
            keyword_data = comma_request_api(keyword_input_text, check)
            company_related_products_list, complete_data_list = comma_request_data_clean_up(keyword_input_text,
                                                                                            keyword_data,
                                                                                            company_name)
            data = {
                # 'complete_data_header': complete_data_header,
                'complete_result_data': complete_data_list
            }

            return Response(data=data, status=status.HTTP_200_OK)
        elif company_name is not None:
            check = '444444444444제로 키워드 검색 한거'
            keyword_data = comma_request_api(keyword_input_text, check)
            company_related_products_list, complete_data_list = comma_request_data_clean_up(keyword_input_text,
                                                                                            keyword_data,
                                                                                            company_name)
            data = {
                # 'company_related_data_header': company_related_data_header,
                'complete_result_data': company_related_products_list
            }
            return Response(data=data, status=status.HTTP_200_OK)

        else:
            data = {
                'result': 'not intended work===side effect almost 404'
            }
            return Response(data=data, status=status.HTTP_200_OK)
