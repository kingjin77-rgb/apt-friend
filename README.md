# 아파트친구 (apt-friend)

법무법인 제이엘이 만드는 아파트 생애주기 컨시어지 앱 — 입주예정자협의회(입예협) 결성부터 입주자대표회의(입대의) 구성까지, 그리고 입주민 생활정보와 전문가 컨시어지까지 하나로.

## 페이지 구성

| 파일 | 설명 |
|---|---|
| `index.html` | 메인 (입대의 · 입예협 · 입주민 · 컨시어지 4탭) |
| `start-association.html` | 협의회 없는 개인이 시작하는 발기인 모집 |
| `lifecycle-guide.html` | 결성→계약검수→사전점검→인수인계→입대의구성→인계, 6단계 로드맵 |
| `document-center.html` | 공문서 자동생성센터 (위임장/회칙/소집공고문/결성통지서/임원선출결과) |
| `poa-system.html` | 위임장 전자서명 접수 시스템 (실시간 접수율 대시보드 + 운영진 모드) |
| `resources.html` | 단계별 템플릿 자료실 |
| `tools.html` | 담보책임기간 계산기 · 내용증명 생성기 |
| `contents.html` | 단지 운영 실무 콘텐츠 12편 |
| `signup.html` / `login.html` | 회원가입 / 로그인 |
| `community.html` / `post-detail.html` / `write-post.html` | 커뮤니티 게시판 |
| `mypage.html` | 마이페이지 |
| `concierge-request.html` | 컨시어지 상담신청 (분야선택→매칭→예약) |
| `handover-checklist.html` | 입예협→입대의 인계 체크리스트 |
| `app-onboarding.html` | 모바일 앱 온보딩 3화면 목업 |
| `app-full-demo.html` | 모바일 앱 전체 작동 목업 (온보딩+탭바 4개 화면) |

## 배포 (GitHub Pages)

1. Settings → Pages → Branch: `main` / `/(root)` 선택
2. `https://<username>.github.io/<repo명>/` 으로 접속

## 상태

프로토타입 단계 — 모든 데이터 저장은 브라우저 localStorage 기반 데모입니다. 실서비스 전환 시 백엔드(DB) 연동이 필요합니다.
