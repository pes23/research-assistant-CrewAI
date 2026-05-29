# 연구 보조 및 논문 초안 생성 시스템
본 시스템은 특정 연구 주제와 아이디어를 입력하면, 5개의 에이전트가 협업하여 학술 검색을 수행하고, 선행 연구 분석 및 비판을 거쳐 영문 논문 초안(abstraction, introduction)을 자동으로 작성하는 에이전틱 시스템이다.

개발 프레임워크: CrewAI (Google Gemini API 연동) 

## Project Directory Structure
research-assistant-crew/
├── .env.example            # 환경변수 설정 파일 예시 
├── .gitignore             
├── README.md               
├── main_research.py        # CrewAI 메인 소스 코드
└── final_research_proposal.md  # 시스템 실행 완료 후 자동 생성된 영문 논문 초안(예시)

## 에이전트 구성 및 역할 

1. Literature Scout: 실시간 구글 학술 검색 도구를 사용해 사용자가 입력한 주제 관련 최신 논문을 수집하고 요약한다.
2. Methodology Critic: 수집된 선행 연구들의 한계점을 찾아낸다.
3. Hypothesis Validator: 사용자의 아이디어가 선행 연구의 한계점을 어떻게 극복하는지 논리적으로 연결한다.
4. Academic Ghostwriter: 분석된 내용 바탕으로 영문으로 논문 초안 작성한다.
5. Principal Investigator(PI): 최종 초안을 검수하고 논리적 오류를 스스로 수정하여 보고서를 완성한다.

## 적용된 에이전틱 디자인 패턴

1. Multi-Agent: 독립된 전문성을 가진 5개의 에이전트가 상호작용한다.
2. Tool Use: `SerperDevTool`을 연동하여 실제 Google Scholar API 기반의 실시간 데이터 검색을 수행한다.
3. Planning: 본격적인 연구 분석 전, 에이전트가 스스로 세부 키워드 트리와 조사 로드맵을 먼저 설정한다.
4. Reflection: 최종 에디터(PI) 에이전트가 초안의 논리적 허점을 검토하고 스스로 교정(Self-Correction)하는 피드백 루프를 갖는다.
5. Reasoning Techniques: Methodology Critic 에이전트가 선행 연구의 한계점을 도출할 때 생각을 단계별로 풀어내는 Chain-of-Thought 방식을 사용한다.

## 실행 방법 
1. 환경변수 설정
```bash
cp .env.example .env 
# .env 파일에 GEMINI_API_KEY 입력

2. 필수 라이브러리 설치 
터미널에서 아래 명령어를 실행하여 필수 패키지를 설치 후 main_research.py 실행.
```bash
pip install crewai crewai-tools python-dotenv

3. 실행
```bash
python main_research.py 