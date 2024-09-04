## 프로젝트 개요

### **1️⃣ 구성**  
본 프로젝트는 클라이언트의 long-polling 요청에 대응하기 위한 서버의 Kafka 개발을 목적으로 합니다.  
1. **Kafka Producing** : 서버는 Kafka producer를 통해 클라이언트의 메시지 전송을 수신합니다.  
2. **Kafka Consuming** : 서버는 Kafka consumer를 통해 클라이언트의 메시지 long-polling 요청에 응답합니다.  
3. Kafka의 초기 설정값은 `.env` 파일을 참조하며, `dotenv` 라이브러리를 활용하여 로드합니다.  
4. 클라이언트의 신규 메시지 polling 요청에 대한 응답은 5초마다 갱신되며, 신규 메시지가 없다면 `204 No Content`를 응답합니다.


### **2️⃣ 개발 기간**  
- `2024.05.07`: 기본 코드 구성  
- `2024.08.26`: 코드 단순화(리팩토링), API 이름 변경


### **3️⃣ 사용법**  
1. 필요한 라이브러리를 설치합니다. (`requirements.txt` 참고)
2. `logging` 설정 파일을 작성합니다.
3. `.env` 파일에 Kafka 환경 변수를 작성하여 `dotenv`를 통해 환경 변수를 로드합니다.
4. Kafka 설정 파일을 작성합니다.
