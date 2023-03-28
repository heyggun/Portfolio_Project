# Portfolio_Project

### 2. [Project 2] PredictionML_and_NER/
 
  - Boosting 기반 성혼 예측 모델링 & 자사 서비스 자체 NER 사전 구축 기반 유저 소개글 키워드 추출 서비스 

[1] ai_chemistry_p_api
 => 성혼 데이터 기반 1:1 분석 모델 api
 
[2] ai_chemistry_list_api
 => 위의 성혼 데이터 기반 1:1 분석 모델 기반, 회원 별 가장 높은 점수를 가진 상대 유저를 랭킹 별 리스트화 해주는 api
 
[3] ai_report_api
 => 위의 [1] 모델과 합쳐져서, 회원 별 예측 모델 + 작성한 자기소개글 NER 기반 정성도 평가 및 키워드 추출 api 
 

 
 ## [데이터]
 
 - ai_report_data : ner 사전 데이터 & 불용어 데이터
 
 
 ## [기타] 
 
 + 한국어 Pos-tagging 테스트 : 보유한 데이터에 가장 적합한 pos-tagging을 위하여 형태소 분석기 테스트 과정이 담긴 jupyter file
 + add_ner : [3] 도메인(이성 매칭 기반)에 맞는 ner 사전 구축 후에, 새로운 ner 추출을 위한 작업이 담긴 jupyter file

