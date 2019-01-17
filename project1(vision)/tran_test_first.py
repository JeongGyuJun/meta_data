import shutil
import requests
import json
import sys
sys.path.append('../../METADATA')
import METADATA
import os, uuid, sys # 이건 storage를 라
from azure.storage.blob import BlockBlobService, PublicAccess

def run_sample():
        try:
            print("스토리지에 이미지 올리고 해당 이미지의 uri를 이용하여 이미지 분석 준비")
            # Create the BlockBlockService that is used to call the Blob service for the storage account
            block_blob_service = BlockBlobService(account_name='projectimage', account_key='JRchgJJAHjSzDMHMe73/9p65tTQTY7R9v/flqDfZagSTj00JiPXlAqi44B3P4Dkr3htQL3Eq2DAG81DXS7GdTw==')

            # Create a container called 'quickstartblobs'.
            container_name ='ratice' # 저장소 이름을 대문자 사용하지말자
            # 대문자는 쓸 수 없는 문자라고 에러를 뱉는다.
            block_blob_service.create_container(container_name)

            # Set the permission so the blobsd are public.
            block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
            # # Create a file in Documents to test the upload and download.
            local_path=os.path.expanduser("~/Documents")
            local_file_name ="secondEx.jpeg"
            storage_url = METADATA.storage_url
            blob_url = storage_url + local_file_name

            full_path_to_file =os.path.join(local_path, local_file_name)

            block_blob_service.create_blob_from_path(container_name, local_file_name, full_path_to_file)

            result_image_analyze = use_describe_image_api(blob_url)
            result_tran = translate_ko(result_image_analyze)
            print("이미지 분석 결과:  ", result_tran)

        except Exception as e:
            print(e)

def use_describe_image_api(blob_url_des):
        params = {  #또 다른 정보
        'visualFeatures': 'Description',
        'langage': 'en'
        }

        headers = { #우리가 보내는 데이터 타입
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': METADATA.VISION_KEY # 메타 데이터엣 있는 것을 임포트 하여 사용함
        }

        data = {
        'url': blob_url_des
        }

        res = requests.post('https://koreacentral.api.cognitive.microsoft.com/vision/v1.0/analyze',
                        params=params, headers=headers, json=data)

        res_dit = json.loads(res.text)
        subscribed_text = res_dit["description"]["captions"][0]["text"]
        print(" 이미지 분석 함수 호출되어 텍스트로 변환 완료(영문) ")
        return subscribed_text

def translate_ko( result_en):
        non_subscribed_text =  result_en

        params = {  #또 다른 정보
            'api-version': '3.0',
            'from': 'en',
            'to' : 'ko'
                 }

        headers = { #우리가 보내는 데이터 타입
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': METADATA.TRANSLATE_KEY # 메타 데이터엣 있는 것을 임포트 하여 사용함
        }

        data = [{    #사진 자료
            'text' : non_subscribed_text # 이미지를 텍스트로 만들어서 이것을 번역하기 위한 데이터로 사용한다.
        }]

        res = requests.post('https://api.cognitive.microsofttranslator.com/translate',
                                params=params, headers=headers, json=data)
        res_dict = json.loads(res.text)
        result = res_dict[0]['translations'][0]['text'] # 여기 이 딕셔너리로 어떻게 원하는 값을 도출하는지 알아보자 !!
        print("한국어 번역 함수 호출되어서 번역 완료됨")
        return result




if __name__ == '__main__':
    run_sample()
