import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Scholarship Explorer", layout="centered")

# 2. Translation Dictionary (English, العربية, Nederlands)
translations = {
    "English": {
        "title": "🎓 Smart Scholarship Explorer",
        "subtitle": "Explore and filter available scholarships based on your degree type.",
        "total": "📊 Total Available Scholarships",
        "select_degree": "Select Degree Type:",
        "available_stage": "Available Scholarships for this stage",
        "select_card": "Click below to open a Detailed Card:",
        "card_title": "📜 Scholarship Detailed Card:",
        "degree": "🎓 Degree Type:",
        "country": "🌍 Country:",
        "deadline": "⏳ Deadline:",
        "coverage": "💰 Scholarship Coverage:",
        "language": "🗣️ Language Proficiency:",
        "notes": "📝 Relevant Notes:",
        "apply": "🔗 Apply Now",
        "error": "Error loading live data from Google Sheets. Details:"
    },
    "العربية": {
        "title": "🎓 مستكشف المنح الدراسية الذكي",
        "subtitle": "ابحث وتصفح المنح الدراسية المتاحة بناءً على المرحلة الدراسية.",
        "total": "📊 إجمالي المنح المتاحة",
        "select_degree": "اختر المرحلة الدراسية:",
        "available_stage": "المنح المتاحة لهذه المرحلة",
        "select_card": "اضغط هنا لاختيار منحة وعرض بطاقة التفاصيل:",
        "card_title": "📜 بطاقة تفاصيل المنحة:",
        "degree": "🎓 المرحلة الدراسية:",
        "country": "🌍 الدولة:",
        "deadline": "⏳ الموعد النهائي:",
        "coverage": "💰 التغطية المالية:",
        "language": "🗣️ الشروط اللغوية:",
        "notes": "📝 ملاحظات هامة:",
        "apply": "🔗 قدم الآن",
        "error": "حدث خطأ أثناء تحميل البيانات المباشرة من جداول جوجل. التفاصيل:"
    },
    "Nederlands": {
        "title": "🎓 Slimme Beurzenzoeker",
        "subtitle": "Bekijk en filter beschikbare beurzen op basis van je studieniveau.",
        "total": "📊 Totaal Aantal Beschikbare Beurzen",
        "select_degree": "Selecteer Studieniveau:",
        "available_stage": "Beschikbare beurzen voor dit niveau",
        "select_card": "Klik hieronder om een gedetailleerde kaart te openen:",
        "card_title": "📜 Gedetailleerde Beurzenkaart:",
        "degree": "🎓 Studieniveau:",
        "country": "🌍 Land:",
        "deadline": "⏳ Deadline:",
        "coverage": "💰 Dekking van de Beurs:",
        "language": "🗣️ Taalvaardigheid:",
        "notes": "📝 Belangrijke Opmerkingen:",
        "apply": "🔗 Nu Solliciteren",
        "error": "Fout bij het laden van live gegevens van Google Sheets. Details:"
    }
}

lang = st.selectbox("🌐 Choose Language / اختر اللغة / Kies Taal", ["English", "العربية", "Nederlands"])
t = translations[lang]

st.title(t["title"])
st.markdown(t["subtitle"])

# 3. 🔗 رابط ملف Google Sheets الخاص بك بعد تحويله لصيغة CSV التلقائية
SHEET_URL = "https://docs.google.com/spreadsheets/d/1cW5YWrR0kj6XEpyKQ1x3wmvCqFIJGYoJneQaRyXDnu4/export?format=csv"

@st.cache_data(ttl=60) # تحديث تلقائي كل 60 ثانية في حال عدلت على الجدول
def load_data():
    df = pd.read_csv(SHEET_URL)
    return df

try:
    df = load_data()
    
    total_scholarships = len(df)
    st.metric(label=t["total"], value=total_scholarships)
    
    st.divider()

    degree_options = df['Degree Type'].dropna().unique().tolist()
    selected_degree = st.selectbox(t["select_degree"], options=degree_options)

    filtered_df = df[df['Degree Type'] == selected_degree]
    
    st.subheader(f"{t['available_stage']} ({len(filtered_df)})")
    
    scholarship_list = filtered_df['Name of scholarship'].tolist()
    selected_scholarship = st.selectbox(t["select_card"], options=scholarship_list)

    if selected_scholarship:
        row = filtered_df[filtered_df['Name of scholarship'] == selected_scholarship].iloc[0]
        
        st.markdown("---")
        st.success(f"{t['card_title']} {row['Name of scholarship']}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"{t['degree']} {row['Degree Type']}")
            st.write(f"{t['country']} {row['Country '] if 'Country ' in row else row.get('Country', 'N/A')}")
            st.write(f"{t['deadline']} {row['Deadline']}")
        with col2:
            st.write(f"{t['coverage']} {row['Scholarship Coverage']}")
            st.write(f"{t['language']} {row['Language Proficiency']}")
            
        st.info(f"{t['notes']}\n{row['Other relevant notes']}")
        
        if pd.notna(row['Application Link']):
            st.link_button(t["apply"], row['Application Link'], use_container_width=True)

except Exception as e:
    st.error(f"{t['error']} {e}")