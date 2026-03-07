# Contributing to GovKR-MD

GovKR-MD는 대한민국 정부 문서를 Markdown으로 변환하는 오픈소스 프로젝트입니다.

개발자, 연구자, 시민 누구나 참여할 수 있습니다.

---

# 참여 방법

다음과 같은 방식으로 기여할 수 있습니다.

### 문서 기여

* 누락된 정부 문서 추가
* Markdown 변환 오류 수정
* 문서 구조 개선
* 메타데이터 보완

### 개발 기여

* 크롤러 개발
* 문서 파서 개선
* 검색 기능 개발
* API 개발

### 데이터 품질 개선

* 문서 구조 정리
* 태그 개선
* 문서 분류 개선

---

# Pull Request 과정

1. Repository fork
2. 새로운 branch 생성

```
git checkout -b feature/add-policy-doc
```

3. 변경 사항 commit

```
git commit -m "Add ministry policy document"
```

4. Pull Request 생성

---

# 문서 작성 가이드

모든 문서는 Markdown으로 작성됩니다.

필수 메타데이터:

```
---
doc_id:
title:
doc_type:
organization:
date_published:
source_url:
---
```

---

# 문서 품질 기준

문서는 다음 기준을 따라야 합니다.

* 원문 의미 유지
* 구조 명확
* 불필요한 HTML 제거
* 표준 Markdown 사용

---

# 커뮤니티

이 프로젝트는 **열린 협업**을 지향합니다.

모든 참여자는 서로 존중하며 협력해야 합니다.

자세한 내용은 CODE_OF_CONDUCT.md를 참고하세요.
