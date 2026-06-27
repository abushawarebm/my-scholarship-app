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
        "total": "📊 Total Available Scholarships (Filtered)",
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
        "left": "Remaining:",
        "and": "and",
        "less_than_day": "Less than a day left"
    },
    "العربية": {
        "title": "🎓 مستكشف المنح الدراسية الذكي",
        "subtitle": "ابحث وتصفح المنح الدراسية المتاحة مع تصفية حية حسب الحالة والمرحلة الدراسية.",
        "total": "📊 إجمالي المنح المتاحة (المصفاة)",
        "filter_status": "🔍 تصفية حسب حالة المنحة من البداية:",
        "all_status": "كل المنح",
        "active_status": "🟢 النشطة فقط",
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
        "left": "متبقي:",
        "and": "و",
        "less_than_day": "أقل من يوم متبقي"
    },
    "Nederlands": {
        "title": "🎓 Slimme Beurzenzoeker",
        "subtitle": "Bekijk en filter beschikbare beurzen op basis van status en studieniveau.",
        "total": "📊 Totaal Aantal Beschikbare Beurzen (Gefilterd)",
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
        "left": "Resterend:",
        "and": "en",
        "less_than_day": "Minder dan een dag over"
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
    if not deadline_str or deadline_str == t["na"]:
        return None
    try:
        for fmt in ('%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d'):
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
            return f"{t['less_than_day']}"
            
        return f"{t['left']} " + f" {t['and']} ".join(parts)
    except:
        return None

try:
    df = load_cleaned_data()

    degree_col = 'Degree Type' if 'Degree Type' in df.columns else df.columns[0]
    name_col = 'Name of scholarship' if 'Name of scholarship' in df.columns else df.columns[1]
    status_col = 'Live Status' if 'Live Status' in df.columns else None

    # خطوة مسبقة: حساب الحالة والملصقات لكل الصفوف لتطبيق الفلتر الرئيسي أولاً
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
            time_label = f" ({countdown})" if countdown else ""