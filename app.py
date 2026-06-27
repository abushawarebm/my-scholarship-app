import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Scholarship Explorer", layout="centered")

# 2. Translation Dictionary
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

# 3. Live URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1cW5YWrR0kj6XEpyKQ1x3wmvCqFIJGYoJneQaRyXDnu4/export?format=csv"

@st.cache_data(ttl=10) # تقليل وقت الكاش للتحديث الفوري
def load_data():
    df = pd.read_csv(SHEET_URL)
    # تنظيف أسماء الأعمدة من أي مسافات زائدة قد تسبب خطأ
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
    
    total_scholarships = len(df)
    st.metric(label=t["total"], value=total_scholarships)
    
    st.divider()

    # محاولة العثور على عمود المرحلة الدراسية بمرونة
    degree_col = 'Degree Type' if 'Degree Type' in df.columns else df.columns[0]
    name_col = 'Name of scholarship' if 'Name of scholarship' in df.columns else df.columns[1]

    degree_options = df[degree_col].dropna().unique().tolist()
    selected_degree = st.selectbox(t["select_degree"], options=degree_options)

    filtered_df = df[df[degree_col] == selected_degree]
    
    st.subheader(f"{t['available_stage']} ({len(filtered_df)})")
    
    scholarship_list = filtered_df[name_col].tolist()
    selected_scholarship = st.selectbox(t["select_card"], options=scholarship_list)

    if selected_scholarship:
        row = filtered_df[filtered_df[name_col] == selected_scholarship].iloc[0]
        
        st.markdown("---")
        st.success(f"{t['card_title']} {row[name_col]}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"{t['degree']} {row.get(degree_col, 'N/A')}")
            # البحث عن عمود الدولة بمرونة
            country_val = row.get('Country', row.get('Country ', 'N/A'))
            st.write(f"{t['country']} {country_val}")
            st.write(f"{t['deadline']} {row.get('Deadline', 'N/A')}")
        with col2:
            st.write(f"{t['coverage']} {row.get('Scholarship Coverage', 'N/A')}")
            st.write(f"{t['language']} {row.get('Language Proficiency', 'N/A')}")
            
        st.info(f"{t['notes']}\n{row.get('Other relevant notes', 'N/A')}")
        
        link_col = 'Application Link' if 'Application Link' in df.columns else None
        if link_col and pd.notna(row[link_col]):
            st.link_button(t["apply"], row[link_col], use_container_width=True)

except Exception as e:
    st.error(f"{t['error']} {e}")
    st.write("Columns found in your sheet / الأعمدة الموجودة في ملفك حالياً:")
    try:
        st.write(list(pd.read_csv(SHEET_URL).columns))
    except:
        st.write("Unable to read columns. Please ensure 'Publish to Web' is activated.")