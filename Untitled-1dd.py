import customtkinter as ctk
import requests

# إعدادات الثيم (شكل التطبيق)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SharifAIApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sharif AI - Llama 4 Edition")
        self.geometry("600x500")

        # العنوان
        self.label = ctk.CTkLabel(self, text="اسأل ذكاء شريف الاصطناعي", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)

        # خانة كتابة السؤال
        self.user_input = ctk.CTkEntry(self, placeholder_text="اكتب سؤالك هنا...", width=500, height=40)
        self.user_input.pack(pady=10)

        # زر الإرسال
        self.send_button = ctk.CTkButton(self, text="إرسال السؤال", command=self.get_ai_response)
        self.send_button.pack(pady=10)

        # منطقة عرض الإجابة (قابلة للتمرير)
        self.result_box = ctk.CTkTextbox(self, width=540, height=250, font=("Arial", 14))
        self.result_box.pack(pady=20)

    def get_ai_response(self):
        question = self.user_input.get()
        if not question: return

        self.result_box.delete("1.0", "end")
        self.result_box.insert("end", "⏳ جاري التفكير... انتظر قليلاً")
        self.update()

        # إعدادات الـ API الخاصة بك
        url = "https://integrate.api.nvidia.com/v1/chat/completions"
        api_key = "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"
        
        headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
        payload = {
            "model": "meta/llama-4-maverick-17b-128e-instruct",
            "messages": [{"role": "user", "content": question}],
            "temperature": 0.7,
            "stream": False
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                answer = response.json()['choices'][0]['message']['content']
                self.result_box.delete("1.0", "end")
                self.result_box.insert("end", answer)
            else:
                self.result_box.insert("end", f"\n❌ خطأ: {response.status_code}")
        except Exception as e:
            self.result_box.insert("end", f"\n❌ حدث خطأ: {str(e)}")

if __name__ == "__main__":
    app = SharifAIApp()
    app.mainloop()