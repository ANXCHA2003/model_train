"""
โปรแกรม GUI สำหรับเทรนโมเดล Machine Learning / Deep Learning
ระบบ: Windows
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
import os
from pathlib import Path

from modules.data_loader import DataLoader
from modules.data_validator import DataValidator
from modules.model_trainer import ModelTrainer
from modules.product_manager import ProductManager
from modules.ui_components import (
    ModernButton, ModernEntry, ModernLabel, ModernTextBox,
    FileUploadFrame, TabFrame, show_info, show_error, show_warning, show_success
)


class MeatModelTrainerApp(ctk.CTk):
    """แอปพลิเคชันหลักสำหรับเทรนโมเดล"""
    
    def __init__(self):
        super().__init__()
        
        # ตั้งค่าหน้าต่าง
        self.title("🥩 Meat Model Trainer - ระบบเทรนโมเดล")
        self.geometry("1000x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # โฟลเดอร์
        self.data_dir = "data"
        self.models_dir = "models"
        
        # ตัวแปรเก็บไฟล์ที่เลือก
        self.selected_image_path = None
        self.selected_data_path = None
        
        # สร้างโฟลเดอร์ถ้ายังไม่มี
        Path(self.data_dir).mkdir(exist_ok=True)
        Path(self.data_dir + "/images").mkdir(exist_ok=True)
        Path(self.models_dir).mkdir(exist_ok=True)
        
        # โมดูล
        self.data_loader = DataLoader(self.data_dir)
        self.data_validator = DataValidator(f"{self.data_dir}/uploaded_data.csv")
        self.product_manager = ProductManager(f"{self.data_dir}/uploaded_data.csv")
        self.model_trainer = None
        
        try:
            self.model_trainer = ModelTrainer(self.models_dir)
        except ImportError as e:
            show_error("ข้อผิดพลาด", f"ต้องติดตั้ง TensorFlow:\npip install tensorflow\n\n{str(e)}")
        
        # สร้าง UI
        self.create_ui()
    
    def create_ui(self):
        """สร้าง User Interface"""
        
        # Header
        header_frame = ctk.CTkFrame(self, height=60)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        header_label = ModernLabel(
            header_frame,
            text="🥩 ระบบเทรนโมเดลสำหรับการจำแนกเนื้อสัตว์"
        )
        header_label.pack()
        
        # Tabview
        self.tabview = ctk.CTkTabview(self, width=950, height=600)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        # สร้าง Tabs
        self.tab_data = self.tabview.add("📦 เพิ่มข้อมูล")
        self.tab_validate = self.tabview.add("🧹 ตรวจสอบข้อมูล")
        self.tab_train = self.tabview.add("🤖 เทรนโมเดล")
        
        # สร้างเนื้อหา Tab
        self.create_data_tab()
        self.create_validate_tab()
        self.create_train_tab()
    
    def create_data_tab(self):
        """สร้างแท็บเพิ่มข้อมูล"""
        
        # สร้าง scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(self.tab_data)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # ===== Section: อัปโหลดภาพ =====
        image_section = ctk.CTkFrame(scroll_frame, fg_color="#1a1a1a", corner_radius=10)
        image_section.pack(fill="x", pady=10)
        
        image_title = ModernLabel(image_section, text="📸 อัปโหลดไฟล์ภาพ")
        image_title.pack(pady=(10, 5), padx=10, anchor="w")
        
        image_subtitle = ModernLabel(image_section, text="รองรับไฟล์: .jpg, .png, .bmp, .gif")
        image_subtitle.pack(pady=(0, 10), padx=10, anchor="w")
        image_subtitle.configure(text_color="#888888")
        
        # ปุ่มเลือกไฟล์ภาพ
        image_btn_frame = ctk.CTkFrame(image_section, fg_color="transparent")
        image_btn_frame.pack(fill="x", padx=10, pady=5)
        
        self.image_upload_btn = ModernButton(
            image_btn_frame,
            text="📁 เลือกไฟล์",
            command=self.select_image_file
        )
        self.image_upload_btn.pack(side="left", padx=5)
        
        self.image_label = ModernLabel(image_btn_frame, text="ยังไม่ได้เลือกไฟล์")
        self.image_label.pack(side="left", padx=10, anchor="w")
        
        # ปุ่มบันทึกไฟล์ภาพ
        save_image_btn = ModernButton(
            image_section,
            text="💾 บันทึกไฟล์ภาพ",
            command=self.save_image
        )
        save_image_btn.pack(pady=(0, 10), padx=10)
        
        # ===== Section: อัปโหลดข้อมูล =====
        data_section = ctk.CTkFrame(scroll_frame, fg_color="#1a1a1a", corner_radius=10)
        data_section.pack(fill="x", pady=10)
        
        data_title = ModernLabel(data_section, text="📊 อัปโหลดไฟล์ข้อมูล")
        data_title.pack(pady=(10, 5), padx=10, anchor="w")
        
        data_subtitle = ModernLabel(data_section, text="รองรับไฟล์: .csv, .xlsx, .json")
        data_subtitle.pack(pady=(0, 10), padx=10, anchor="w")
        data_subtitle.configure(text_color="#888888")
        
        # ปุ่มเลือกไฟล์ข้อมูล
        data_btn_frame = ctk.CTkFrame(data_section, fg_color="transparent")
        data_btn_frame.pack(fill="x", padx=10, pady=5)
        
        self.data_upload_btn = ModernButton(
            data_btn_frame,
            text="📁 เลือกไฟล์",
            command=self.select_data_file
        )
        self.data_upload_btn.pack(side="left", padx=5)
        
        self.data_label = ModernLabel(data_btn_frame, text="ยังไม่ได้เลือกไฟล์")
        self.data_label.pack(side="left", padx=10, anchor="w")
        
        # ปุ่มบันทึกไฟล์ข้อมูล
        save_data_btn = ModernButton(
            data_section,
            text="💾 บันทึกไฟล์ข้อมูล",
            command=self.save_data
        )
        save_data_btn.pack(pady=(0, 10), padx=10)
        
        # ===== Section: สถานะข้อมูล =====
        status_section = ctk.CTkFrame(scroll_frame, fg_color="#1a1a1a", corner_radius=10)
        status_section.pack(fill="both", expand=True, pady=10)
        
        status_title = ModernLabel(status_section, text="✅ สถานะข้อมูล")
        status_title.pack(pady=(10, 5), padx=10, anchor="w")
        
        # ข้อมูลภาพ
        image_info_frame = ctk.CTkFrame(status_section, fg_color="transparent")
        image_info_frame.pack(fill="x", padx=10, pady=5, anchor="w")
        
        image_info_label = ModernLabel(image_info_frame, text="📸 ไฟล์ภาพ:")
        image_info_label.pack(side="left", padx=5)
        
        self.image_count_label = ModernLabel(image_info_frame, text="0 ไฟล์")
        self.image_count_label.pack(side="left", padx=5)
        self.image_count_label.configure(text_color="#4CAF50")
        
        # ข้อมูลตาราง
        data_info_frame = ctk.CTkFrame(status_section, fg_color="transparent")
        data_info_frame.pack(fill="x", padx=10, pady=5, anchor="w")
        
        data_info_label = ModernLabel(data_info_frame, text="📊 ไฟล์ข้อมูล:")
        data_info_label.pack(side="left", padx=5)
        
        self.data_rows_label = ModernLabel(data_info_frame, text="0 แถว")
        self.data_rows_label.pack(side="left", padx=5)
        self.data_rows_label.configure(text_color="#4CAF50")
        
        self.data_cols_label = ModernLabel(data_info_frame, text="0 คอลัมน์")
        self.data_cols_label.pack(side="left", padx=5)
        self.data_cols_label.configure(text_color="#4CAF50")
        
        # ปุ่มรีเฟรช
        refresh_btn = ModernButton(
            status_section,
            text="🔄 รีเฟรช",
            command=self.refresh_data_info
        )
        refresh_btn.pack(pady=10)
    
    def create_validate_tab(self):
        """สร้างแท็บตรวจสอบข้อมูล"""
        
        # Title
        title = ModernLabel(self.tab_validate, text="🧹 ตรวจสอบและทำความสะอาดข้อมูล")
        title.pack(pady=10)
        
        # ปุ่มตรวจสอบ
        button_frame = ctk.CTkFrame(self.tab_validate)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        check_btn = ModernButton(
            button_frame,
            text="📋 ตรวจสอบข้อมูล",
            command=self.check_data
        )
        check_btn.pack(side="left", padx=5)
        
        remove_missing_btn = ModernButton(
            button_frame,
            text="🗑️ ลบค่าว่าง",
            command=self.remove_missing
        )
        remove_missing_btn.pack(side="left", padx=5)
        
        remove_dup_btn = ModernButton(
            button_frame,
            text="🔁 ลบแถวซ้ำ",
            command=self.remove_duplicates
        )
        remove_dup_btn.pack(side="left", padx=5)
        
        # ผลการตรวจสอบ
        result_frame = ctk.CTkFrame(self.tab_validate)
        result_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        result_title = ModernLabel(result_frame, text="📊 ผลการตรวจสอบ")
        result_title.pack(pady=5)
        
        self.validate_text = ModernTextBox(result_frame)
        self.validate_text.pack(fill="both", expand=True, pady=10)
    
    def create_train_tab(self):
        """สร้างแท็บเทรนโมเดล"""
        
        # Title
        title = ModernLabel(self.tab_train, text="🤖 เทรนโมเดล Machine Learning")
        title.pack(pady=10)
        
        # Input frame
        input_frame = ctk.CTkFrame(self.tab_train)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        # Target column
        target_label = ModernLabel(input_frame, text="🎯 ชื่อคอลัมน์เป้าหมาย (Target):")
        target_label.pack(pady=5)
        
        self.target_entry = ModernEntry(input_frame, placeholder="เช่น: price, category")
        self.target_entry.pack(fill="x", pady=5)
        
        # Epochs
        epochs_label = ModernLabel(input_frame, text="⏱️ จำนวน Epochs:")
        epochs_label.pack(pady=5)
        
        self.epochs_entry = ModernEntry(input_frame, placeholder="เช่น: 50")
        self.epochs_entry.pack(fill="x", pady=5)
        self.epochs_entry.insert(0, "50")
        
        # Batch size
        batch_label = ModernLabel(input_frame, text="📦 Batch Size:")
        batch_label.pack(pady=5)
        
        self.batch_entry = ModernEntry(input_frame, placeholder="เช่น: 32")
        self.batch_entry.pack(fill="x", pady=5)
        self.batch_entry.insert(0, "32")
        
        # ปุ่มเทรน
        train_btn = ModernButton(
            input_frame,
            text="🚀 เริ่มเทรนโมเดล",
            command=self.train_model
        )
        train_btn.pack(pady=15)
        
        # Model name
        model_name_label = ModernLabel(input_frame, text="💾 ชื่อโมเดล (ไม่มี .h5 หรือ .tflite):")
        model_name_label.pack(pady=5)
        
        self.model_name_entry = ModernEntry(input_frame, placeholder="เช่น: my_meat_model")
        self.model_name_entry.pack(fill="x", pady=5)
        self.model_name_entry.insert(0, "meat_model")
        
        # ปุ่มบันทึก
        save_model_btn = ModernButton(
            input_frame,
            text="💾 บันทึกโมเดล",
            command=self.save_model
        )
        save_model_btn.pack(pady=10)
        
        # ผลการเทรน
        result_frame = ctk.CTkFrame(self.tab_train)
        result_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        result_title = ModernLabel(result_frame, text="📊 ผลการเทรน")
        result_title.pack(pady=5)
        
        self.train_text = ModernTextBox(result_frame)
        self.train_text.pack(fill="both", expand=True, pady=10)
    
    # ============ Data Tab Methods ============
    
    def select_image_file(self):
        """เลือกไฟล์ภาพ"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.selected_image_path = file_path
            filename = Path(file_path).name
            self.image_label.configure(text=f"✅ {filename}")
    
    def select_data_file(self):
        """เลือกไฟล์ข้อมูล"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Data Files", "*.csv *.xlsx *.json"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.selected_data_path = file_path
            filename = Path(file_path).name
            self.data_label.configure(text=f"✅ {filename}")
    
    def on_image_selected(self, file_path):
        """เมื่อเลือกไฟล์ภาพ"""
        pass
    
    def on_data_selected(self, file_path):
        """เมื่อเลือกไฟล์ข้อมูล"""
        pass
    
    def save_image(self):
        """บันทึกไฟล์ภาพ"""
        if not hasattr(self, 'selected_image_path'):
            show_warning("ข้อผิดพลาด", "กรุณาเลือกไฟล์ภาพ")
            return
        
        file_path = self.selected_image_path
        success, message = self.data_loader.save_image(file_path)
        
        if success:
            show_success("สำเร็จ", message)
            self.image_label.configure(text="ยังไม่ได้เลือกไฟล์")
            del self.selected_image_path
        else:
            show_error("เกิดข้อผิดพลาด", message)
        
        self.refresh_data_info()
    
    def save_data(self):
        """บันทึกไฟล์ข้อมูล"""
        if not hasattr(self, 'selected_data_path'):
            show_warning("ข้อผิดพลาด", "กรุณาเลือกไฟล์ข้อมูล")
            return
        
        file_path = self.selected_data_path
        success, message = self.data_loader.save_data_file(file_path)
        
        if success:
            show_success("สำเร็จ", message)
            self.data_label.configure(text="ยังไม่ได้เลือกไฟล์")
            del self.selected_data_path
        else:
            show_error("เกิดข้อผิดพลาด", message)
        
        self.refresh_data_info()
    
    def refresh_data_info(self):
        """รีเฟรชข้อมูล"""
        # จำนวนภาพ
        images = self.data_loader.get_image_list()
        self.image_count_label.configure(text=f"{len(images)} ไฟล์" if images else "0 ไฟล์")
        
        # จำนวนข้อมูล
        rows, cols = self.data_loader.get_data_info()
        self.data_rows_label.configure(text=f"{rows} แถว" if rows > 0 else "0 แถว")
        self.data_cols_label.configure(text=f"{cols} คอลัมน์" if cols > 0 else "0 คอลัมน์")
    
    # ============ Validate Tab Methods ============
    
    def check_data(self):
        """ตรวจสอบข้อมูล"""
        self.validate_text.delete("1.0", "end")
        
        success, message = self.data_validator.load_data()
        
        if not success:
            self.validate_text.insert("end", f"❌ {message}")
            return
        
        summary = self.data_validator.get_summary()
        self.validate_text.insert("end", summary)
    
    def remove_missing(self):
        """ลบค่าว่าง"""
        success, message = self.data_validator.load_data()
        
        if not success:
            show_error("เกิดข้อผิดพลาด", message)
            return
        
        success, message = self.data_validator.remove_missing_values()
        
        if success:
            show_success("สำเร็จ", message)
            self.check_data()
        else:
            show_error("เกิดข้อผิดพลาด", message)
    
    def remove_duplicates(self):
        """ลบแถวซ้ำ"""
        success, message = self.data_validator.load_data()
        
        if not success:
            show_error("เกิดข้อผิดพลาด", message)
            return
        
        success, message = self.data_validator.remove_duplicates()
        
        if success:
            show_success("สำเร็จ", message)
            self.check_data()
        else:
            show_error("เกิดข้อผิดพลาด", message)
    
    # ============ Train Tab Methods ============
    
    def train_model(self):
        """เทรนโมเดล"""
        
        if self.model_trainer is None:
            show_error("เกิดข้อผิดพลาด", "TensorFlow ยังไม่ได้ติดตั้ง")
            return
        
        self.train_text.delete("1.0", "end")
        self.train_text.insert("end", "⏳ กำลังเตรียมข้อมูล...\n")
        self.update()
        
        # ดึงค่า
        target_column = self.target_entry.get()
        try:
            epochs = int(self.epochs_entry.get())
            batch_size = int(self.batch_entry.get())
        except ValueError:
            show_error("เกิดข้อผิดพลาด", "Epochs และ Batch Size ต้องเป็นตัวเลข")
            return
        
        if not target_column:
            show_error("เกิดข้อผิดพลาด", "กรุณาป้อนชื่อคอลัมน์เป้าหมาย")
            return
        
        # โหลดข้อมูล
        df = self.data_loader.load_data()
        if df is None:
            show_error("เกิดข้อผิดพลาด", "ไม่พบไฟล์ข้อมูล")
            return
        
        # เตรียมข้อมูล
        success, message, data_info = self.model_trainer.prepare_data(df, target_column)
        
        if not success:
            self.train_text.insert("end", f"❌ {message}")
            return
        
        self.train_text.insert("end", f"{message}\n\n")
        self.train_text.insert("end", "🏗️ สร้างโมเดล...\n")
        self.update()
        
        # สร้างโมเดล
        num_classes = len(set(data_info['y_train']))
        self.model_trainer.build_model(data_info['input_dim'], num_classes)
        
        self.train_text.insert("end", f"✅ โมเดลสำเร็จ\n\n")
        self.train_text.insert("end", f"🚀 เทรนโมเดล ({epochs} epochs)...\n")
        self.update()
        
        # เทรน
        success, message, accuracy = self.model_trainer.train(
            data_info['X_train'],
            data_info['y_train'],
            data_info['X_test'],
            data_info['y_test'],
            epochs=epochs,
            batch_size=batch_size
        )
        
        if success:
            self.train_text.insert("end", f"\n✅ {message}\n")
            show_success("สำเร็จ", message)
        else:
            self.train_text.insert("end", f"\n❌ {message}")
            show_error("เกิดข้อผิดพลาด", message)
    
    def save_model(self):
        """บันทึกโมเดล"""
        
        if self.model_trainer is None or self.model_trainer.model is None:
            show_error("เกิดข้อผิดพลาด", "ยังไม่ได้เทรนโมเดล")
            return
        
        model_name = self.model_name_entry.get()
        
        if not model_name:
            show_error("เกิดข้อผิดพลาด", "กรุณาป้อนชื่อโมเดล")
            return
        
        success, message = self.model_trainer.save_model(model_name)
        
        if success:
            show_success("สำเร็จ", message)
            self.train_text.insert("end", f"\n{message}\n")
        else:
            show_error("เกิดข้อผิดพลาด", message)


def main():
    """ฟังก์ชันหลัก"""
    app = MeatModelTrainerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
