# Portfolio_Project


### 7. [Side_Project 2]

  - 양방향 사람 추천 모델링(Reciprocal Recommendation System; RRS)


[1] ai_rrs_api -> 상호추천 서비스 api

- 알고리즘 설명 : https://www.notion.so/yeoboya-success-member-analysis/people-to-people-Reciprocal-recommendation-system-click-b41643b709974361a13c6a048806a4c5

## [데이터]

- active한 회원 데이터
- 탈퇴한 회원 데이터 & 탈퇴한 회원의 메시지 및 열람 등의 로그 데이터
- 전체 회원 데이터에서 필요한 feature 및 파생변수로 전처리 된 회원 데이터
- 서비스 유저 메시지 데이터, 프로필 열람 데이터
- active 및 exit(탈퇴)한 회원들의 데이터를 기반으로 응답률 데이터
- 회원 feature간 상관관계(corrleation)를 파악하기 위해 필요한 feature만 추출한 회원 데이터
 

## [모델]

- 위의 응답률 데이터로 학습한 응답률 예측 모델(catboosting 사용)

## [기타]

- Akiva Kleinerman,  Ariel Rosenfeld(2019). Supporting users in fnding successful matches in reciprocal recommender systems
 논문 참고
-전통적인 item-to-people recommender system에서는, 보통 추천의 성공이 추천(items)을 받아들이는 receiver(추천을 받는 사람, 즉 서비스 유저)에 의해 결정됨
반면, RRSs에서 성공적인 추천은 두 사용자의 “successful interaction(성공적 상호작용)”을 이끌어 내는 것
- 즉, 서비스 유저가 추천을 받고 난 후 추천된 유저(recommended user)에게 상호작용을 개시했는지, 그리고 가장 중요한 것은 추천 된 유저가 그 상호작용에 긍정적으로 응했는지 여부
- 머신러닝 및 최적화 테크닉과 결합한 유저 history data 기반의 새로운 유저 모델링(user modeling)과 추천 방법론(recommendation method)이 결합된 추천서비스
- 논문에 따르면 CF 기반 유사도 측정 후에, 긍정 응답을 예측하고 해당 유사도와 긍정 응답에 대한 스코어를 집계하는데
개개인 유저의 히스토리 데이터에 대한 가중치를 적용하여 최종 점수를 집계한다
실서비스에 적용해보려고 테스트 해 본 결과, 실시간 추천이 어려워 로직을 약간 변경하여 긍정응답
긍정응답을 먼저 계산하고, 긍정응답이 있는 회원들을 대상으로 유사도를 측정하고 설명론을 들어가는 로직으로 변경하였음
- 해당 설명론에서 다수의 유저 간 상관관계가 잘 도출되지 않는 현상이 일어나서, feature의 재 선별이 필요한 단계에서 개발 보류 중
