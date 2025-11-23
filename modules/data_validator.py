"""
โมดูลสำหรับตรวจสอบและทำความสะอาดข้อมูล
"""

import pandas as pd
from typing import Dict, List, Tuple
from pathlib import Path


class DataValidator:
    """คลาสสำหรับตรวจสอบคุณภาพข้อมูล"""
    
    def __init__(self, data_file: str = "data/uploaded_data.csv"):
        """
        Args:
            data_file: ที่อยู่ไฟล์ข้อมูล
        """
        self.data_file = Path(data_file)
        self.df = None
    
    def load_data(self) -> Tuple[bool, str]:
        """
        โหลดไฟล์ข้อมูล

        Returns:
            (สำเร็จ, ข้อความ)
        """
        try:
            if not self.data_file.exists():
                return False, "ไฟล์ข้อมูลยังไม่ได้อัปโหลด"
            
            self.df = pd.read_csv(self.data_file)
            return True, f"โหลดสำเร็จ: {len(self.df)} แถว"
        
        except Exception as e:
            return False, f"เกิดข้อผิดพลาด: {str(e)}"
    
    def check_missing_values(self) -> Dict[str, int]:
        """
        ตรวจสอบค่าว่าง

        Returns:
            dict เก็บชื่อคอลัมน์และจำนวนค่าว่าง
        """
        if self.df is None:
            return {}
        
        missing = self.df.isnull().sum()
        return missing[missing > 0].to_dict()
    
    def check_duplicates(self) -> int:
        """
        ตรวจสอบแถวซ้ำ

        Returns:
            จำนวนแถวซ้ำ
        """
        if self.df is None:
            return 0
        
        return self.df.duplicated().sum()
    
    def check_data_types(self) -> Dict[str, str]:
        """
        ตรวจสอบประเภทข้อมูล

        Returns:
            dict เก็บชื่อคอลัมน์และประเภทข้อมูล
        """
        if self.df is None:
            return {}
        
        return self.df.dtypes.to_dict()
    
    def get_summary(self) -> str:
        """
        ดึงสรุปข้อมูล

        Returns:
            ข้อความสรุป
        """
        if self.df is None:
            return "ไม่มีข้อมูล"
        
        summary = f"📊 สรุปข้อมูล:\n"
        summary += f"├─ จำนวนแถว: {len(self.df)}\n"
        summary += f"├─ จำนวนคอลัมน์: {len(self.df.columns)}\n"
        summary += f"├─ คอลัมน์: {', '.join(self.df.columns)}\n"
        
        # ค่าว่าง
        missing = self.check_missing_values()
        if missing:
            summary += f"├─ ⚠️ ค่าว่าง:\n"
            for col, count in missing.items():
                summary += f"│  ├─ {col}: {count}\n"
        
        # แถวซ้ำ
        duplicates = self.check_duplicates()
        if duplicates > 0:
            summary += f"├─ ⚠️ แถวซ้ำ: {duplicates}\n"
        
        summary += f"└─ ✅ ข้อมูลพร้อม"
        
        return summary
    
    def remove_missing_values(self) -> Tuple[bool, str]:
        """
        ลบแถวที่มีค่าว่าง

        Returns:
            (สำเร็จ, ข้อความ)
        """
        if self.df is None:
            return False, "ไม่มีข้อมูล"
        
        try:
            original_len = len(self.df)
            self.df = self.df.dropna()
            new_len = len(self.df)
            removed = original_len - new_len
            
            # บันทึกไฟล์
            self.df.to_csv(self.data_file, index=False)
            
            return True, f"ลบแถวที่มีค่าว่าง {removed} แถว"
        
        except Exception as e:
            return False, f"เกิดข้อผิดพลาด: {str(e)}"
    
    def remove_duplicates(self) -> Tuple[bool, str]:
        """
        ลบแถวซ้ำ

        Returns:
            (สำเร็จ, ข้อความ)
        """
        if self.df is None:
            return False, "ไม่มีข้อมูล"
        
        try:
            original_len = len(self.df)
            self.df = self.df.drop_duplicates()
            new_len = len(self.df)
            removed = original_len - new_len
            
            # บันทึกไฟล์
            self.df.to_csv(self.data_file, index=False)
            
            return True, f"ลบแถวซ้ำ {removed} แถว"
        
        except Exception as e:
            return False, f"เกิดข้อผิดพลาด: {str(e)}"
