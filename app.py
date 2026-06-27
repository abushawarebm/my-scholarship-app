import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# 1. إعدادات الصفحة
st.set_page_config(page_title="Scholarship Explorer", layout="centered")

# 2. قاموس الترجمة للغات الثلاث (تم تدقيق النصوص بالكامل)
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
        "expired": "Expired / Closed",
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
        "expired": "منتهية / مغلقة",
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
        "expired": "Verlopen / Gesloten",
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

# دالة حساب العداد الزمني مع دعم شامل ومرن جداً لكل أنواع صيغ التاريخ النصية والرقمية
def calculate_countdown_details(deadline_str, current_translations):
    if not deadline_str or deadline_str == current_translations["na"]:
        return None
    
    # محاولة تنظيف النص وتحويل الشهور المكتوبة نصياً بالإنجليزية إلى أرقام إذا وجدت
    months_map = {"january": "01", "february": "02", "march": "03", "april": "04", "may": "05", "june": "06",
                  "july": "07", "august": "08", "september": "09", "october": "10", "november": "11", "december": "12",
                  "jan": "01", "feb": "02", "mar": "03", "apr": "04", "jun": "06", "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12"}
    
    clean_str = str(deadline_str).lower().strip()
    for m_name, m_num in months_map.items():
        if m_name in clean_str:
            clean_str = clean_str.replace(m_name, m_num)
            
    # قائمة بجميع صيغ التواريخ الممكن إدخالها في جداول البيانات
    date_formats = (
        '%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d',
        '%d %m %Y', '%Y %m %d', '%b %d, %Y', '%B %d, %Y', '%d %b %Y', '%d %B %Y'
    )
    
    try:
        deadline_date = None
        for fmt in date_formats:
            try:
                deadline_date = datetime.strptime(clean_str, fmt)
                break
            except ValueError:
                try:
                    deadline_date = datetime.strptime(str(deadline_str).strip(), fmt)
                    break
                except ValueError:
                    continue
                    
        if deadline_date is None:
            return None 
            
        now = datetime.now()
        if deadline_date <= now:
            return "expired"
            
        diff = relativedelta(deadline_date, now)
        
        parts = []
        if diff.months > 0:
            parts.append(f"{diff.months} {current_translations['months']}")
        if diff.days > 0:
            parts.append(f"{diff.days} {current_translations['days']}")
            
        if not parts:
            return f"{current_translations['less_than_day']}"
            
        return f"{current_translations['left']} " + f" {current_translations['and']} ".join(parts)
    except:
        return None

try:
    df = load_cleaned_data()

    degree_col = 'Degree Type' if 'Degree Type' in df.columns else df.columns[0]
    name_col = 'Name of scholarship' if 'Name of scholarship' in df.columns else df.columns[1]
    status_col = 'Live Status' if 'Live Status' in df.columns else None

    # 🛠️ 1. فلتر الحالة الرئيسي يظهر أولاً لفلترة المجموع الرئيسي
    status_filter = st.selectbox(
        t["filter_status"], 
        options=[t["all_status"], t["active_status"], t["expired_status"]]
    )

    # حساب الحالة التلقائية والملصقات المترجمة لكل منحة بناءً على اللغة المحددة حالياً
    live_statuses = []
    display_names = []
    for idx, row in df.iterrows():
        deadline_val = row.get('Deadline', t['na'])
        countdown = calculate_countdown_details(deadline_val, t)
        is_expired_by_script = status_col and "expired" in str(row.get(status_col, '')).lower()
        
        if is_expired_by_script or countdown == "expired":
            current_status = "expired"
            label = f"🔴 {row[name_col]} ({t['expired']})"
        else:
            current_status = "active"
            time_label = f" ({countdown})" if countdown else ""
            label = f"🟢 {row[name_col]}{time_label}"
            
        live_statuses.append(current_status)
        display_names.append(label)
        
    df['calculated_status'] = live_statuses
    df['display_name_label'] = display_names

    # تصفية المجموع الرئيسي بناءً على الفلتر الأول
    main_filtered_df = df.copy()
    if status_filter == t["active_status"]:
        main_filtered_df = main_filtered_df[main_filtered_df['calculated_status'] == "active"]
    elif status_filter == t["expired_status"]:
        main_filtered_df = main_filtered_df[main_filtered_df['calculated_status'] == "expired"]

    # 📊 2. عرض رقم المجموع الرئيسي المحدث بشكل حي
    total_scholarships = len(main_filtered_df)
    st.metric(label=t["total"], value=total_scholarships)
    st.divider()

    # 🎓 3. فلتر اختيار المرحلة الدراسية (يعتمد على المجموع المصفى)
    degree_options = [opt for opt in main_filtered_df[degree_col].unique() if opt != t["na"]]
    selected_degree = st.selectbox(t["select_degree"], options=degree_options)

    # التصفية النهائية للمرحلة المختارة
    final_df = main_filtered_df[main_filtered_df[degree_col] == selected_degree]

    st.subheader(f"{t['available_stage']} ({len(final_df)})")
    
    scholarship_options = final_df['display_name_label'].tolist()
    selected_display_name = st.selectbox(t["select_card"], options=scholarship_options)

    if selected_display_name:
        row = final_df[final_df['display_name_label'] == selected_display_name].iloc[0]
        
        st.markdown("---")
        st.success(f"{t['card_title']} {row[name_col]}")
        
        deadline_val = row.get('Deadline', t['na'])
        countdown_result = calculate_countdown_details(deadline_val, t)
        
        if row['calculated_status'] == "expired":
            st.error(t["expired"])
        elif countdown_result:
            st.metric(label=t["left"], value=countdown_result)
            st.divider()
            
        # تفاصيل المنحة المترجمة في أعمدة
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
    st.error(f"Error loading live data: {e}")