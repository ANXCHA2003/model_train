"""
โมดูลสำหรับองค์ประกอบ GUI
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import Callable, Optional


class ModernButton(ctk.CTkButton):
    """ปุ่มแบบ Modern"""
    
    def __init__(self, master, text: str, command: Callable, **kwargs):
        super().__init__(
            master,
            text=text,
            command=command,
            font=("Arial", 12, "bold"),
            corner_radius=10,
            hover_color="#0066cc",
            **kwargs
        )


class ModernEntry(ctk.CTkEntry):
    """ช่องป้อนข้อมูลแบบ Modern"""
    
    def __init__(self, master, placeholder: str = "", **kwargs):
        super().__init__(
            master,
            placeholder_text=placeholder,
            font=("Arial", 12),
            corner_radius=8,
            border_width=2,
            **kwargs
        )


class ModernLabel(ctk.CTkLabel):
    """ป้ายชื่อแบบ Modern"""
    
    def __init__(self, master, text: str, **kwargs):
        super().__init__(
            master,
            text=text,
            font=("Arial", 12),
            **kwargs
        )


class ModernTextBox(ctk.CTkTextbox):
    """กล่องข้อความแบบ Modern"""
    
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            font=("Courier", 11),
            corner_radius=8,
            **kwargs
        )


class FileUploadFrame(ctk.CTkFrame):
    """เฟรมสำหรับอัปโหลดไฟล์"""
    
    def __init__(self, master, on_file_selected: Callable, **kwargs):
        super().__init__(master, **kwargs)
        
        self.on_file_selected = on_file_selected
        
        # ปุ่มเลือกไฟล์
        self.upload_btn = ModernButton(
            self,
            text="📁 เลือกไฟล์",
            command=self.select_file
        )
        self.upload_btn.pack(pady=10)
        
        # ป้ายแสดงชื่อไฟล์
        self.file_label = ModernLabel(self, text="ยังไม่ได้เลือกไฟล์")
        self.file_label.pack(pady=5)
        
        self.selected_file = None
    
    def select_file(self, file_types=None):
        """เลือกไฟล์"""
        if file_types is None:
            file_types = [("All Files", "*.*")]
        
        file_path = filedialog.askopenfilename(filetypes=file_types)
        
        if file_path:
            self.selected_file = file_path
            filename = file_path.split("/")[-1]
            self.file_label.configure(text=f"✅ {filename}")
            self.on_file_selected(file_path)
    
    def get_file(self):
        """ดึงไฟล์ที่เลือก"""
        return self.selected_file


class TabFrame(ctk.CTkScrollableFrame):
    """เฟรมแสดง Tab"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)


def show_info(title: str, message: str):
    """แสดงข้อความข้อมูล"""
    messagebox.showinfo(title, message)


def show_error(title: str, message: str):
    """แสดงข้อความข้อผิดพลาด"""
    messagebox.showerror(title, message)


def show_warning(title: str, message: str):
    """แสดงข้อความเตือน"""
    messagebox.showwarning(title, message)


def show_success(title: str, message: str):
    """แสดงข้อความสำเร็จ"""
    messagebox.showinfo(title, f"✅ {message}")
