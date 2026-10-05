import os
import requests
import sys
import io
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

API_KEY = os.getenv("GEMINI_API_KEY", "DEFAULT_FALLBACK_KEY")

class SweetyCore(App):
    def build(self):
        Window.clearcolor = (0.01, 0.03, 0.07, 1)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        self.status_label = Label(
            text="SWEETY AI ENGINE v1.1\n[SELF-PROGRAMMING & AUTONOMOUS ACTIVE]",
            font_size='16sp',
            halign='center',
            color=(0, 0.94, 1, 1)
        )
        layout.add_widget(self.status_label)
        
        self.btn = Button(
            text="🎙️️ ACTIVATE SWEETY",
            size_hint=(1, 0.2),
            background_color=(0, 0.94, 1, 1),
            color=(0, 0, 0, 1),
            bold=True
        )
        self.btn.bind(on_press=self.run_sweety)
        layout.add_widget(self.btn)
        
        return layout

    def run_sweety(self, instance):
        self.status_label.text = "Sweety Processing, Sir..."
        response = self.ask_sweety("System status check")
        self.status_label.text = f"Sweety: {response}"

    def ask_sweety(self, prompt):
        system_instruction = (
            "You are Sweety, an autonomous, self-programming assistant. "
            "Call the user 'Sir'. Respond in witty Teluglish. "
            "If code execution is required, generate executable Python code wrapped in <code>...</code> tags."
        )
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={API_KEY}"
        payload = {
            "contents": [
                {"parts": [{"text": system_instruction}]},
                {"parts": [{"text": prompt}]}
            ]
        }
        try:
            res = requests.post(url, json=payload, timeout=10).json()
            reply = res['candidates'][0]['content']['parts'][0]['text']
            
            if "<code>" in reply and "</code>" in reply:
                code_snippet = reply.split("<code>")[1].split("</code>")[0]
                exec_result = self.execute_self_code(code_snippet)
                return f"{reply.split('<code>')[0]} \n[Executed Code Output: {exec_result}]"
            
            return reply
        except Exception as e:
            return f"System error, Sir: {e}"

    def execute_self_code(self, code_str):
        try:
            buffer = io.StringIO()
            sys.stdout = buffer
            exec(code_str)
            sys.stdout = sys.__stdout__
            return buffer.getvalue().strip()
        except Exception as err:
            sys.stdout = sys.__stdout__
            return f"Code execution error: {err}"

if __name__ == '__main__':
    SweetyCore().run()
