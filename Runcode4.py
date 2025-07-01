import streamlit as st
import pandas as pd
import joblib
from sklearn.metrics import r2_score
import numpy as np
import io

# ============================
# App title
# ============================
st.title("\U0001F3AF Dự đoán Điểm Gốc từ dữ liệu môn học (.csv)")
st.markdown("---")

# ============================
# Upload CSV
# ============================
file = st.file_uploader("Tải lên file CSV chứa thông tin môn học:", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    st.success("✅ Đã đọc file thành công!")
    st.dataframe(df.head())

    # ============================
    # Chọn chế độ nhập thông tin bổ sung
    # ============================
    st.markdown("### 🙋 Chọn phương thức nhập thông tin bổ sung:")
    input_method = st.radio("Chọn cách nhập dữ liệu thiếu:", ["Nhập thủ công", "Hệ thống tự sinh"])

    # ============================
    # Xử lý dữ liệu bổ sung
    # ============================
    if input_method == "Nhập thủ công":
        st.subheader("Bước 2: Nhập dữ liệu riêng cho từng môn học")
        st.info("Bạn có thể nhập giá trị riêng cho từng dòng dữ liệu.")

        for idx in df.index:
            with st.expander(f"Môn học {idx+1} - {df.at[idx, 'course_code']}"):
                df.at[idx, 'weekly_study_hours'] = st.number_input(f"⏱️ Giờ học hàng tuần (dòng {idx+1})", min_value=0.0, value=10.0, key=f"study_{idx}")
                df.at[idx, 'attendance_percentage'] = st.number_input(f"📊 Tỷ lệ chuyên cần (0-100) (dòng {idx+1})", min_value=0.0, max_value=100.0, value=75.0, key=f"att_{idx}")
                df.at[idx, 'commute_time_minutes'] = st.number_input(f"🚶‍♂️ Thời gian đi học (phút) (dòng {idx+1})", min_value=0, value=15, key=f"commute_{idx}")
                fs_level = st.selectbox(f"👪 Mức hỗ trợ gia đình (dòng {idx+1})", ["thấp", "trung bình", "cao", "rất cao"], key=f"support_{idx}")
                mapping = {"thấp": 0, "trung bình": 1, "cao": 2, "rất cao": 3}
                df.at[idx, 'family_support'] = mapping.get(fs_level, 1)

    else:
        st.warning("Hệ thống đang dùng giá trị mặc định.")
        df['weekly_study_hours'] = 10
        df['attendance_percentage'] = 75.0
        df['commute_time_minutes'] = 15
        df['family_support'] = 1

    # ============================
    # Feature Engineering
    # ============================
    attendance_float = pd.to_numeric(df['attendance_percentage'].astype(str).str.replace('%', ''), errors='coerce')
    df['attendance_float'] = attendance_float
    df['study_hours_x_attendance'] = df['weekly_study_hours'] * (attendance_float / 100)
    df['attendance_x_support'] = (attendance_float / 100) * df['family_support']


    subject_type_map = {
        'CS 201': 'general', 'CS 211': 'major', 'MTH 103': 'general', 'PHY 101': 'major',
        'MTH 104': 'general', 'PHI 100': 'general', 'LAW 201': 'general', 'POS 151': 'general',
        'IS 301': 'major', 'CMU-CS 252': 'major', 'CMU-CS 303': 'major', 'CMU-CS 311': 'major',
        'CMU-CS 316': 'major', 'CMU-CS 445': 'major', 'CMU-CS 447': 'major', 'CMU-CS 462': 'major',
        'CMU-SE 100': 'major', 'CMU-SE 214': 'major', 'CMU-SE 252': 'major', 'CMU-SE 303': 'major',
        'CMU-IS 401': 'major', 'CMU-IS 432': 'major', 'IS-ENG 136': 'major', 'IS-ENG 137': 'major',
        'IS-ENG 186': 'major', 'IS-ENG 187': 'major', 'IS-ENG 236': 'major', 'CMU-ENG 130': 'major',
        'CMU-ENG 230': 'major', 'COM 141': 'general', 'COM 142': 'general', 'EVR 205': 'general',
        'CHE 101': 'general', 'HIS 222': 'general', 'MTH 203': 'general', 'MTH 204': 'general',
        'MTH 291': 'major', 'MTH 254': 'major', 'MTH 341': 'major', 'DTE-IS 102': 'major', 'DTE-IS 152': 'major',
        'STA 151': 'general','CMU-CS 246':'major','CMU-CS 297':'major','PHI 150': 'general','CS 464': 'major',
        'CS 466': 'major','POS 361': 'general',
    }
    subject_type_map_numeric = {'major': 2, 'general': 1}
    difficulty_map = {
        'CMU-SE 100': 1,
        'CS 201': 1,
        'CS 211': 2,
        'DTE-IS 102': 1,
        'IS-ENG 136': 2,
        'CHE 101': 2,
        'CMU-CS 252': 1,
        'CMU-CS 311': 3,
        'DTE-IS 152': 1,
        'IS-ENG 137': 2,
        'IS-ENG 186': 2,
        'MTH 103': 3,
        'COM 141': 1,
        'PHY 101': 2,
        'CMU-CS 303': 3,
        'CMU-SE 214': 2,
        'HIS 222': 1,
        'IS-ENG 187': 2,
        'IS-ENG 236': 2,
        'MTH 104': 2,
        'PHI 100': 1,
        'CMU-CS 246': 2,
        'CMU-CS 297': 1,
        'CMU-CS 316': 3,
        'CMU-ENG 130': 2,
        'COM 142': 1,
        'EVR 205': 1,
        'MTH 254': 2,
        'STA 151': 1,
        'CMU-IS 432': 3,
        'CMU-SE 252': 3,
        'CMU-SE 303': 3,
        'IS 301': 3,
        'MTH 291': 2,
        'PHI 150': 1,
        'CMU-CS 445': 3,
        'CMU-CS 447': 2,
        'CMU-CS 462': 3,
        'CMU-ENG 230': 2,
        'CS 464': 3,
        'MTH 203': 2,
        'MTH 204': 2,
        'MTH 341': 2,
        'CMU-IS 401': 3,
        'CS 466': 3,
        'LAW 201': 1,
        'POS 151': 1,
        'POS 361': 1,

    }

    st.success("🎉 Đã tính xong các đặc trưng bổ sung!")

    # ============================
    # Chuyển đổi kiểu dữ liệu phù hợp nếu cần
    # ============================
    df['year'] = df['year'].astype(str)
    df['course_code'] = df['course_code'].astype(str)
    df['study_format'] = df['study_format'].astype(str)
    df['semester_number'] = df['semester_number'].apply(lambda x: 3 if str(x).strip().lower() == 'hè' else pd.to_numeric(x, errors='coerce'))

    # ============================
    # Chọn đúng cột cần thiết cho mô hình
    # ============================
    required_columns = [
        'year', 'course_code', 'study_format', 'semester_number', 'credits_unit',
        'previous_courses_taken', 'previous_credits_earned', 'weekly_study_hours',
        'attendance_percentage', 'commute_time_minutes', 'family_support',
        'study_hours_x_attendance',
        'attendance_x_support', 'expected_difficulty', 'expected_score_hint',
        'fail_rate_general', 'fail_rate_major', 'attendance_gap_general_vs_major',
        'attendance_float', 'mean_score_per_student', 'std_score_per_student',
        'total_courses', 'num_failed_courses', 'subject_type', 'avg_attendance_by_subject_type',
        'gpa_change_rate'
    ]

    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        st.error(f"❌ Thiếu cột cần thiết trong dữ liệu: {missing_cols}")
    else:
        df_predict = df[required_columns].copy()
        cat_cols = ['year', 'course_code', 'study_format']
        num_cols = [c for c in df_predict.columns if c not in cat_cols]
        df_predict[cat_cols] = df_predict[cat_cols].fillna('unknown')
        for col in num_cols:
            if df_predict[col].dtype == 'object':
                continue
            col_data = pd.to_numeric(df_predict[col], errors='coerce').dropna()
            median_val = col_data.median() if not col_data.empty else 0
            df_predict[col] = df_predict[col].replace([np.inf, -np.inf], np.nan)
            df_predict[col] = df_predict[col].fillna(median_val)

        try:
            xgb_model = joblib.load("model_v3/xgb_final_pipeline.joblib")
            mlp_model = joblib.load("model_v3/mlp_final_pipeline.joblib")
            df['predict_xgb'] = xgb_model.predict(df_predict)
            df['predict_mlp'] = mlp_model.predict(df_predict)

            tab1, tab2 = st.tabs(["📋 Dữ liệu & Dự đoán", "📈 Dashboard Phân tích"])

            with tab1:
                st.markdown("### 📄 Bảng dữ liệu sau khi dự đoán")
                st.dataframe(df)
                csv = df.to_csv(index=False)
                st.download_button("📥 Tải kết quả về (.csv)", data=csv, file_name="ket_qua_du_doan.csv", mime="text/csv")
                st.success("✅ Dự đoán thành công! Bạn có thể tải file kết quả bên trên.")

            with tab2:
                st.subheader("📊 Biểu đồ điểm theo thời gian")
                if 'year' in df.columns and 'student_id' in df.columns:
                    df['year'] = df['year'].astype(str)
                    plot_df = df.groupby(['year'])[['predict_xgb', 'predict_mlp']].mean().reset_index()
                    if 'raw_score' in df.columns:
                        raw_score_year = df.groupby(['year'])['raw_score'].mean().reset_index()
                        plot_df = pd.merge(plot_df, raw_score_year, on='year', how='left')
                        plot_df.rename(columns={'raw_score': 'actual_score'}, inplace=True)
                    st.line_chart(plot_df.set_index('year'))

                st.markdown("### 📚 Gợi ý phương pháp học theo tổng thời gian học")
                if 'weekly_study_hours' in df.columns and 'student_id' in df.columns:
                    study_sum = df.groupby('student_id')['weekly_study_hours'].sum().reset_index()
                    for _, row in study_sum.iterrows():
                        sid = row['student_id']
                        hours = row['weekly_study_hours']
                        if hours < 30:
                            strategy = "🔹 **Học thêm mỗi ngày 1 giờ**, tập trung vào môn khó và ôn lại kiến thức cũ."
                        elif hours < 50:
                            strategy = "🔸 **Duy trì đều đặn**, kết hợp luyện đề và học nhóm."
                        else:
                            strategy = "✅ **Phân bố thời gian hợp lý**, tránh học dồn và nghỉ ngơi đầy đủ."
                        st.markdown(f"- 👤 Sinh viên **{sid}** đã học tổng **{hours:.1f} giờ** ➜ {strategy}")

        except Exception as e:
            st.error(f"❌ Lỗi khi nạp mô hình hoặc xử lý dữ liệu: {e}")
else:
    st.info("⬆️ Vui lòng tải lên file CSV để bắt đầu.")
