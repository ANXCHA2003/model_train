"""
โมดูลสำหรับเทรนโมเดล Machine Learning
"""

import os
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple, Optional

try:
    import tensorflow as tf
    from tensorflow import keras
    layers = keras.layers
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False


class ModelTrainer:
    """คลาสสำหรับเทรนโมเดล Neural Network"""
    
    def __init__(self, models_dir: str = "models"):
        """
        Args:
            models_dir: ที่อยู่โฟลเดอร์เก็บโมเดล
        """
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.model = None
        self.history = None
        
        if not TF_AVAILABLE:
            raise ImportError("ต้องติดตั้ง TensorFlow: pip install tensorflow")
    
    def prepare_data(self, df: pd.DataFrame, target_column: str, 
                    test_size: float = 0.2) -> Tuple[bool, str, Optional[dict]]:
        """
        เตรียมข้อมูลสำหรับเทรน

        Args:
            df: DataFrame ข้อมูล
            target_column: ชื่อคอลัมน์เป้าหมาย
            test_size: สัดส่วนข้อมูล test

        Returns:
            (สำเร็จ, ข้อความ, dict ข้อมูล)
        """
        try:
            if target_column not in df.columns:
                return False, f"ไม่พบคอลัมน์: {target_column}", None
            
            # แยก X และ y
            X = df.drop(columns=[target_column])
            y = df[target_column]
            
            # เลือกเฉพาะคอลัมน์ตัวเลข
            numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
            X = X[numeric_cols]
            
            if len(numeric_cols) == 0:
                return False, "ไม่มีคอลัมน์ตัวเลข", None
            
            # แปลง y เป็นตัวเลข (ถ้าเป็น categorical)
            if y.dtype == 'object':
                y = pd.factorize(y)[0]
            
            # แบ่งข้อมูล train/test
            from sklearn.model_selection import train_test_split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42
            )
            
            # Normalize ข้อมูล
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)
            
            data_info = {
                'X_train': X_train,
                'X_test': X_test,
                'y_train': y_train,
                'y_test': y_test,
                'input_dim': len(numeric_cols),
                'scaler': scaler
            }
            
            return True, f"เตรียมข้อมูลสำเร็จ: {len(X_train)} train, {len(X_test)} test", data_info
        
        except Exception as e:
            return False, f"เกิดข้อผิดพลาด: {str(e)}", None
    
    def build_model(self, input_dim: int, num_classes: Optional[int] = None) -> None:
        """
        สร้างโมเดล Neural Network

        Args:
            input_dim: จำนวน input features
            num_classes: จำนวน output classes (ถ้าเป็น classification)
        """
        self.model = keras.Sequential([
            layers.Dense(128, activation='relu', input_dim=input_dim),
            layers.Dropout(0.2),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dense(16, activation='relu'),
            layers.Dense(num_classes if num_classes and num_classes > 2 else 1, 
                        activation='softmax' if (num_classes and num_classes > 2) else 'sigmoid')
        ])
        
        # Compile
        loss = 'sparse_categorical_crossentropy' if (num_classes and num_classes > 2) else 'binary_crossentropy'
        self.model.compile(
            optimizer='adam',
            loss=loss,
            metrics=['accuracy']
        )
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray, 
             X_test: np.ndarray, y_test: np.ndarray,
             epochs: int = 50, batch_size: int = 32) -> Tuple[bool, str, Optional[float]]:
        """
        เทรนโมเดล

        Args:
            X_train: ข้อมูล training
            y_train: ป้ายกำกับ training
            X_test: ข้อมูล test
            y_test: ป้ายกำกับ test
            epochs: จำนวน epoch
            batch_size: ขนาด batch

        Returns:
            (สำเร็จ, ข้อความ, accuracy)
        """
        try:
            if self.model is None:
                return False, "โมเดลยังไม่ได้สร้าง", None
            
            # เทรน
            self.history = self.model.fit(
                X_train, y_train,
                epochs=epochs,
                batch_size=batch_size,
                validation_data=(X_test, y_test),
                verbose=0
            )
            
            # ประเมิน
            test_loss, test_accuracy = self.model.evaluate(X_test, y_test, verbose=0)
            
            return True, f"เทรนสำเร็จ! Accuracy: {test_accuracy:.4f}", test_accuracy
        
        except Exception as e:
            return False, f"เกิดข้อผิดพลาด: {str(e)}", None
    
    def save_model(self, model_name: str = "my_model") -> Tuple[bool, str]:
        """
        บันทึกโมเดล (.h5 และ .tflite)

        Args:
            model_name: ชื่อโมเดล

        Returns:
            (สำเร็จ, ข้อความ)
        """
        try:
            if self.model is None:
                return False, "ไม่มีโมเดล"
            
            # บันทึก H5
            h5_path = self.models_dir / f"{model_name}.h5"
            self.model.save(str(h5_path))
            
            # บันทึก TFLite
            converter = tf.lite.TFLiteConverter.from_keras_model(self.model)
            converter.optimizations = [tf.lite.Optimize.DEFAULT]
            tflite_model = converter.convert()
            
            tflite_path = self.models_dir / f"{model_name}.tflite"
            with open(str(tflite_path), 'wb') as f:
                f.write(tflite_model)
            
            return True, f"บันทึกสำเร็จ:\n- {h5_path}\n- {tflite_path}"
        
        except Exception as e:
            return False, f"เกิดข้อผิดพลาด: {str(e)}"
    
    def get_model_summary(self) -> str:
        """
        ดึงสรุปโมเดล

        Returns:
            ข้อความสรุป
        """
        if self.model is None:
            return "ไม่มีโมเดล"
        
        summary = []
        self.model.summary(print_fn=lambda x: summary.append(x))
        return "\n".join(summary)
