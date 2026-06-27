import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات الصفحة والتنسيق العام
st.set_page_config(page_title="Scholarship Explorer", layout="centered")

# 2. قاموس الترجمة المطور للغات الثلاث (مع إضافة كلمات الفلترة الجديدة)
translations = {
    "English": {
        "title": "🎓 Smart Scholarship Explorer",
        "subtitle": "Explore and filter available scholarships based on your degree type.",
        "total": "📊 Total Available Scholarships",
        "select_degree": "Select Degree Type:",
        "select_status": "Filter by Scholarship Status:",
        "status_all": "All Scholarships",
        "status_active": "🟢 Active Only",
        "status_expired": "🔴 Closed / Expired Only",
        "available_stage": "Available Scholarships matching your criteria",
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
        "subtitle": "ابحث وتصفح المنح الدراسية المتاحة بناءً على المرحلة الدراسية والحالة الحية.",
        "total": "📊 إجمالي المنح المتاحة",
        "select_degree": "اختر المرحلة الدراسية:",
        "select_status": "تصفية حسب حالة المنحة:",
        "status_all": "جميع المنح",
        "status_active": "🟢 الفعالة فقط",
        "status_expired": "🔴 المغلقة / المنتهية فقط",
        "available_stage": "المنح المتاحة المتوافقة مع خياراتك",
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
        "select_status": "Filteren op status beurs:",
        "status_all": "Alle Beurzen",
        "status_active": "🟢 Alleen Actief",
        "status_expired": "🔴 Alleen Verlopen / Gesloten",
        "available_stage": "Beschikbare beurzen die aan uw criteria voldoen",
        "select_card": "Klik hieronder om een gedetailleerde kaart te openen:",
        "card_title": "📜 Gedetailleerde Beurzenkaart