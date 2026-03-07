# GovKR-MD Document Schema

이 문서는 GovKR-MD 프로젝트의 **Markdown 문서 구조 표준**을 정의합니다.

모든 문서는 동일한 메타데이터 구조를 따라야 합니다.

---

# Document Structure

모든 문서는 다음 구조를 사용합니다.

```
Frontmatter (YAML)
Markdown Body
```

---

# Frontmatter

모든 문서는 YAML 메타데이터를 포함해야 합니다.

Example:

```
---
doc_id: KR-GOV-MOE-POLICY-2025-001
title: 2025 교육 정책 추진 계획
doc_type: policy
organization: Ministry of Education
country: KR
date_published: 2025-03-01
language: ko
source_url: https://www.moe.go.kr
tags:
 - education
 - policy
---
```

---

# 필수 필드

| field          | 설명       |
| -------------- | -------- |
| doc_id         | 문서 고유 ID |
| title          | 문서 제목    |
| doc_type       | 문서 유형    |
| organization   | 기관       |
| date_published | 발행 날짜    |
| source_url     | 원문 URL   |

---

# 선택 필드

| field        | 설명    |
| ------------ | ----- |
| version      | 문서 버전 |
| date_updated | 수정 날짜 |
| language     | 언어    |
| tags         | 문서 태그 |

---

# Document Types

```
law
decree
rule
notice
announcement
policy
whitepaper
report
guideline
committee_minutes
statistics
api_documentation
```

---

# Document ID Format

문서 ID는 다음 구조를 사용합니다.

```
COUNTRY-ORG-TYPE-YEAR-NUMBER
```

Example:

```
KR-GOV-MOE-POLICY-2025-001
```

---

# File Naming

파일 이름은 다음 형식을 사용합니다.

```
YYYY-title.md
```

Example:

```
2025-education-policy.md
```

---

# Directory Structure

```
docs/
 ├ laws/
 ├ decrees/
 ├ rules/
 ├ notices/
 ├ policies/
 ├ reports/
 └ committee-minutes/
```

---

# Markdown Rules

문서는 가능한 한 **순수 Markdown**을 사용합니다.

권장:

* 제목: #
* 목록: -
* 코드 블록: ```

지양:

* inline HTML
* 복잡한 스타일

---

# Long-term Goal

이 스키마는 다음을 목표로 합니다.

* 공공 문서 표준화
* 기계 읽기 가능 구조
* 정책 데이터 분석
* AI 학습 데이터셋
