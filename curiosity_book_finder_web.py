import streamlit as st
import requests
from urllib.parse import quote_plus

GOOGLE_BOOKS_API = "https://www.googleapis.com/books/v1/volumes?q="

# 서귀포시 도서관 소장 여부 확인 (단순 매칭 시뮬레이션)
def check_library_availability(title):
    library_books = [
        "태권도 교본",
        "스포츠 심리학 입문"
    ]
    return title in library_books

# 온라인 구매 링크 생성
def suggest_online_links(title):
    search_query = quote_plus(title)
    yes24_link = f"https://www.yes24.com/Product/Search?domain=ALL&query={search_query}"
    kyobo_link = f"https://search.kyobobook.co.kr/web/search?vPstrKeyWord={search_query}"
    return yes24_link, kyobo_link

# Google Books API를 통해 도서 검색
def search_books_google(keywords):
    query = '+'.join(quote_plus(kw) for kw in keywords)
    url = GOOGLE_BOOKS_API + query

    try:
        response = requests.get(url, timeout=10)  # 타임아웃 추가
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f"📡 도서 검색 중 오류가 발생했습니다:\n\n{e}")
        return []

    data = response.json()
    books = []
    for item in data.get("items", [])[:3]:
        title = item["volumeInfo"].get("title", "제목 없음")
        info_link = item["volumeInfo"].get("infoLink", "")
        books.append((title, info_link))
    return books

# Streamlit 메인 앱
def main():
    st.set_page_config(page_title="호기심 단어로 책 찾기", layout="centered")
    st.title("📚 호기심 단어로 책 찾기")
    st.write("내 호기심과 연관된 3개의 키워드를 입력하면 관련 도서를 추천해드립니다.")

    keyword_input = st.text_input("키워드 3개를 입력하세요 (쉼표로 구분)", placeholder="예: 정원, 꽃, 장미")

    if st.button("도서 검색") and keyword_input:
        keywords = [k.strip() for k in keyword_input.split(",") if k.strip()]
        if len(keywords) != 3:
            st.warning("⚠️ 정확히 3개의 키워드를 입력해주세요.")
            return

        with st.spinner("🔍 도서를 검색 중입니다..."):
            books = search_books_google(keywords)

        if not books:
            st.error("❌ 도서를 찾을 수 없습니다. 키워드를 다시 입력해 주세요.")
            return

        st.subheader("📖 추천 도서")
        for title, link in books:
            st.markdown(f"### 📘 {title}")
            st.markdown(f"🔗 [책 정보 보러가기]({link})")

            if check_library_availability(title):
                st.success(f"✅ '{title}' 은 서귀포시 공공도서관에 있습니다.")
            else:
                st.error(f"❌ '{title}' 은 서귀포시 공공도서관에 없습니다.")
                yes24, kyobo = suggest_online_links(title)
                st.markdown("🛒 **온라인 구매 링크:**")
                st.markdown(f"- [YES24에서 검색하기]({yes24})")
                st.markdown(f"- [교보문고에서 검색하기]({kyobo})")

if __name__ == "__main__":
    main()