# 🇰🇷 GovKR-MD

대한민국 정부 문서 Markdown 아카이브
Korean Government Documents in Markdown

GovKR-MD는 대한민국의 정부 문서를 **Markdown 형식으로 변환하여 공개 저장소로 관리하는 오픈소스 프로젝트**입니다.

법령, 시행령, 행정규칙, 고시, 정책 보고서, 백서, 공고, 회의록 등
정부가 생산하는 다양한 문서를 **구조화된 Markdown 문서**로 변환하여
Git 기반 버전 관리와 공개 협업이 가능하도록 하는 것을 목표로 합니다.

---

# 프로젝트 목표

* 대한민국 정부 문서를 Markdown으로 변환
* Git 기반 버전 관리
* 기계가 읽을 수 있는 공공 문서 구조 제공
* 공공 정책과 행정 기록의 투명성 향상
* AI 및 데이터 분석을 위한 공공 데이터 기반 구축

---

# Project Goal (English)

GovKR-MD is an open-source project that converts Korean government documents into structured Markdown.

The goal is to create a **version-controlled, machine-readable archive of public administration documents**.

This enables:

* transparent public records
* collaborative improvements
* machine-readable government data
* long-term archival
* AI-ready public policy datasets

---

# 포함 문서 범위

이 프로젝트는 대한민국 정부가 생산하는 다양한 공공 문서를 포함합니다.

### 법령 문서

* 법률
* 대통령령
* 총리령
* 부령
* 조례
* 규칙

### 행정 문서

* 고시
* 공고
* 훈령
* 예규
* 지침
* 행정해석

### 정책 문서

* 정책 보고서
* 백서
* 연구 보고서
* 국정 과제
* 정부 전략 문서

### 기록 문서

* 위원회 회의록
* 국무회의 자료
* 정부 통계 보고서
* 공공 API 문서

---

# Document Scope (English)

The project includes various types of government documents:

Legal Documents

* Laws
* Presidential Decrees
* Ministerial Orders
* Administrative Rules
* Local Ordinances

Administrative Documents

* Notices
* Announcements
* Directives
* Guidelines

Policy Documents

* White Papers
* Policy Reports
* Research Reports
* National Strategy Documents

Institutional Records

* Committee Minutes
* Government Meeting Records
* Public Statistics Reports
* API Documentation

---

# Repository Structure

```id="0t8yco"
govkr-md
├── schema
│   └── Markdown document specification
│
├── crawler
│   └── government website crawlers
│
├── parser
│   └── converters (HTML / PDF / XML → Markdown)
│
├── normalization
│   └── metadata normalization tools
│
├── docs
│   ├── laws
│   ├── decrees
│   ├── rules
│   ├── notices
│   ├── policies
│   ├── reports
│   └── committee-minutes
│
├── site
│   └── static documentation website
│
└── search
    └── search index and API
```

---

# 문서 예시

```id="qbv9sz"
---
doc_id: KR-GOV-MOE-POLICY-2025-001
title: 2025 교육 정책 추진 계획
doc_type: policy
organization: Ministry of Education
country: KR
date_published: 2025-03-01
source_url: https://www.moe.go.kr
tags:
 - education
 - reform
---

# 2025 교육 정책 추진 계획

교육부는 다음과 같은 정책을 추진한다.
```

---

# 문서 유형

```id="50m7te"
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

# 왜 Markdown인가?

Markdown은 다음과 같은 장점이 있습니다.

* 장기 보존에 유리한 단순한 포맷
* Git 기반 버전 관리 가능
* 협업 수정(Pull Request) 가능
* 기계 처리 및 분석 용이
* 정적 사이트 생성 가능

공공 문서는 **투명하고, 접근 가능하며, 버전 관리되어야 합니다.**

---

# 데이터 출처

가능한 데이터 출처

* law.go.kr
* 정부 부처 공식 웹사이트
* 공공데이터포털
* 정책 보고서 아카이브
* 정부 보도자료

---

# 기여 방법

개발자, 연구자, 기자, 시민 누구나 참여할 수 있습니다.

기여 방법

* 문서 변환 개선
* 메타데이터 수정
* 누락 문서 추가
* 파서 개발
* 검색 및 API 개발

Pull Request를 환영합니다.

---

# 프로젝트 비전

GovKR-MD는 장기적으로 **대한민국 공공 행정 문서의 Markdown 아카이브**를 구축하는 것을 목표로 합니다.

이를 통해 다음과 같은 가능성이 열립니다.

* 정책 변경 diff 분석
* 법령 변화 추적
* 시민 기술(Civic Tech) 도구
* AI 기반 정책 분석
* 공공 데이터 지식 그래프

---

# License

이 프로젝트는 **CC0 1.0 Universal** 라이선스를 사용합니다.

모든 문서는 최대한 자유로운 재사용을 위해 퍼블릭 도메인으로 공개됩니다.

자세한 내용은 LICENSE 파일을 참고하세요.
