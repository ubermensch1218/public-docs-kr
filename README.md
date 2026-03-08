# 🇰🇷 GovKR-MD

대한민국 정부 문서 Markdown 아카이브
Korean Government Documents in Markdown

GovKR-MD는 대한민국의 정부 문서를 **Markdown 형식으로 변환하여 공개 저장소로 관리하는 오픈소스 프로젝트**입니다.

---

## 현재 단계 (Phase 1)

> **법령 변환부터 시작합니다.**

초기 단계에서는 **[법제처 law.go.kr](https://law.go.kr)**의 법령 데이터를
구조화된 Markdown으로 변환하는 데 집중합니다.

이유:
- 법령은 구조가 명확 (조/항/호/목)
- 데이터가 안정적
- 프로젝트 신뢰도 확보

---

## 프로젝트 목표

- [x] 법령 Markdown 스키마 설계
- [ ] law.go.kr 크롤러 개발
- [ ] HTML → Markdown 파서
- [ ] 샘플 법령 100개 변환
- [ ] public 전환

---

## Repository Structure

```
govkr-md/
├── README.md
├── LICENSE
├── SCHEMA.md              # 일반 문서 스키마
├── SCHEMA-LAW.md          # 법령 전용 스키마 ⭐
├── ROADMAP.md
│
├── crawler/
│   └── lawgo.py           # law.go.kr 크롤러
│
├── parser/
│   └── html_to_md.py      # HTML → Markdown 변환
│
├── docs/
│   └── laws/              # 법령 문서
│       └── LS_2011_6258_개인정보보호법/
│           └── LS_2011_6258_개인정보보호법.md
│
└── scripts/
    └── ...                # 유틸리티
```

---

## 법령 스키마

법령은 일반 문서와 다른 특수 구조를 가집니다.

### 조문 계층 구조

```
조 (Article)
  └ 항 (Paragraph): ①, ②, ③
      └ 호 (Item): 1., 2., 3.
          └ 목 (Sub-item): 가., 나., 다.
```

### 샘플

```yaml
---
law_id: LS_2011_6258
title: 개인정보 보호법
law_type: law
ministry: 행정안전부
promulgation_date: 2011-03-29
last_amendment: 2024-03-20
source_url: https://law.go.kr/...
---
```

```markdown
## 제1조 (목적)

이 법은 개인정보의 보호에 관한 사항을 정함으로써...

## 제2조 (정의)

① 이 법에서 사용하는 용어의 뜻은 다음과 같다.

1. "개인정보"란 ...
   가. 성명, 주민등록번호 ...
   나. 해당 정보만으로는 ...
```

자세한 스키마는 **[SCHEMA-LAW.md](./SCHEMA-LAW.md)**를 참조하세요.

---

## 왜 Markdown인가?

- 장기 보존에 유리한 단순한 포맷
- Git 기반 버전 관리 가능
- 협업 수정 (Pull Request) 가능
- 기계 처리 및 분석 용이
- 정적 사이트 생성 가능

---

## 프로젝트 비전

이 프로젝트는 장기적으로 다음을 목표로 합니다:

- 법령 변경 diff 분석
- 개정 이력 추적
- 시민 기술 (Civic Tech) 도구
- AI 기반 법령 분석
- 공공 데이터 지식 그래프

---

## 기여 방법

현재는 초기 개발 단계입니다. 다음과 같은 기여를 환영합니다:

- 크롤러 개발
- 파서 개선
- 스키마 제안
- 샘플 문서 추가

---

## License

**CC0 1.0 Universal**

모든 문서는 최대한 자유로운 재사용을 위해 퍼블릭 도메인으로 공개됩니다.

---

## 참고 자료

- [법제처 법령공포시스템](https://law.go.kr)
- [OASIS Akoma Ntoso](http://docs.oasis-open.org/legaldocml/akoma-ntoso/) (국제 법률 마크업 표준)
- [USLM](https://github.com/usgpo/uslm) (미국 법률 마크업)
