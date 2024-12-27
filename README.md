<h2>💁프로젝트 소개</h2>
<p>Pollloop는 Django 기반의 동적 설문조사 및 QnA 플랫폼 백엔드입니다. 사용자들이 다양한 유형의 설문을 쉽게 생성하고 관리할 수 있으며, 실시간 양방향 통신이 가능한 Ask 보드를 운영할 수 있습니다.</p>
<p><strong>개발 기간</strong>: 2024.12.18 ~ 2025.01.16 (30일)</p>

<h2>🚀주요 기능</h2>
<h3>폼(Form) 기능</h3>
<ul>
    <li>다양한 질문 유형 지원 (단답형, 장문형, 체크박스, 라디오, 드롭다운 등)</li>
    <li>파일 업로드 처리 (이미지, PDF, 스프레드시트)</li>
    <li>임시 저장 및 발행 기능</li>
    <li>결과 분석 및 통계 생성</li>
    <li>참여자 관리 및 초대 시스템</li>
</ul>

<h3>Ask 기능</h3>
<ul>
    <li>질문 작성 및 관리 API</li>
    <li>좋아요 기능 구현</li>
    <li>익명/실명 옵션 처리</li>
    <li>공지사항 CRUD 작업</li>
    <li>질문 고정 및 숨김 기능</li>
    <li>종료 후 통계 데이터 제공</li>
</ul>

<h2>🤖기술 스택</h2>
<ul>
    <li><strong>프레임워크</strong>: Django</li>
    <li><strong>데이터베이스</strong>: MySQL</li>
    <li><strong>API</strong>: Django REST Framework</li>
    <li><strong>인증</strong>: JWT (JSON Web Tokens)</li>
    <li><strong>실시간 통신</strong>: Django Channels</li>
    <li><strong>테스트</strong>: pytest</li>
    <li><strong>문서화</strong>: Swagger/OpenAPI</li>
    <li><strong>버전 관리</strong>: Git</li>
</ul>

<h2>💼팀 소개</h2>
<p>백엔드 개발자 (3명):</p>
<ul>
    <li>김명현: 사용자 인증 및 권한 관리, 데이터 분석 및 통계 처리</li>
    <li>신현민: 폼 생성 및 관리 API, 배포, Ask 기능 및 실시간 통신 구현</li>
    <li>이준영: 사용자 인증 및 권한 관리</li>
</ul>

<h2>프로젝트 문서</h2>
<ul>
    <li>요구사항 명세서</li>
    <li>데이터베이스 스키마</li>
    <li>API 명세서</li>
    <li>시스템 아키텍처 문서</li>
    <li>배포 가이드</li>
</ul>

<h2>실행 방법</h2>
<pre><code># 저장소 클론

<h2>Git 워크플로우</h2>
<h3>브랜치 전략</h3>
<ul>
    <li><code>main</code>: 프로덕션 배포용 브랜치</li>
    <li><code>develop</code>: 개발 통합 브랜치</li>
    <li><code>feature/*</code>: 기능 개발 브랜치</li>
    <li><code>hotfix/*</code>: 긴급 버그 수정 브랜치</li>
</ul>

<h3>커밋 메시지 컨벤션</h3>
<pre><code>type: subject

<p><strong>유형</strong>:</p>
<ul>
    <li><code>feat</code>: 새로운 기능 추가</li>
    <li><code>fix</code>: 버그 수정</li>
    <li><code>docs</code>: 문서 수정</li>
    <li><code>style</code>: 코드 포맷팅, 세미콜론 누락 등</li>
    <li><code>refactor</code>: 코드 리팩토링</li>
    <li><code>test</code>: 테스트 코드</li>
    <li><code>chore</code>: 빌드 작업, 패키지 매니저 설정 등</li>
</ul>

<p><strong>예시</strong>:</p>
<pre><code>feat: 사용자 인증 API 구현
