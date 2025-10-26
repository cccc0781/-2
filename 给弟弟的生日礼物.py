import tkinter as tk
import random
import time
from PIL import Image, ImageTk

# 新增：多文案
popup_texts = [
    "生日快乐", "天天开心", "生日快乐", "你最可爱啦", "生日快乐",
    "天天开心", "身体健康", "好事发生", "想和你贴贴", "岁岁无虞",
    "万事顺遂", "万事顺遂", "所念皆如愿", "生日快乐", "好奶呀是弟弟吧",
    "无事绊心弦", "昭昭如愿", "生日快乐", "爱你到永远", "你是最棒的",
    "我的小可爱", "生日快乐", "岁岁安澜", "长安常乐", "永远在一起"
]

# 使用你提供的柯南图片路径
conan_image_path = r"C:\Users\lenovo\Desktop\新兰.jpg"

class PopupManager:
    def __init__(self):
        self.windows = []
        self.photo_images = []  # 保存所有图片引用
        self.root = tk.Tk()
        self.root.withdraw()  # 隐藏主窗口
        
        # 预加载图片
        self.original_image = None
        self.load_image()
    
    def load_image(self):
        """加载背景图片"""
        try:
            self.original_image = Image.open(conan_image_path)
            print("图片加载成功！")
        except Exception as e:
            print(f"加载图片失败: {e}")
            self.original_image = None
    
    def create_popup(self, index):
        """创建一个弹窗"""
        window = tk.Toplevel(self.root)
        window.title("亲爱的炼狱宝宝")
        
        # 设置窗口位置 - 更分散的分布
        width = window.winfo_screenwidth()
        height = window.winfo_screenheight()
        
        # 计算位置，让弹窗更均匀分布
        row = index % 5  # 5行
        col = index % 6  # 6列
        x = col * (width // 6) + random.randint(-50, 50)
        y = row * (height // 5) + random.randint(-30, 30)
        
        # 确保在屏幕范围内
        x = max(0, min(x, width - 220))
        y = max(0, min(y, height - 50))
        
        window.geometry(f"300x150+{x}+{y}")
        
        # 设置窗口始终在最前面
        window.attributes('-topmost', True)
        
        if self.original_image:
            try:
                # 调整图片大小
                resized_image = self.original_image.resize((300, 150), Image.Resampling.LANCZOS)
                conan_bg = ImageTk.PhotoImage(resized_image)
                
                # 保存图片引用
                self.photo_images.append(conan_bg)
                
                # 创建Canvas并设置背景
                canvas = tk.Canvas(window, width=300, height=150)
                canvas.pack(fill="both", expand=True)
                canvas.create_image(0, 0, image=conan_bg, anchor="nw")
                
                # 添加文字
                random_text = random.choice(popup_texts)
                # 文字描边效果
                canvas.create_text(111, 26, text=random_text, font=("楷体", 14, "bold"), fill="black")
                canvas.create_text(109, 26, text=random_text, font=("楷体", 14, "bold"), fill="black")
                canvas.create_text(110, 25, text=random_text, font=("楷体", 14, "bold"), fill="black")
                canvas.create_text(110, 27, text=random_text, font=("楷体", 14, "bold"), fill="black")
                canvas.create_text(110, 26, text=random_text, font=("楷体", 14, "bold"), fill="white")
                
                print(f"创建第 {index + 1} 个弹窗（有图片）")
                
            except Exception as e:
                print(f"创建图片背景失败: {e}")
                self.create_fallback_window(window, index)
        else:
            self.create_fallback_window(window, index)
        
        self.windows.append(window)
        
        # 8秒后自动关闭窗口（稍微延长显示时间）
        window.after(8000, lambda: self.close_window(window))
    
    def create_fallback_window(self, window, index):
        """创建备用窗口（无图片版本）"""
        random_text = random.choice(popup_texts)
        popup_colors = ["pink", "lightpink", "hotpink", "palevioletred", "lightcoral", 
                       "lightblue", "lightgreen", "lavender", "peachpuff", "lightyellow"]
        random_color = random.choice(popup_colors)
        label = tk.Label(window, text=random_text, bg=random_color, 
                        font=("楷体", 14), width=25, height=4)
        label.pack()
        print(f"创建第 {index + 1} 个弹窗（备用背景）")
    
    def close_window(self, window):
        """关闭窗口"""
        if window in self.windows:
            self.windows.remove(window)
        window.destroy()
    
    def start_popups(self):
        """开始创建弹窗序列"""
        total_popups = 100  # 增加到30个弹窗
        
        for i in range(total_popups):
            # 随机间隔创建，更自然的效果
            delay = i * 200 + random.randint(-50, 50)  # 200ms基础间隔，加上随机变化
            self.root.after(delay, lambda idx=i: self.create_popup(idx))
        
        # 所有弹窗创建完成后，60秒后退出程序
        total_duration = total_popups * 200 + 10000  # 计算总时间
        self.root.after(total_duration, self.cleanup)
        
        print(f"开始创建 {total_popups} 个弹窗...")
        self.root.mainloop()
    
    def cleanup(self):
        """清理资源"""
        print("程序结束")
        self.root.quit()

# 创建并启动弹窗管理器
manager = PopupManager()
manager.start_popups()
