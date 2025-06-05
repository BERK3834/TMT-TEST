import tkinter as tk
from tkinter import scrolledtext
import random
import time

class TrailMakingTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Trail Making Test")
        self.root.geometry("1920x1080")
        self.root.attributes("-fullscreen", True)  
        self.root.configure(bg="black")

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        self.test_running = False
        self.start_time = None
        self.total_time = 300  
        self.remaining_time = self.total_time
        self.current_step = 0
        self.correct_answers = 0
        self.wrong_answers = 0
        
        self.sequence_A = [str(i) for i in range(1, 24)]
        self.sequence_B = sum([[str(i), chr(64 + i)] for i in range(1, 13)], [])
        self.correct_sequence = []
        self.current_sequence = []
        self.button_positions = [] 
        
        self.part_A_results = {"time": 0, "correct": 0, "wrong": 0, "score": 0, "result": ""}
        self.part_B_results = {"time": 0, "correct": 0, "wrong": 0, "score": 0, "result": ""}
        
        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.previous_button_position = None
        
        self.start_screen()
    
    def start_screen(self):
        self.clear_widgets()

        tk.Label(self.root, text="Trail Making Test Kuralları", font=("Arial", 16, "bold"), fg="white", bg="black").pack(pady=10)

        rules = ("Bu test, bilişsel yeteneklerinizi ve görsel-motor hızınızı ölçmek için tasarlanmıştır.\n"
                 "- Bölüm A: 1'den 23'e kadar sırasıyla tıklayın.\n"
                 "- Bölüm B: 1-A, 2-B, 3-C şeklinde sırayla tıklayın.\n"
                 "- Yanlış seçim yaparsanız önceki doğru adıma dönmeniz gerekecek.\n"
                 "- Test süresi 5 dakikadır, süre dolduğunda veyahut siz bitir butonuna bastığınızda test otomatik diğer parta geçmektedir.\n"
                 "- 'Başla' butonuyla testi başlatabilirsiniz.")
        
        text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=8, bg="black", fg="white", font=("Arial", 12))
        text_area.insert(tk.INSERT, rules)
        text_area.config(state=tk.DISABLED)
        text_area.pack(pady=10)
        
        tk.Button(self.root, text="Başla", font=("Arial", 14, "bold"), bg="gray", fg="white", command=lambda: self.start_test()).pack(pady=10)
    
    def start_test(self):
        self.test_running = True
        self.start_time = time.time()
        self.remaining_time = self.total_time
        self.current_step = 0
        self.correct_answers = 0
        self.wrong_answers = 0
        self.part_A_results = {"time": 0, "correct": 0, "wrong": 0, "score": 0, "result": ""}
        self.part_B_results = {"time": 0, "correct": 0, "wrong": 0, "score": 0, "result": ""}
        
        self.clear_widgets()
        self.start_part("A")
    
    def start_part(self, part):
        self.clear_widgets()
        
        if part == "A":
            self.correct_sequence = self.sequence_A
        elif part == "B":
            self.correct_sequence = self.sequence_B
        
        self.current_sequence = self.correct_sequence[:]  
        random.shuffle(self.current_sequence)  

        self.button_positions = []  
        
        self.test_running = True
        self.start_time = time.time()
        self.remaining_time = self.total_time
        self.current_step = 0
        self.correct_answers = 0
        self.wrong_answers = 0
        
        self.timer_label = tk.Label(self.root, text=self.format_time(self.remaining_time), font=("Arial", 14), fg="white", bg="black")
        self.timer_label.pack(pady=10)
        
        self.buttons = []
        for value in self.current_sequence:
            x, y = self.get_non_overlapping_position()
            btn = tk.Button(self.root, text=value, font=("Arial", 12), bg="gray", fg="white", width=5, height=2,
                            command=lambda b=value: self.check_selection(b, part))
            btn.place(x=x, y=y)  
            self.buttons.append(btn)
        
        tk.Button(self.root, text="Bitir", font=("Arial", 14), bg="gray", fg="white", command=self.finish_test).pack(pady=20)
        
        self.update_timer()
    
    def get_non_overlapping_position(self):
        max_attempts = 100  
        for _ in range(max_attempts):
            x = random.randint(50, 900)  
            y = random.randint(100, 600)  
            
            overlap = False
            for bx, by in self.button_positions:
                if abs(x - bx) < 60 and abs(y - by) < 60:  
                    overlap = True
                    break
            
            if not overlap:
                self.button_positions.append((x, y))
                return x, y
        
        return 50, 100  
    
    def check_selection(self, value, part):
        if not self.test_running:
            return

        expected = self.correct_sequence[self.current_step]  

        if value == expected:
            self.current_step += 1
            self.correct_answers += 1
            self.update_button_color(value, "green")
            
            if self.current_step > 1 and part == "A":
                prev_value = self.correct_sequence[self.current_step - 2]
                prev_button = next(btn for btn in self.buttons if btn.cget("text") == prev_value)
                prev_x = prev_button.winfo_x() + prev_button.winfo_width() // 2
                prev_y = prev_button.winfo_y() + prev_button.winfo_height() // 2
                
                current_button = next(btn for btn in self.buttons if btn.cget("text") == value)
                current_x = current_button.winfo_x() + current_button.winfo_width() // 2
                current_y = current_button.winfo_y() + current_button.winfo_height() // 2
                
                self.canvas.create_line(prev_x, prev_y, current_x, current_y, fill="green", width=2)
            
            if self.current_step >= len(self.correct_sequence):  
                self.finish_test()
        else:
            self.wrong_answers += 1
            self.update_button_color(value, "red")
    
    def update_button_color(self, value, color):
        for btn in self.buttons:
            if btn.cget("text") == value:
                btn.configure(bg=color)
                self.root.after(1000, lambda: btn.configure(bg="gray"))
                break
    
    def update_timer(self):
        if self.test_running:
            elapsed_time = int(time.time() - self.start_time)
            self.remaining_time = max(0, self.total_time - elapsed_time)
            self.timer_label.config(text=self.format_time(self.remaining_time))
            
            if self.remaining_time > 0:
                self.root.after(1000, self.update_timer)
            else:
                self.finish_test()
    
    def format_time(self, remaining_time):
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        return f"Kalan Süre: {minutes:02d}:{seconds:02d}"
    
    def finish_test(self):
        self.test_running = False
        elapsed_time = int(time.time() - self.start_time)
        
        score = elapsed_time + (self.wrong_answers * 2)
        if score <= 29:
            result = "İYİ"
        elif score <= 78:
            result = "ORTALAMA"
        else:
            result = "ZAYIF"
        
        if self.correct_sequence == self.sequence_A:
            self.part_A_results["time"] = elapsed_time
            self.part_A_results["correct"] = self.correct_answers
            self.part_A_results["wrong"] = self.wrong_answers
            self.part_A_results["score"] = score
            self.part_A_results["result"] = result
            self.start_part("B")
        elif self.correct_sequence == self.sequence_B:
            self.part_B_results["time"] = elapsed_time
            self.part_B_results["correct"] = self.correct_answers
            self.part_B_results["wrong"] = self.wrong_answers
            self.part_B_results["score"] = score
            self.part_B_results["result"] = result
            self.show_final_results()
    
    def show_final_results(self):
        self.clear_widgets()
        
        result_text = (
            f"Part A Sonuçları:\n"
            f"Geçen Süre: {self.part_A_results['time']} saniye\n"
            f"Doğru: {self.part_A_results['correct']}, Yanlış: {self.part_A_results['wrong']}\n"
            f"Puan: {self.part_A_results['score']}, Sonuç: {self.part_A_results['result']}\n"
            "----------------------------------------\n"
            f"Part B Sonuçları:\n"
            f"Geçen Süre: {self.part_B_results['time']} saniye\n"
            f"Doğru: {self.part_B_results['correct']}, Yanlış: {self.part_B_results['wrong']}\n"
            f"Puan: {self.part_B_results['score']}, Sonuç: {self.part_B_results['result']}"
        )
        
        tk.Label(self.root, text=result_text, font=("Arial", 12), fg="white", bg="black").pack(pady=20)
        tk.Button(self.root, text="Yeniden Başla", font=("Arial", 14), bg="gray", fg="white", command=self.start_screen).pack(pady=20)
    
    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrailMakingTest(root)
    root.mainloop()