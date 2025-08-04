import streamlit as st
import pandas as pd
import ast
from utils.openai_helper import generate_ad_copies

st.set_page_config(page_title="모바일 게임 광고 카피 생성기", layout="wide")

st.markdown(
    """
    <h2 style='text-align: center; color: #FF4B4B;'>🎮 모바일 게임 광고 카피 생성기</h2>
    <p style='text-align: center; font-size:16px;'>
    광고 카피를 빠르고 다양하게 생성하세요
    </p>
    """, 
    unsafe_allow_html=True
)
st.markdown("---")

# ---- 레이아웃: 좌(입력) / 우(결과) ---- #
left_col, right_col = st.columns([1, 2])

# ---- 왼쪽: 입력 폼 ---- #
with left_col:
    with st.form("ad_form"):
        st.subheader("⚙️ 광고 설정")
        product_name = st.text_input("게임명", "드래곤 퀘스트")
        target_audience = st.text_input("타겟 오디언스", "20~30대 남성 게이머")
        game_genre = st.selectbox("게임 장르", ["RPG", "FPS", "퍼즐", "전략", "MMORPG", "레이싱"])
        highlight = st.multiselect(
            "광고에서 강조할 포인트", 
            ["PvP 경쟁", "보상 시스템", "그래픽", "스토리라인", "빠른 성장", "실시간 전투", "친구와 협동"]
        )
        tone = st.selectbox("광고 톤/스타일", ["설득력 있는", "재미있는", "짜릿한", "흥미진진", "모험심 자극"])
        num_ads = st.slider("생성할 광고 개수", 5, 20, 5)

        submitted = st.form_submit_button("🚀 광고 카피 생성")

# ---- 오른쪽: 결과 ---- #
with right_col:
    if submitted:
        ads_text = generate_ad_copies(product_name, target_audience, tone, num_ads, game_genre, highlight)
        try:
            ads = ast.literal_eval(ads_text)
            df = pd.DataFrame(ads)

            st.success(f"✅ {len(df)}개의 광고 카피가 생성되었습니다!")

            # 결과 카드 출력
            for i, row in df.iterrows():
                st.markdown(
                    f"""
                    <div style='background-color:#f9f9f9; padding:20px; 
                                border-radius:15px; margin-bottom:15px;
                                box-shadow: 0 2px 6px rgba(0,0,0,0.05);'>
                        <h4 style='color:#FF4B4B;'>📢 {row['headline']}</h4>
                        <p style='font-size:15px;'>{row['description']}</p>
                        <p style='color:#555; font-weight:bold;'>{row['call_to_action']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # CSV 다운로드 버튼
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 CSV 다운로드", data=csv, file_name="ads_copy.csv", mime="text/csv")
        except Exception as e:
            st.error(f"응답 처리 오류: {e}")
            st.text(ads_text)
