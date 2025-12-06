###Elsayed tamer elsayed darwesh
import tkinter as tk
from tkinter import ttk, messagebox
import requests

# --- 1. الجزء الخارجي (الدالة المسؤولة عن جلب سعر الصرف من الإنترنت) ---
def get_real_exchange_rate(from_currency, to_currency):
    try:
        # رابط API المجاني لجلب الأسعار بناءً على العملة الأساسية
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        
        # إرسال الطلب
        response = requests.get(url)
        
        # التحقق من نجاح الاتصال
        if response.status_code == 200:
            # تحويل البيانات القادمة من صيغة JSON إلى قاموس بايثون
            data = response.json()
            # استخراج السعر للعملة المطلوبة
            rate = data['rates'][to_currency]
            return rate
        else:
            messagebox.showerror("خطأ", "لا يمكن الاتصال بخدمة أسعار العملات حالياً.")
            return None
            
    except requests.exceptions.ConnectionError:
        messagebox.showerror("خطأ في الاتصال", "يرجى التأكد من اتصالك بالإنترنت.")
        return None
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ غير متوقع: {e}")
        return None


# --- 2. كود المنهج (دالة الزر والواجهة الرسومية) ---

def perform_conversion():
    # الحصول على البيانات من أدوات الواجهة
    amount_str = amount_entry.get()
    from_curr = from_combo.get()
    to_curr = to_combo.get()

    # التحقق من أن الحقول ليست فارغة
    if not amount_str or not from_curr or not to_curr:
        messagebox.showwarning("تنبيه", "الرجاء ملء جميع الحقول.")
        return

    # محاولة تحويل النص المدخل إلى رقم
    try:
        amount = float(amount_str)
    except ValueError:
        messagebox.showerror("خطأ في الإدخال", "الرجاء إدخال مبلغ صحيح (أرقام فقط).")
        return

    # تحديث الليبل مؤقتاً
    result_label.config(text="جاري جلب السعر...", fg="blue")
    root.update_idletasks()

    # استدعاء الدالة الخارجية لجلب السعر الحقيقي
    rate = get_real_exchange_rate(from_curr, to_curr)

    if rate is not None:
        # الحساب وعرض النتيجة
        converted_amount = amount * rate
        result_text = f"{amount} {from_curr} = {converted_amount:.2f} {to_curr}"
        result_label.config(text=result_text, fg="green", font=("Arial", 14, "bold"))
    else:
         result_label.config(text="فشلت عملية التحويل", fg="red")


# --- إعداد النافذة الرئيسية (Tkinter Setup) ---
root = tk.Tk()
root.title("محول العملات")
root.geometry("400x300")
root.config(padx=20, pady=20)

# قائمة العملات
currency_list = ["USD", "EGP", "EUR", "SAR", "AED", "GBP", "KWD"]

# الصف الأول: إدخال المبلغ
tk.Label(root, text="المبلغ:").grid(row=0, column=0, sticky="w", pady=10)
amount_entry = tk.Entry(root)
amount_entry.grid(row=0, column=1, padx=10, sticky="we")

# الصف الثاني: العملة المحول منها
tk.Label(root, text="من عملة:").grid(row=1, column=0, sticky="w", pady=10)
from_combo = ttk.Combobox(root, values=currency_list, state="readonly")
from_combo.grid(row=1, column=1, padx=10, sticky="we")
from_combo.set("USD")

# الصف الثالث: العملة المحول إليها
tk.Label(root, text="إلى عملة:").grid(row=2, column=0, sticky="w", pady=10)
to_combo = ttk.Combobox(root, values=currency_list, state="readonly")
to_combo.grid(row=2, column=1, padx=10, sticky="we")
to_combo.set("EGP")

# الصف الرابع: زر التحويل
convert_btn = tk.Button(root, text="تحويل", command=perform_conversion, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"))
convert_btn.grid(row=3, column=0, columnspan=2, pady=20, sticky="we")

# الصف الخامس: عرض النتيجة
result_label = tk.Label(root, text="---", font=("Arial", 12))
result_label.grid(row=4, column=0, columnspan=2, pady=10)

# توسيع الأعمدة لتناسب المحتوى
root.grid_columnconfigure(1, weight=1)

root.mainloop()
