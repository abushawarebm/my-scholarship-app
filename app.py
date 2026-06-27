import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Scholarship Explorer", layout="centered")

# 2. قاموس الترجمة للغات الثلاث (تم تصحيح الأخطاء النصية)
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
        "error": "Error loading live data from Google Sheets. Details:",
        "na": "Not Available",
        "days_left": "Time Remaining:",
        "days": "Days",
        "hours": "Hours",
        "expired": "⚠️ Application Closed / Expired"
    },
    "العربية": {
        "title": "🎓 مستكشف المنح الدراسية الذكي",
        "subtitle": "ابحث وتصفح المنح الدراسية المتاحة بناءً على المرحلة الدراسية مع التحديثات الحية.",
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
        "error": "حدث خطأ أثناء تحميل البيانات المباشرة من جداول جوجل. التفاصيل:",
        "na": "غير متوفر",
        "days_left": "الوقت المتبقي لانتهاء التقديم:",
        "days": "أيام",
        "hours": "ساعة",
        "expired": "⚠️ انتهى التقديم / أُغلقت المنحة رسمياً"
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
        "error": "Fout bij het laden van live gegevens van Google Sheets. Details:",
        "na": "Niet Beschikbaar",
        "days_left": "Resterende tijd:",
        "days": "Dagen",
        "hours": "Uur",
        "expired": "⚠️ Aanmelding gesloten / Verlopen"
    }
}

# اختيار اللغة
lang = st.selectbox("🌐 Choose Language / اختر اللغة / Kies Taal", ["English", "العربية", "Nederlands"])
t = translations[lang]

st.title(t["title"])
st.markdown(t["subtitle"])

# 3. رابط سحب البيانات المباشر من Google Sheets بصيغة CSV
SHEET_URL = "https://docs.google.com/spreadsheets/d/1cW5YWrR0kj6XEpyKQ1x3wmvCqFIJGYoJneQaRyXDnu4/export?format=csv"

@st.cache_data(ttl=10)
def load_cleaned_data():
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.strip()
    
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
        
    df.fillna(t["na"], inplace=True)
    df.replace("nan", t["na"], inplace=True)
    
    if 'Application Link' in df.columns:
        df['Application Link'] = df['Application Link'].apply(
            lambda x: f"https://{x}" if (x != t["na"] and not x.startswith(('http://', 'https://'))) else x
        )
    return df

# دالة حساب العداد الزمني المتبقي للمنحة
def calculate_countdown(deadline_str):
    try:
        for fmt in ('%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%d/%m/%Y'):
            try:
                deadline_date = datetime.strptime(deadline_str, fmt)
                break
            except ValueError:
                continue
        else:
            return None 
            
        now = datetime.now()
        time_left = deadline_date - now
        
        if time_left.total_seconds() <= 0:
            return "expired"
        
        days = time_left.days
        hours = time_left.seconds // 3600
        return f"⏳ {t['days_left']} {days} {t['days']} و {hours} {t['hours']}"
    except:
        return None

try:
    df = load_cleaned_data()
    
    total_scholarships = len(df)
    st.metric(label=t["total"], value=total_scholarships)
    st.divider()

    degree_col = 'Degree Type' if 'Degree Type' in df.columns else df.columns[0]
    name_col = 'Name of scholarship' if 'Name of scholarship' in df.columns else df.columns[1]
    status_col = 'Live Status' if 'Live Status' in df.columns else None

    degree_options = [opt for opt in df[degree_col].unique() if opt != t["na"]]
    selected_degree = st.selectbox(t["select_degree"], options=degree_options)

    filtered_df = df[df[degree_col] == selected_degree]
    st.subheader(f"{t['available_stage']} ({len(filtered_df)})")
    
    scholarship_list = filtered_df[name_col].tolist()
    selected_scholarship = st.selectbox(t["select_card"], options=scholarship_list)

    if selected_scholarship:
        row = filtered_df[filtered_df[name_col] == selected_scholarship].iloc[0]
        
        st.markdown("---")
        st.success(f"{t['card_title']} {row[name_col]}")
        
        deadline_val = row.get('Deadline', t['na'])
        countdown_result = calculate_countdown(deadline_val)
        
        is_expired_by_script = status_col and "expired" in str(row.get(status_col, '')).lower()
        
        if is_expired_by_script or countdown_result == "expired":
            st.error(t["expired"])
        elif countdown_result:
            st.warning(countdown_result)
            
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"{t['degree']} {row.get(degree_col, t['na'])}")
            country_val = row.get('Country', row.get('Country ', t['na']))
            st.write(f"{t['country']} {country_val}")
            st.write(f"{t['deadline']} {deadline_val}")
        with col2:
            st.write(f"{t['coverage']} {row.get('Scholarship Coverage', t['na'])}")
            st.write(f"{t['language']} {row.get('Language Proficiency', t['na'])}")
            
        st.info(f"{t['notes']}\n{row.get('Other relevant notes', t['na'])}")
        
        link_col = 'Application Link' if 'Application Link' in df.columns else None
        if link_col and row[link_col] != t["na"]:
            st.link_button(t["apply"], row[link_col], use_container_width=True)

except Exception as e:
    st.error(f"{t['error']} {e}")