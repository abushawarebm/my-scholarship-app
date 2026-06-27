import streamlit as st
import pandas as pd
from datetime import datetime, date

# 1. إعدادات الصفحة
st.set_page_config(page_title="Scholarship Explorer", layout="centered")

# 2. قاموس الترجمة الكامل والثابت للغات الثلاث
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
        "na": "Not Available",
        "expired": "Expired / Closed",
        "months": "Months",
        "days": "Days",
        "left": "Remaining:",
        "and": "and",
        "less_than_day": "Less than a day left",
        "summary_title": "⚡ Quick Overview",
        "top_countries": "Top Countries",
        "fully_funded": "Fully Funded Count"
    },
    "العربية": {
        "title": "🎓 مستكشف المنح الدراسية الذكي",
        "subtitle": "ابحث وتصفح المنح الدراسية المتاحة مع تصفية حية حسب الحالة والمرحلة الدراسية.",
        "total": "📊 إجمالي المنح المتاحة حالياً",
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
        "na": "غير متوفر",
        "expired": "منتهية / مغلقة",
        "months": "شهر",
        "days": "يوم",
        "left": "متبقي:",
        "and": "و",
        "less_than_day": "أقل من يوم متبقي",
        "summary_title": "⚡ ملخصات سريعة وإحصائيات",
        "top_countries": "أبرز الدول المتاحة",
        "fully_funded": "عدد المنح الممولة بالكامل"
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
        "na": "Niet Beschikbaar",
        "expired": "Verlopen / Gesloten",
        "months": "Maanden",
        "days": "Dagen",
        "left": "Resterend:",
        "and": "en",
        "less_than_day": "Minder dan een dag over",
        "summary_title": "⚡ Snel Overzicht",
        "top_countries": "Populaire Landen",
        "fully_funded": "Aantal Volledig Gefinancierd"
    }
}

# اختيار اللغة
lang = st.selectbox("🌐 Choose Language / اختر اللغة / Kies Taal", ["English", "العربية", "Nederlands"])
t = translations[lang]

st.title(t["title"])
st.markdown(t["subtitle"])

# 3. رابط سحب البيانات المباشر من Google Sheets بصيغة CSV
SHEET_URL = "https://docs.google.com/spreadsheets/d/1cW5YWrR0kj6XEpyKQ1x3wmvCqFIJGYoJneQaRyXDnu4/export?format=csv"

@st.cache_data(ttl=1)
def load_cleaned_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip()
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).str.strip()
        df.fillna("Not Available", inplace=True)
        df.replace("nan", "Not Available", inplace=True)
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

# دالة معالجة وحساب الوقت المتبقي المستقرة والمجربة 100%
def calculate_countdown_details(deadline_str, trans_dict):
    if not deadline_str or str(deadline_str).strip() in ["Not Available", "nan", ""]:
        return None
    try:
        # تحويل صيغ التاريخ الشائعة بنجاح وتفادي مشاكل الحروف الزائدة
        parsed_date = pd.to_datetime(str(deadline_str).strip(), errors='coerce')
        if pd.isna(parsed_date):
            return None
            
        deadline_date = parsed_date.date()
        today = date.today()
        
        if deadline_date < today:
            return "expired"
            
        diff_days = (deadline_date - today).days
        if diff_days == 0:
            return f"{trans_dict['less_than_day']}"
            
        months = diff_days // 30
        days = diff_days % 30
        
        parts = []
        if months > 0:
            parts.append(f"{months} {trans_dict['months']}")
        if days > 0:
            parts.append(f"{days} {trans_dict['days']}")
            
        if not parts:
            return f"{trans_dict['less_than_day']}"
            
        return f"{trans_dict['left']} " + f" {trans_dict['and']} ".join(parts)
    except:
        return None

df = load_cleaned_data()

if not df.empty:
    degree_col = 'Degree Type' if 'Degree Type' in df.columns else df.columns[0]
    name_col = 'Name of scholarship' if 'Name of scholarship' in df.columns else df.columns[1]
    status_col = 'Live Status' if 'Live Status' in df.columns else None

    # خطوة الفلترة المسبقة بناءً على التاريخ الفعلي للحاسوب والسيرفر
    calculated_statuses = []
    for idx, row in df.iterrows():
        deadline_val = row.get('Deadline', "Not Available")
        countdown = calculate_countdown_details(deadline_val, t)
        is_expired_by_script = status_col and "expired" in str(row.get(status_col, '')).lower()
        
        if is_expired_by_script or countdown == "expired":
            calculated_statuses.append("expired")
        else:
            calculated_statuses.append("active")
    df['calculated_status'] = calculated_statuses

    # 🛠️ 1. الفلتر الرئيسي في بداية الصفحة لفلترة البيانات بالكامل
    status_filter = st.selectbox(
        t["filter_status"], 
        options=[t["all_status"], t["active_status"], t["expired_status"]]
    )

    # تطبيق الفلترة الرئيسية فوراً على المجموع الرئيسي
    main_filtered_df = df.copy()
    if status_filter == t["active_status"]:
        main_filtered_df = main_filtered_df[main_filtered_df['calculated_status'] == "active"]
    elif status_filter == t["expired_status"]:
        main_filtered_df = main_filtered_df[main_filtered_df['calculated_status'] == "expired"]

    # 📊 2. العداد الإجمالي للمنح المصفاة
    total_scholarships = len(main_filtered_df)
    st.metric(label=t["total"], value=total_scholarships)
    
    # ⚡ 3. إضافة قسم ملخصات سريع ومختصر للمنح الحالية المصفاة
    st.markdown(f"### {t['summary_title']}")
    sum_col1, sum_col2 = st.columns(2)
    
    with sum_col1:
        # حساب أبرز الدول تكراراً في المجموعة المصفاة حالياً
        if 'Country' in main_filtered_df.columns:
            top_countries = main_filtered_df['Country'].value_counts().index[:2].tolist()
            countries_str = ", ".join(top_countries) if top_countries else t["na"]
            st.reply = st.caption(f"🌍 {t['top_countries']}: **{countries_str}**")
    with sum_col2:
        # حساب المنح الممولة بالكامل في المجموعة الحالية
        if 'Scholarship Coverage' in main_filtered_df.columns:
            fully_funded_count = main_filtered_df['Scholarship Coverage'].str.lower().str.contains('full').sum()
            st.caption(f"💰 {t['fully_funded']}: **{fully_funded_count}**")
            
    st.divider()

    # تحديث لواصق الأسماء والعداد الزمني المتبقي للمجموع الحالي المفلتر
    display_names = []
    for idx, row in main_filtered_df.iterrows():
        deadline_val = row.get('Deadline', "Not Available")
        countdown = calculate_countdown_details(deadline_val, t)
        if row['calculated_status'] == "expired":
            display_names.append(f"🔴 {row[name_col]} ({t['expired']})")
        else:
            time_label = f" ({countdown})" if countdown else ""
            display_names.append(f"🟢 {row[name_col]}{time_label}")
    main_filtered_df['display_name_label'] = display_names

    # 🎓 4. فلتر اختيار المرحلة الدراسية المعتمد تماماً على الفلتر الرئيسي
    degree_options = [opt for opt in main_filtered_df[degree_col].unique() if opt != "Not Available"]
    
    if degree_options:
        selected_degree = st.selectbox(t["select_degree"], options=degree_options)
        final_df = main_filtered_df[main_filtered_df[degree_col] == selected_degree]

        st.subheader(f"{t['available_stage']} ({len(final_df)})")
        
        scholarship_options = final_df['display_name_label'].tolist()
        if scholarship_options:
            selected_display_name = st.selectbox(t["select_card"], options=scholarship_options)

            if selected_display_name:
                row = final_df[final_df['display_name_label'] == selected_display_name].iloc[0]
                st.markdown("---")
                st.success(f"{t['card_title']} {row[name_col]}")
                
                deadline_val = row.get('Deadline', "Not Available")
                countdown_result = calculate_countdown_details(deadline_val, t)
                
                if row['calculated_status'] == "expired":
                    st.error(t["expired"])
                elif countdown_result:
                    st.metric(label=t["left"], value=countdown_result)
                    st.divider()
                    
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
                if link_col and row[link_col] != "Not Available" and str(row[link_col]) != "nan":
                    # إصلاح الرابط تلقائياً لو لم يحتوي على البروتوكول الأساسي
                    url_clean = str(row[link_col]).strip()
                    if not url_clean.startswith(('http://', 'https://')):
                        url_clean = f"https://{url_clean}"
                    st.link_button(t["apply"], url_clean, use_container_width=True)
        else:
            st.info("No scholarships available for this selection.")
    else:
        st.info("No options available for the selected status.")