import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# 1. إعدادات الصفحة
st.set_page_config(page_title="Scholarship Explorer", layout="centered")

# 2. قاموس الترجمة للغات الثلاث
translations = {
    "English": {
        "title": "🎓 Smart Scholarship Explorer",
        "subtitle": "Explore and filter available scholarships based on status and degree type.",
        "total": "📊 Total Available Scholarships",
        "filter_status": "🔍 Filter by Scholarship Status:",
        "all_status": "All Scholarships",
        "active_status": "🟢 Active Only",
        "expired_status": "🔴 Expired Only",
        "select_degree": "Select Degree Type:",
        "available_stage": "Available Scholarships matching your filters",
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
        "expired": "⚠️ Application Closed / Expired",
        "months": "Months",
        "days": "Days",
        "left": "Time Remaining"
    },
    "العربية": {
        "title": "🎓 مستكشف المنح الدراسية الذكي",
        "subtitle": "ابحث وتصفح المنح الدراسية المتاحة مع تصفية حية حسب الحالة والمرحلة الدراسية.",
        "total": "📊 إجمالي المنح المتاحة",
        "filter_status": "🔍 تصفية حسب حالة المنحة:",
        "all_status": "كل المنح",
        "active_status": "🟢  النشطة فقط",
        "expired_status": "🔴 المنتهية فقط",
        "select_degree": "اختر المرحلة الدراسية:",
        "available_stage": "المنح المتاحة المتوافقة مع الفلاتر",
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
        "expired": "⚠️ انتهى التقديم / أُغلقت المنحة رسمياً",
        "months": "شهر",
        "days": "يوم",
        "left": "الوقت المتبقي لانتهاء التقديم"
    },
    "Nederlands": {
        "title": "🎓 Slimme Beurzenzoeker",
        "subtitle": "Bekijk en filter beschikbare beurzen op basis van status en studieniveau.",
        "total": "📊 Totaal Aantal Beschikbare Beurzen",
        "filter_status": "🔍 Filter op Beursstatus:",
        "all_status": "Alle Beurzen",
        "active_status": "🟢 Alleen Actief",
        "expired_status": "🔴 Alleen Verlopen",
        "select_degree": "Selecteer Studieniveau:",
        "available_stage": "Beschikbare beurzen die aan de filters voldoen",
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
        "expired": "⚠️ Aanmelding gesloten / Verlopen",
        "months": "Maanden",
        "days": "Dagen",
        "left": "Resterende Tijd"
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

# دالة حساب العداد الزمني بالأشهر والأيام
def calculate_countdown_details(deadline_str):
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
        if deadline_date <= now:
            return "expired"
            
        diff = relativedelta(deadline_date, now)
        
        parts = []
        if diff.months > 0:
            parts.append(f"{diff.months} {t['months']}")
        if diff.days > 0:
            parts.append(f"{diff.days} {t['days']}")
            
        if not parts:
            return "⏳ أقل من يوم"
            
        return " و ".join(parts)
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

    # إضافة فلاتر التحكم
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        status_filter = st.selectbox(t["filter_status"], options=[t["all_status"], t["active_status"], t["expired_status"]])
    with col_f2:
        degree_options = [opt for opt in df[degree_col].unique() if opt != t["na"]]
        selected_degree = st.selectbox(t["select_degree"], options=degree_options)

    # حساب الحالة الحية والملصقات
    live_statuses = []
    display_names = []
    for idx, row in df.iterrows():
        deadline_val = row.get('Deadline', t['na'])
        countdown = calculate_countdown_details(deadline_val)
        is_expired_by_script = status_col and "expired" in str(row.get(status_col, '')).lower()
        
        if is_expired_by_script or countdown == "expired":
            current_status = "expired"
            label = f"🔴 {row[name_col]} ({t['expired']})"
        else:
            current_status = "active"
            label = f"🟢 {row[name_col]} (⏳ متبقي {countdown if countdown else ''})"
            
        live_statuses.append(current_status)
        display_names.append(label)
        
    df['calculated_status'] = live_statuses
    df['display_name_label'] = display_names

    # تصفية البيانات
    filtered_df = df[df[degree_col] == selected_degree]
    if status_filter == t["active_status"]:
        filtered_df = filtered_df[filtered_df['calculated_status'] == "active"]
    elif status_filter == t["expired_status"]:
        filtered_df = filtered_df[filtered_df['calculated_status'] == "expired"]

    st.subheader(f"{t['available_stage']} ({len(filtered_df)})")
    
    scholarship_options = filtered_df['display_name_label'].tolist()
    selected_display_name = st.selectbox(t["select_card"], options=scholarship_options)

    if selected_display_name:
        row = filtered_df[filtered_df['display_name_label'] == selected_display_name].iloc[0]
        
        st.markdown("---")
        st.success(f"{t['card_title']} {row[name_col]}")
        
        # ⏱️ عرض العداد الزمني بشكل ضخم واحترافي داخل البطاقة
        deadline_val = row.get('Deadline', t['na'])
        countdown_result = calculate_countdown_details(deadline_val)
        
        if row['calculated_status'] == "expired":
            st.error(t["expired"])
        elif countdown_result:
            st.metric(label=t["left"], value=f"⏳ {countdown_result}")
            st.divider()
            
        # تفاصيل المنحة في أعمدة
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