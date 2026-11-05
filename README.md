# My Daily News 1.0

개인용 뉴스 대시보드 + 텔레그램 브리핑. Python 표준 라이브러리만 사용합니다. AI 요약은 **아직 포함되지 않습니다**. 뉴스 제목과 원문 링크를 보냅니다.

## 1. 로컬 테스트

1. Python 3.8 이상 설치.
2. 프로젝트 폴더에서 `python news.py` 실행 (Windows에서 `py -3 news.py` 가능).
3. `docs/news.json` 파일이 생성되었는지 확인.
4. `python -m http.server 8000 --directory docs` 실행.
5. 브라우저에서 `http://localhost:8000` 접속.

## 2. Telegram 봇 준비

1. Telegram에서 공식 `@BotFather`에게 `/newbot` 명령을 보내 봇 생성.
2. 발급된 **봇 토큰을 비공개**로 보관 (코드에 붙여 넣지 않기).
3. 생성한 봇에게 `/start` 메시지를 보냅니다.
4. 브라우저에서 `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`를 열어 응답의 `message.chat.id`를 확인합니다. `<YOUR_TOKEN>`은 실제 토큰으로 대체합니다. 주소를 다른 사람과 공유하지 마세요. 브라우저 방문 기록에도 토큰이 남을 수 있습니다.
5. GitHub 저장소 Settings → Secrets and variables → Actions → New repository secret 에서 `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` 등록.

## 3. GitHub 자동 실행

1. 새 GitHub 저장소를 만들고 **프로젝트 폴더 안의 모든 파일**을 업로드 (`.github/workflows/daily.yml` 포함). 공개 저장소라면 개인 정보와 토큰을 절대 넣지 마세요.
2. Settings → Pages → Build and deployment → Deploy from a branch → `main` / `/docs` → Save. Pages URL에서 웹앱 확인. Pages는 정적 호스팅으로 Python 서버가 상시 실행되지는 않습니다.
3. Actions → Daily News → Run workflow 로 수동 실행해 Telegram 수신과 `docs/news.json` 갱신 확인.
4. 이후 GitHub Actions가 **한국시간 매일 오전 8시 무렵** 실행합니다. GitHub 예약 실행은 지연되거나 실행이 누락될 수 있고, 공개 저장소의 장기간 비활성 상태에서는 예약 워크플로가 비활성화될 수 있습니다.

## 유의 사항

- GitHub Pages 사이트는 일반적으로 공개 접근이 가능하므로 개인 뉴스 목록에 민감한 데이터를 넣지 마세요.
- Google News RSS의 접근 가능 여부 및 기사량은 변경될 수 있습니다.
- 이 프로젝트는 5개 분야에서 기사를 수집해 분야별 2개씩 Telegram에 보냅니다. **기사 본문 요약이 아닙니다.**
- 무료 사용은 GitHub 요금제, 사용량 및 정책에 따라 달라집니다.
- 뉴스 수집 후 Telegram 전송에 성공했지만 GitHub 저장 실패 시 데이터 갱신이 누락될 수 있습니다.
