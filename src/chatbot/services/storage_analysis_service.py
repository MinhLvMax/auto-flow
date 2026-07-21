from pathlib import Path
from src.chatbot.services.file_service.json_reader import JsonReader
from src.chatbot.config import FILES_INDEX_PATH, FOLDERS_INDEX_PATH
from src.chatbot.services.groq_llm_services import GroqServices

class StorageAnalysisService:
    '''
    Cung cấp các cơ chế phân tích kho
    '''
    def __init__(self, files_index_path = None, folders_index_path = None, json_loader = None, llm_service = None):
        self.files_index_path = files_index_path or FILES_INDEX_PATH
        self.folders_index_path = folders_index_path or FOLDERS_INDEX_PATH
        self.json_loader = json_loader or JsonReader()
        self.llm_service = llm_service or GroqServices()

        # Bộ đệm dữ liệu sau khi nạp
        self.files_data = []
        self.folders_data = []

        # Tự động nạp dữ liệu khi khởi tạo dịch vụ
        self.load_indexes()

    def load_indexes(self) -> bool:
        """
        Nạp dữ liệu từ files_index.json và folders_index.json vào bộ nhớ.
        """
        try:
            self.files_data = self.json_loader.read(Path(self.files_index_path)) or []
            self.folders_data = self.json_loader.read(Path(self.folders_index_path)) or []
            return True
        except Exception:
            self.files_data = []
            self.folders_data = []
            return False

    def get_storage_overview(self) -> dict:
        """
        Phân tích và trả về thông tin tổng quan của kho tài nguyên.
        """
        if not self.files_data:
            return {
                "total_files": 0,
                "total_folders": 0,
                "total_size_bytes": 0,
                "total_size_friendly": "0 KB",
                "file_types": {}
            }

        total_files = len(self.files_data)
        total_folders = len(self.folders_data)

        # Tính toán tổng dung lượng
        total_size_bytes = sum(item.get("size", 0) for item in self.files_data)
        total_size_friendly = self._format_size(total_size_bytes)

        # Thống kê phân loại đuôi file
        file_types = {}
        for item in self.files_data:
            suffix = item.get("suffix", "").lower().strip()
            if not suffix:
                suffix = "unknown"
            file_types[suffix] = file_types.get(suffix, 0) + 1

        # Sắp xếp định dạng file xuất hiện nhiều nhất lên trước
        sorted_file_types = dict(
            sorted(file_types.items(), key=lambda x: x[1], reverse=True)
        )

        return {
            "total_files": total_files,
            "total_folders": total_folders,
            "total_size_bytes": total_size_bytes,
            "total_size_friendly": total_size_friendly,
            "file_types": sorted_file_types
        }

    def get_directory_tree_prompt(self, max_depth: int = 3, max_entries: int = 40) -> str:
        """
        Xây dựng chuỗi sơ đồ cây thư mục rút gọn dựa trên dữ liệu folders_index.
        - max_depth: Độ sâu tối đa hiển thị (tính từ thư mục gốc của kho).
        - max_entries: Số lượng thư mục tối đa được liệt kê để tránh Token quá lớn.
        """
        if not self.folders_data:
            return "Chưa có dữ liệu cấu trúc thư mục."

        # Sắp xếp các thư mục theo thứ tự phân cấp bảng chữ cái
        sorted_folders = sorted(self.folders_data, key=lambda x: x.get("path", ""))

        # Xác định thư mục gốc để làm mốc tính độ sâu tương đối
        root_folder = sorted_folders[0]
        root_path_obj = Path(root_folder.get("path", ""))
        root_parts_len = len(root_path_obj.parts)

        tree_lines = []
        tree_lines.append(f"📁 {root_path_obj.name}/ (Gốc)")

        entries_count = 0
        omitted_count = 0

        for item in sorted_folders[1:]:  # Bỏ qua thư mục gốc đã in ở đầu
            folder_path_str = item.get("path", "")
            folder_path_obj = Path(folder_path_str)

            # Tính độ sâu tương đối của thư mục con so với gốc
            relative_depth = len(folder_path_obj.parts) - root_parts_len

            # Bỏ qua nếu vượt quá độ sâu cấu hình
            if relative_depth > max_depth:
                continue

            # Kiểm tra giới hạn số lượng dòng để tránh tràn Token
            if entries_count >= max_entries:
                omitted_count += 1
                continue

            indent = "    " * relative_depth
            file_count = item.get("file_count", 0)
            subfolder_count = item.get("subfolder_count", 0)

            # Định dạng hiển thị trực quan thông tin số lượng bên trong thư mục
            meta_info = f"({file_count} files, {subfolder_count} folders)"
            tree_lines.append(f"{indent}└── 📁 {folder_path_obj.name}/ {meta_info}")

            entries_count += 1

        if omitted_count > 0:
            tree_lines.append(f"    ... (và {omitted_count} thư mục con khác đã được ẩn để tối ưu dung lượng)")

        return "\n".join(tree_lines)

    def get_warehouse_summary_prompt(self) -> str:
        """
        Tổng hợp cả hai thông tin: Số liệu tổng quan + Sơ đồ cây rút gọn
        để trả về một chuỗi Prompt hoàn chỉnh nạp vào hệ thống.
        """
        overview = self.get_storage_overview()
        tree_structure = self.get_directory_tree_prompt(max_depth=3, max_entries=35)

        if overview["total_files"] == 0:
            return "Kho dữ liệu hiện tại đang trống hoặc chưa được lập chỉ mục."

        # ext_summary = ", ".join([f"{k} ({v})" for k, v in overview["file_types"].items()])

        return (
            f"--- BÁO CÁO TỔNG QUAN KHO DỮ LIỆU ---\n"
            f"- Tổng số lượng file: {overview['total_files']} file\n"
            f"- Tổng số lượng thư mục: {overview['total_folders']} thư mục\n"
            f"- Tổng dung lượng toàn kho: {overview['total_size_friendly']}\n"
            # f"- Định dạng phân loại file: {ext_summary}\n\n"
            f"--- SƠ ĐỒ CẤU TRÚC THƯ MỤC CHÍNH ---\n"
            f"{tree_structure}"
        )

    def _format_size(self, size_bytes: int) -> str:
        """Chuyển đổi kích thước byte sang định dạng thân thiện hơn (KB, MB, GB)"""
        if size_bytes == 0:
            return "0 Bytes"

        # Thống kê dung lượng thô
        size_kb = size_bytes / 1024
        size_mb = size_kb / 1024
        size_gb = size_mb / 1024

        if size_gb >= 1.0:
            return f"{size_gb:.2f} GB"
        elif size_mb >= 1.0:
            return f"{size_mb:.2f} MB"
        else:
            return f"{size_kb:.1f} KB"


if __name__ == '__main__':
    storage_analysis_service = StorageAnalysisService()
    print(storage_analysis_service.get_warehouse_summary_prompt())





