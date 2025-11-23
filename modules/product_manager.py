"""
โมดูลสำหรับจัดการข้อมูลสินค้า
"""

import pandas as pd
from pathlib import Path
from typing import Tuple, List, Dict


class ProductManager:
    """คลาสสำหรับจัดการข้อมูลสินค้า"""
    
    def __init__(self, data_file: str = "data/uploaded_data.csv"):
        """
        Args:
            data_file: ที่อยู่ไฟล์ข้อมูลสินค้า
        """
        self.data_file = Path(data_file)
        self.df = None
    
    def load_data(self) -> Tuple[bool, str]:
        """
        โหลดข้อมูลสินค้า

        Returns:
            (สำเร็จ, ข้อความ)
        """
        try:
            if not self.data_file.exists():
                return False, "ไฟล์ไม่พบ"
            
            self.df = pd.read_csv(self.data_file)
            return True, f"โหลดสำเร็จ: {len(self.df)} สินค้า"
        
        except Exception as e:
            return False, f"เกิดข้อผิดพลาด: {str(e)}"
    
    def add_product(self, product_data: Dict) -> Tuple[bool, str]:
        """
        เพิ่มสินค้าใหม่

        Args:
            product_data: dict ข้อมูลสินค้า

        Returns:
            (สำเร็จ, ข้อความ)
        """
        try:
            if self.df is None:
                self.df = pd.DataFrame([product_data])
            else:
                self.df = pd.concat([self.df, pd.DataFrame([product_data])], ignore_index=True)
            
            self.df.to_csv(self.data_file, index=False)
            return True, "เพิ่มสินค้าสำเร็จ"
        
        except Exception as e:
            return False, f"เกิดข้อผิดพลาด: {str(e)}"
    
    def get_product_by_barcode(self, barcode: str) -> Dict:
        """
        ค้นหาสินค้าตามบาร์โค้ด

        Args:
            barcode: บาร์โค้ดสินค้า

        Returns:
            dict ข้อมูลสินค้า หรือ None ถ้าไม่พบ
        """
        if self.df is None:
            return None
        
        result = self.df[self.df.get('barcode', pd.Series()) == barcode]
        
        if len(result) > 0:
            return result.iloc[0].to_dict()
        
        return None
    
    def get_all_products(self) -> List[Dict]:
        """
        ดึงรายชื่อสินค้าทั้งหมด

        Returns:
            list ข้อมูลสินค้า
        """
        if self.df is None:
            return []
        
        return self.df.to_dict('records')
    
    def update_product(self, index: int, product_data: Dict) -> Tuple[bool, str]:
        """
        อัปเดตข้อมูลสินค้า

        Args:
            index: ตำแหน่งสินค้า
            product_data: dict ข้อมูลใหม่

        Returns:
            (สำเร็จ, ข้อความ)
        """
        try:
            if self.df is None or index >= len(self.df):
                return False, "ไม่พบสินค้า"
            
            for key, value in product_data.items():
                self.df.at[index, key] = value
            
            self.df.to_csv(self.data_file, index=False)
            return True, "อัปเดตสำเร็จ"
        
        except Exception as e:
            return False, f"เกิดข้อผิดพลาด: {str(e)}"
    
    def delete_product(self, index: int) -> Tuple[bool, str]:
        """
        ลบสินค้า

        Args:
            index: ตำแหน่งสินค้า

        Returns:
            (สำเร็จ, ข้อความ)
        """
        try:
            if self.df is None or index >= len(self.df):
                return False, "ไม่พบสินค้า"
            
            self.df = self.df.drop(index).reset_index(drop=True)
            self.df.to_csv(self.data_file, index=False)
            
            return True, "ลบสำเร็จ"
        
        except Exception as e:
            return False, f"เกิดข้อผิดพลาด: {str(e)}"
