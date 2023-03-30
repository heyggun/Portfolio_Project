# Portfolio_Project

### 1. [Project 1] CF_recommendation/
 
  - CF(Collaborative Filtering) 기반 user 추천 서비스

[1] ai_chemistry_p_api
 => CF 기반 추천 서비스 api
 
 
 ## [데이터]
 
 - 유저 활동 로그데이터 2종 (좋아요, 프로필 열람) 을 기반으로 한 여성/남성 서비스 유저 score matrix 
 - active한 회원 목록 데이터
 - 여성, 남성 따로 matrix, score, optimizer, best_model이 다름
 
 
 ## [기타] 
 
 + ALS 알고리즘을 활용한 카카오 buffalo 라이브러리 활용
 + 쉘 스크립트로 매일매일 회원 데이터 및 회원 활동에 대해서 새벽에 스크립트 데몬이 돌아가고 추천이 갱신됨
 + 서비스 특성상 탈퇴가 잦아, 매일 아침 9-10시쯤 리스트가 갱신됨
 + 모델이 예측한 추천 회원을 web 단으로 보내면, web에서 db와 2차 검수하여, active한 회원들을 view 단에 뿌려줌
 
