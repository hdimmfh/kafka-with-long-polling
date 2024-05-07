## 🏋🏼‍♀️ 소개
본 프로젝트는 kafka를 활용한 long polling 기능구현 개발 프로젝트 입니다.</br>
kafka의 컨슈머, 프로듀서를 활용하여 데이터 파이프라인을 구축합니다.</br>
사용자는 5초마다 새로운 데이터를 요청합니다.</br>
새로운 데이터가 있다면 결과를 반환하고, 없다면 오류가 발생합니다.(exception handling 필요)</br>
- 개발일자 : 2024.05.07

## ⚽️ 사용법
1. 필요한 라이브러리를 설치합니다. (requirements.txt 참고)
2. logging 설정 파일을 작성합니다.
3. dotenv 활용을 통한 환경변수 로드를 위해 .env 파일에 kafka 환경변수를 작성합니다.
4. kafka 설정 파일을 작성합니다.

<kbd>
  <img width="1050" alt="ppt image1" src="https://github.com/hdimmfh/long-polling-with-kafka/assets/74033655/195b9f02-3ee6-4e65-a340-f1afb65a75df">
</kbd>
<kbd>
  <img width="1050" alt="ppt image2" src="https://github.com/hdimmfh/long-polling-with-kafka/assets/74033655/70b341b5-01a3-4cb2-8a66-937bfea09c68">
</kbd>
<kbd>
 <img width="1050" alt="ppt image3" src="https://github.com/hdimmfh/long-polling-with-kafka/assets/74033655/dc072ae2-01de-4219-b558-3a0447acfd7e">
</kbd>
<kbd>
  <img width="1050" alt="ppt image4" src="https://github.com/hdimmfh/long-polling-with-kafka/assets/74033655/15c2e730-6723-49f7-b022-0864ddfb9656">
</kbd>
