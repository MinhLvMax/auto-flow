# from pydantic import BaseModel, Field
# from typing import List
#
#
# class Prompt(BaseModel):
#     subject: str = Field(..., description="Chủ thể chính, vật thể trung tâm của bức ảnh.")
#     action: str = Field(..., description="Hành động, chuyển động hoặc trạng thái của chủ thể.")
#     environment: str = Field(..., description="Bối cảnh, địa điểm hoặc thế giới xung quanh.")
#     composition: str = Field(..., description="Bố cục điện ảnh (vd: quy tắc 1/3, đối xứng).")
#     camera_angle: str = Field(..., description="Góc máy (vd: góc thấp, góc nhìn chim bay).")
#     lighting: str = Field(..., description="Nguồn sáng và mood ánh sáng.")
#     atmosphere: str = Field(..., description="Yếu tố khí quyển tạo chiều sâu (vd: sương mù, khói).")
#     realism: str = Field(..., description="Các từ khóa để tăng độ chân thực.")
#     texture: str = Field(..., description="Chi tiết bề mặt vật lý.")
#     lens: str = Field(..., description="Máy ảnh và ống kính giả lập.")
#     color_science: str = Field(..., description="Hệ màu và tông màu tổng thể.")
#     style: str = Field(..., description="Aesthetic hoặc phong cách nghệ thuật.")
#     scale: str = Field(..., description="Quy mô không gian của chủ thể so với môi trường.")
#     motion: str = Field(..., description="Hiệu ứng chuyển động hoặc động năng.")
#     quality_boosters: List[str] = Field(default_factory=list, description="Danh sách các từ khóa tăng chất lượng.")
#     aspect_ratio: str = Field("16:9", description="Tỉ lệ khung hình.")
#
#     def format_prompt(self) -> str:
#         """Kết hợp các thuộc tính thành một chuỗi prompt hoàn chỉnh."""
#         boosters = ", ".join(self.quality_boosters)
#
#         # Cấu trúc prompt theo lớp lang
#         prompt_parts = [
#             f"Style: {self.style} | Realism: {self.realism}",
#             f"Subject: {self.subject} | Action: {self.action} | Environment: {self.environment}",
#             f"Composition: {self.composition} | Camera: {self.camera_angle}, {self.lens}",
#             f"Lighting: {self.lighting} | Atmosphere: {self.atmosphere} | Color: {self.color_science}",
#             f"Texture: {self.texture} | Scale: {self.scale} | Motion: {self.motion}",
#             f"Quality: {boosters}",
#             f"--ar {self.aspect_ratio}"
#         ]
#         return " ".join(prompt_parts)
#
#     @classmethod
#     def get_llm_schema(cls):
#         """Hàm này trả về mô tả để LLM hiểu được nó cần điền gì vào các trường."""
#         return {
#         field_name: field_info.description
#         for field_name, field_info in cls.model_fields.items()
#     }
#
#
# if __name__ == '__main__':
#     from pprint import pprint
#     pprint(Prompt.get_llm_schema())
