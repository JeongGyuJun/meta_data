import requests
import json
import sys
sys.path.append('../../METADATA')
import METADATA
# 궁금증
# 파일 http가 아닌 파일 형식으로 여는 것 (Pro 1과 다른 점은 이 부분이다.)
# with open('193px-Classroom.jpeg', 'rb') as f:# 이부분은 파일 형식으로
#     image_data = f.read() # 열어야하기 때문에 추가한다.



params = {  #또 다른 정보
    'visualFeatures': 'Description',
    'langage': 'en'

         }
headers = { #우리가 보내는 데이터 타입
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': METADATA.VISION_KEY # 메타 데이터엣 있는 것을 임포트 하여 사용함
}


data = {
    'url': 'https://projectimage.blob.core.windows.net/ratice/firstEx.jpeg'

}

res = requests.post('https://koreacentral.api.cognitive.microsoft.com/vision/v1.0/analyze',
                        params=params, headers=headers, data=data)
#  json이 아닌 data로 바꿘준다.


#여기까지해서 requests하면 통신을 해서 값을 받아올 수 있다.
#####################################################################################

#다음으로 딕셔너리,리스트 자료형을 해서 원하는 정보 값을 알 수 있다.(알맞은 자료형으로 변환해서 사용)

res_dict = json.loads(res.text)
subscribed_text = res_dict['description']['captions'][0]['text']


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
    'text' : subscribed_text # 이미지를 텍스트로 만들어서 이것을 번역하기 위한 데이터로 사용한다.
}]

res = requests.post('https://api.cognitive.microsofttranslator.com/translate',
                        params=params, headers=headers, json=data)
res_dict = json.loads(res.text)
result = res_dict[0]['translations'][0]['text'] # 여기 이 딕셔너리로 어떻게 원하는 값을 도출하는지 알아보자 !!
print(result)
