#!/usr/bin/env python3
"""
law.go.kr 법령 크롤러 - Playwright 버전
법제처 웹사이트에서 법령 데이터를 Playwright로 스크래핑합니다.

설치:
    pip install playwright requests beautifulsoup4
    playwright install chromium

사용법:
    python crawler/lawgo.py --id 241478
    python crawler/lawgo.py --url "https://law.go.kr/LSW/lsInfoP.do?lsiSeq=241478"
"""

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Playwright 선택적 import
try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

from bs4 import BeautifulSoup

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs" / "laws"


class LawGoKrCrawler:
    """법제처 법령 크롤러 - Playwright 기반"""

    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or DOCS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

        if not HAS_PLAYWRIGHT:
            print("❌ Playwright가 설치되지 않았습니다.")
            print("   pip install playwright")
            print("   playwright install chromium")
            sys.exit(1)

    def get_law_detail(self, law_id: str) -> dict:
        """법령 상세 정보 수집 - Playwright 사용"""
        print(f"📖 법령 ID {law_id} 수집 중...")

        url = f"https://law.go.kr/LSW/lsInfoP.do?lsiSeq={law_id}"

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()

                # 타임아웃 늘리기
                page.set_default_timeout(60000)

                # 페이지 로드 - domcontentloaded만 기다림
                page.goto(url, wait_until="domcontentloaded")

                # JavaScript 실행 대기
                page.wait_for_timeout(5000)

                # HTML 가져오기
                html = page.content()
                browser.close()

            # BeautifulSoup으로 파싱
            soup = BeautifulSoup(html, "html.parser")
            law_data = self._extract_metadata(soup, law_id)
            law_data["articles"] = self._extract_articles(soup)

            print(f"   제목: {law_data.get('title', 'N/A')}")
            print(f"   조문: {len(law_data.get('articles', []))}개")

            return law_data

        except Exception as e:
            print(f"❌ 수집 실패: {e}")
            return None

    def _extract_metadata(self, soup: BeautifulSoup, law_id: str) -> dict:
        """HTML에서 메타데이터 추출"""
        metadata = {
            "law_id": f"LS_{law_id}",
            "source_url": f"https://law.go.kr/LSW/lsInfoP.do?lsiSeq={law_id}"
        }

        # 방법1: HTML 선택자
        title_selectors = [
            "h2.title", ".law_tt", ".view_tit", "#viewTitleDiv h2",
            ".pg_title h2", "h1", "strong.law_nm"
        ]
        for selector in title_selectors:
            elem = soup.select_one(selector)
            if elem:
                title = elem.get_text(strip=True)
                if title and len(title) > 2 and not title.startswith("법령"):
                    metadata["title"] = title
                    break

        # 방법2: 텍스트에서 추출 (가장 신뢰할 수 있는 방법)
        if not metadata.get("title"):
            body = soup.get_text(separator='\n')
            lines = [l.strip() for l in body.split('\n') if l.strip()]

            # 처음 50줄에서 법령명 패턴 찾기
            for line in lines[:50]:
                # "- 법령명" 또는 그냥 "법령명" 패턴
                clean_line = re.sub(r'^[-\s]+', '', line)
                clean_line = re.sub(r'\[.*?\]', '', clean_line).strip()

                # 법령명 패턴: 한글 + (법률|법|령|규칙|조례)
                if re.match(r'^[가-힣]+(?:법률|법|령|규칙|조례|규정|시행령|시행규칙)$', clean_line):
                    if len(clean_line) > 3 and not clean_line.startswith("제"):
                        metadata["title"] = clean_line
                        break

        # 방법3: title 태그
        if not metadata.get("title"):
            title_tag = soup.select_one("title")
            if title_tag:
                title = title_tag.get_text(strip=True)
                title = re.sub(r'\s*[\|｜].*$', '', title)
                if title and len(title) > 2:
                    metadata["title"] = title

        # 메타 정보 추출
        body_text = soup.get_text()
        self._parse_meta_from_text(metadata, body_text)

        return metadata

    def _parse_meta_item(self, metadata: dict, key: str, value: str):
        """메타데이터 항목 파싱"""
        key_lower = key.strip().lower()
        value = value.strip()

        if not value:
            return

        if "소관부처" in key_lower or "주무부처" in key_lower:
            metadata["ministry"] = value
        elif "공포일" in key_lower:
            metadata["promulgation_date"] = self._parse_date(value)
        elif "시행일" in key_lower:
            metadata["enforcement_date"] = self._parse_date(value)
        elif "공포번호" in key_lower:
            metadata["law_serial"] = value
        elif "조문수" in key_lower:
            match = re.search(r'\d+', value)
            if match:
                metadata["total_articles"] = int(match.group())

    def _parse_meta_from_text(self, metadata: dict, text: str):
        """텍스트에서 메타데이터 추출"""
        patterns = {
            "ministry": r'(?:소관부처|주무부처)[:\s]*(.+?)(?:\n|$)',
            "promulgation_date": r'공포일[:\s]*(\d{4}[.\-]?\d{1,2}[.\-]?\d{1,2})',
            "enforcement_date": r'시행일[:\s]*(\d{4}[.\-]?\d{1,2}[.\-]?\d{1,2})',
            "law_serial": r'공포번호[:\s]*(.+?)(?:\n|$)',
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, text)
            if match:
                value = match.group(1).strip()
                if key in ["promulgation_date", "enforcement_date"]:
                    value = self._parse_date(value)
                metadata[key] = value

    def _extract_articles(self, soup: BeautifulSoup) -> list:
        """HTML에서 조문 추출"""
        articles = []

        # 조문 영역 찾기
        content_selectors = [
            "#viewBodyDiv", ".law_con", ".pg_group", ".law_content",
            "#lawContent", ".article_area", "#cont"
        ]

        content_area = None
        for selector in content_selectors:
            content_area = soup.select_one(selector)
            if content_area:
                break

        if not content_area:
            content_area = soup

        # 텍스트 추출
        text = content_area.get_text(separator='\n')

        # 불필요한 텍스트 제거
        text = re.sub(r'댓글\s*\d+', '', text)
        text = re.sub(r'인쇄|공유|스크랩', '', text)

        # 조문 패턴: 제X조, 제X조의X
        # 장/절 헤더도 포함
        lines = text.split('\n')
        current_article = None
        current_content = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 조 시작 확인
            article_match = re.match(r'^(제\d+조(?:의\d+)?)\s*(?:\(([^)]+)\))?(.*)$', line)

            if article_match:
                # 이전 조 저장
                if current_article:
                    articles.append(current_article)

                # 새 조 시작
                current_article = {
                    "number": article_match.group(1),
                    "title": article_match.group(2) or "",
                    "content": article_match.group(3).strip() if article_match.group(3) else ""
                }
            elif current_article:
                # 현재 조에 내용 추가
                current_article["content"] += " " + line

        # 마지막 조 추가
        if current_article:
            articles.append(current_article)

        # 내용 정리
        for article in articles:
            article["content"] = re.sub(r'\s+', ' ', article["content"]).strip()

        return articles[:500]  # 최대 500조

    def _parse_date(self, date_str: str) -> str:
        """날짜 파싱 → YYYY-MM-DD"""
        date_str = re.sub(r'\s+', '', date_str)
        match = re.search(r'(\d{4})[.\-년]?(\d{1,2})[.\-월]?(\d{1,2})', date_str)
        if match:
            return f"{match.group(1)}-{match.group(2).zfill(2)}-{match.group(3).zfill(2)}"
        return date_str

    def to_markdown(self, law_data: dict) -> str:
        """법령 데이터를 Markdown으로 변환"""
        if not law_data:
            return ""

        lines = []

        # Frontmatter
        lines.append("---")
        lines.append(f"law_id: {law_data.get('law_id', 'UNKNOWN')}")
        if law_data.get('title'):
            lines.append(f"title: {law_data['title']}")
        lines.append("law_type: law")
        if law_data.get('ministry'):
            lines.append(f"ministry: {law_data['ministry']}")
        if law_data.get('promulgation_date'):
            lines.append(f"promulgation_date: {law_data['promulgation_date']}")
        if law_data.get('enforcement_date'):
            lines.append(f"enforcement_date: {law_data['enforcement_date']}")
        if law_data.get('law_serial'):
            lines.append(f"law_serial: {law_data['law_serial']}")
        if law_data.get('total_articles'):
            lines.append(f"total_articles: {law_data['total_articles']}")
        lines.append(f"source_url: {law_data.get('source_url', '')}")
        lines.append("status: 시행")
        lines.append("---")
        lines.append("")

        # 제목
        if law_data.get('title'):
            lines.append(f"# {law_data['title']}")
            lines.append("")

        # 조문
        for article in law_data.get('articles', []):
            title_part = f" ({article['title']})" if article.get('title') else ""
            lines.append(f"## {article['number']}{title_part}")
            lines.append("")
            if article.get('content'):
                lines.append(article['content'])
                lines.append("")

        return "\n".join(lines)

    def save_law(self, law_data: dict) -> Path:
        """법령을 파일로 저장"""
        if not law_data or not law_data.get('title'):
            print("❌ 저장 실패: 데이터 없음")
            return None

        law_id = law_data.get('law_id', 'UNKNOWN')
        title = law_data.get('title', 'unknown')

        # 파일명 정규화
        safe_title = re.sub(r'[^\w\s가-힣-]', '', title)
        safe_title = re.sub(r'\s+', '_', safe_title)[:50]

        # 폴더 생성
        folder = self.output_dir / f"{law_id}_{safe_title}"
        folder.mkdir(parents=True, exist_ok=True)

        # 파일 저장
        filepath = folder / f"{law_id}_{safe_title}.md"
        markdown = self.to_markdown(law_data)

        filepath.write_text(markdown, encoding='utf-8')
        print(f"✅ 저장: {filepath.name}")

        return filepath

    def fetch_by_url(self, url: str) -> dict:
        """URL로 법령 수집"""
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)

        if "lsiSeq" in qs:
            return self.get_law_detail(qs["lsiSeq"][0])
        else:
            print("❌ URL에 lsiSeq 파라미터가 없습니다")
            return None

    def batch_fetch(self, law_ids: list):
        """여러 법령 일괄 수집"""
        for law_id in law_ids:
            try:
                law_data = self.get_law_detail(law_id)
                if law_data:
                    self.save_law(law_data)
            except Exception as e:
                print(f"❌ {law_id} 실패: {e}")


def main():
    parser = argparse.ArgumentParser(description="law.go.kr 법령 크롤러 (Playwright)")
    parser.add_argument("--id", "-i", help="법령 ID (lsiSeq)")
    parser.add_argument("--url", "-u", help="법령 URL")
    parser.add_argument("--batch", "-b", help="법령 ID 목록 (쉼표 구분)")
    parser.add_argument("--output", "-o", help="출력 디렉토리")

    args = parser.parse_args()

    crawler = LawGoKrCrawler(Path(args.output) if args.output else DOCS_DIR)

    if args.batch:
        # 일괄 수집
        law_ids = [x.strip() for x in args.batch.split(",")]
        crawler.batch_fetch(law_ids)
    elif args.url:
        law_data = crawler.fetch_by_url(args.url)
        if law_data:
            crawler.save_law(law_data)
    elif args.id:
        law_data = crawler.get_law_detail(args.id)
        if law_data:
            crawler.save_law(law_data)
    else:
        print("""
법령 크롤러 사용법 (Playwright 버전):

1. ID로 수집:
   python crawler/lawgo.py --id 241478

2. URL로 수집:
   python crawler/lawgo.py --url "https://law.go.kr/...lsiSeq=241478"

3. 일괄 수집:
   python crawler/lawgo.py --batch "2164,241478,239843"

설치:
   pip install playwright
   playwright install chromium

법령 ID 예시:
  - 헌법: 2164
  - 민법: 242146
  - 형법: 239843
  - 개인정보보호법: 241478
  - 도로교통법: 241038
        """)


if __name__ == "__main__":
    main()
