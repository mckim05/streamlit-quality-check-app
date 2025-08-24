import streamlit as st
import pandas as pd

st.set_page_config(page_title="출하 품질 검사", layout="wide")
st.title("출하 품질 검사 결과")

# 1. 파일 업로드
uploaded_file = st.file_uploader("측정값 CSV 업로드", type=["csv"])

if uploaded_file is not None:
    # 2. CSV 읽기
    df = pd.read_csv(uploaded_file, encoding = 'cp949')
    df.columns = df.columns.str.strip()  # 컬럼 공백 제거

    st.subheader("원본 데이터")
    st.dataframe(df)

    # 3. 검사 규격
    spec = {
        "치수1": (9.8, 10.2),
        "치수2": (4.9, 5.1)
    }

    # 4. 컬럼 존재 여부 확인
    missing_cols = [col for col in spec.keys() if col not in df.columns]
    if missing_cols:
        st.error(f"데이터에 없는 컬럼: {', '.join(missing_cols)}")
    else:
        # 5. Pass/Fail 계산 (벡터화)
        for col, (low, high) in spec.items():
            df[col + "_합불"] = df[col].apply(lambda x: "Pass" if low <= x <= high else "Fail")

        # 6. 종합합불 계산
        df["종합합불"] = df[[col for col in df.columns if "_합불" in col]]\
                           .apply(lambda x: "Fail" if (x=="Fail").any() else "Pass", axis=1)

        st.subheader("합불 결과")
        st.dataframe(df, use_container_width=True)

        # 7. 총 검사 건수 / 불합격 건수
        total_count = len(df)
        fail_count = (df["종합합불"]=="Fail").sum()

        col1, col2 = st.columns(2)
        col1.metric("총 검사 건수", total_count)
        col2.metric("불합격 건수", fail_count)
else:
    st.info("CSV 파일을 업로드해주세요.")
