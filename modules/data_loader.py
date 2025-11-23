"""
โมดูลสำหรับโหลด อัปโหลด และจัดเก็บไฟล์ข้อมูล
"""

import os
import shutil
from pathlib import Path
import pandas as pd
from typing import Tuple, List


class DataLoader:
    """คลาสสำหรับจัดการการโหลดและบันทึกข้อมูล"""
    
    def __init__(self, data_dir: str = "data"):
        """
        Args:
            data_dir: ที่อยู่โฟลเดอร์เก็บข้อมูล
        """
        self.data_dir = Path(data_dir)
        self.images_dir = self.data_dir / "images"
        self.data_file = self.data_dir / "uploaded_data.csv"
        
        # สร้างโฟลเดอร์ถ้ายังไม่มี
        self.images_dir.mkdir(parents=True, exist_ok=True)
    
    def save_image(self, source_path: str) -> Tuple[bool, str]:
        """
        บันทึกไฟล์ภาพ

        Args:
            source_path: ที่อยู่ไฟล์ต้นฉบับ

        Returns:
            (สำเร็จ, ข้อความ)
        """
        try:
            source = Path(source_path)
            if not source.exists():
                return False, "ไฟล์ไม่พบ"
            
            # ตรวจสอบนามสกุลไฟล์
            valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
            if source.suffix.lower() not in valid_extensions:
                return False, f"นามสกุลไม่รองรับ: {source.suffix}"
            
            # คัดลอกไฟล์ไปยังโฟลเดอร์ images
            destination = self.images_dir / source.name
            shutil.copy2(source, destination)
            
            return True, f"บันทึกสำเร็จ: {source.name}"
        
        except Exception as e:
            return False, f"เกิดข้อผิดพลาด: {str(e)}"
    
    def save_data_file(self, source_path: str) -> Tuple[bool, str]:
        """
        บันทึกไฟล์ข้อมูล (.csv, .xlsx, .json)

        Args:
            source_path: ที่อยู่ไฟล์ต้นฉบับ

        Returns:
            (สำเร็จ, ข้อความ)
        """
        try:
            source = Path(source_path)
            if not source.exists():
                return False, "ไฟล์ไม่พบ"
            
            # อ่านไฟล์ตามนามสกุล
            if source.suffix.lower() == '.csv':
                df = pd.read_csv(source)
            elif source.suffix.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(source)
            elif source.suffix.lower() == '.json':
                df = pd.read_json(source)
            else:
                return False, f"นามสกุลไม่รองรับ: {source.suffix}"
            
            # บันทึกเป็น CSV
            df.to_csv(self.data_file, index=False)
            
            return True, f"บันทึกสำเร็จ: {len(df)} แถว"
        
        except Exception as e:
            return False, f"เกิดข้อผิดพลาด: {str(e)}"
    
    def get_image_list(self) -> List[str]:
        """
        ดึงรายชื่อไฟล์ภาพทั้งหมด

        Returns:
            รายชื่อไฟล์ภาพ
        """
        valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
        images = [f.name for f in self.images_dir.iterdir() 
                 if f.suffix.lower() in valid_extensions]
        return sorted(images)
    
    def get_data_info(self) -> Tuple[int, int]:
        """
        ดึงข้อมูลของไฟล์ข้อมูล

        Returns:
            (จำนวนแถว, จำนวนคอลัมน์)
        """
        if not self.data_file.exists():
            return 0, 0
        
        try:
            df = pd.read_csv(self.data_file)
            return len(df), len(df.columns)
        except:
            return 0, 0
    
    def load_data(self) -> pd.DataFrame:
        """
        โหลดไฟล์ข้อมูล

        Returns:
            DataFrame หรือ None ถ้าไม่พบไฟล์
        """
        if not self.data_file.exists():
            return None
        
        try:
            return pd.read_csv(self.data_file)
        except:
            return None
