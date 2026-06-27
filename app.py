import streamlit as st
import pandas as pd

# 1. تهيئة إعدادات الصفحة
st.set_page_config(page_title="مستكشف المنح الدراسية", layout="centered")

st.title("🎓 مستكشف المنح الدراسية الذكي")
st.markdown("ابحث وتصفح المنح الدراسية المتاحة بناءً على المرحلة الدراسية.")

# 2. دالة قراءة ملف الـ CSV الجديد (تم تعديلها لقراءة pandas من نوع csv)
@st.cache_data
def load_data():
    # يقرأ الملف المرفوع في نفس المجلد على جيتهاب
    df = pd.read_csv("Book2.csv")
    return df

try:
    df = load_data()
    
    # 3. عرض إجمالي عدد المنح في الأعلى
    total_scholarships = len(df)
    st.metric(label="📊 إجمالي المنح المتاحة", value=total_scholarships)
    
    st.divider()

    # 4. القائمة المنسدلة لاختيار المرحلة الدراسية
    degree_options = df['Degree Type'].dropna().unique().tolist()
    selected_degree = st.selectbox("اختر المرحلة الدراسية:", options=degree_options)

    # 5. تصفية البيانات بناءً على الاختيار
    filtered_df = df[df['Degree Type'] == selected_degree]
    
    st.subheader(f"المنح المتاحة لهذه المرحلة ({len(filtered_df)})")
    
    # 6. قائمة اختيار منحة معينة لعرض تفاصيلها
    scholarship_list = filtered_df['Name of scholarship'].tolist()
    selected_scholarship = st.selectbox("اضغط هنا لاختيار منحة وعرض بطاقة التفاصيل:", options=scholarship_list)

    # 7. عرض بطاقة تفاصيل المنحة المحددة
    if selected_scholarship:
        row = filtered_df[filtered_df['Name of scholarship'] == selected_scholarship].iloc[0]
        
        st.markdown("---")
        st.success(f"📜 **بطاقة تفاصيل المنحة: {row['Name of scholarship']}**")
        
        # تنظيم التفاصيل في أعمدة
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"🎓 **المرحلة الدراسية:** {row['Degree Type']}")
            st.write(f"🌍 **الدولة:** {row['Country '] if 'Country ' in row else row.get('Country', 'N/A')}")
            st.write(f"⏳ **الموعد النهائي:** {row['Deadline']}")
        with col2:
            st.write(f"💰 **التغطية المالية:** {row['Scholarship Coverage']}")
            st.write(f"🗣️ **الشروط اللغوية:** {row['Language Proficiency']}")
            
        st.info(f"📝 **ملاحظات هامة:**\n{row['Other relevant notes']}")
        
        # زر تفاعلي للتقديم
        if pd.notna(row['Application Link']):
            st.link_button("🔗 قدم الآن", row['Application Link'], use_container_width=True)

except Exception as e:
    st.error(f"تأكد من وجود ملف 'Book2.csv' في نفس المجلد على جيتهاب. تفاصيل الخطأ: {e}")