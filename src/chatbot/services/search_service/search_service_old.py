# services/search_service.py
from pathlib import Path
from src.chatbot.services.file_service.json_reader import JsonReader
from src.config import BASE_DIR
from difflib import SequenceMatcher


class SearchService:
    default_index_path = BASE_DIR / 'src' / 'chatbot' / "data_dir_space.json"

    def __init__(self, index_path=default_index_path):
        # Chuyển đổi đường dẫn thành đối tượng Path để làm việc an toàn hơn
        self.index_path = Path(index_path)
        self.tree_data = None
        self.json_reader = JsonReader()

        # Tự động tải dữ liệu khi khởi tạo dịch vụ
        self._load_index()

    def _load_index(self):
        """Tải dữ liệu cây thư mục sử dụng JsonReader"""
        if not self.index_path.exists():
            print(f"Cảnh báo: Không tìm thấy file index tại {self.index_path}")
            self.tree_data = {}
            return

        # Sử dụng đúng hàm read đã có của JsonReader
        self.tree_data = self.json_reader.read(self.index_path)
        if self.tree_data is None:
            self.tree_data = {}

    def _recursive_search(self, current_node: dict, current_path: list, query: str, results: list):
        """
        Hàm nội bộ duyệt cây đệ quy để tìm kiếm từ khóa.
        - current_node: Node hiện tại đang xét (dict)
        - current_path: Danh sách các thư mục cha dẫn đến node này
        - query: Từ khóa tìm kiếm (đã viết thường)
        - results: Danh sách lưu các đường dẫn tìm thấy
        """
        if not isinstance(current_node, dict):
            return

        for key, value in current_node.items():
            # Tạo đường dẫn mới bao gồm cả key hiện tại
            new_path = current_path + [key]

            # Kiểm tra xem tên file/thư mục (key) có chứa từ khóa tìm kiếm không
            if query in key.lower():
                # Chuyển đổi danh sách [folder1, folder2, file] thành "/folder1/folder2/file"
                path_str = "/" + "/".join(new_path)
                results.append(path_str)

            # Nếu giá trị là một dict (tức là thư mục con), tiếp tục duyệt đệ quy vào trong
            if isinstance(value, dict):
                self._recursive_search(value, new_path, query, results)

    def _search_by_keyword(self, query: str) -> list:
        """Cơ chế tìm kiếm theo từ khóa (Không phân biệt chữ hoa/thường)"""
        if not self.tree_data:
            return []

        results = []
        # Chuyển query về dạng chữ thường để so sánh không phân biệt hoa thường
        clean_query = query.strip().lower()

        if not clean_query:
            return []

        # Bắt đầu duyệt cây từ gốc (root) với danh sách đường dẫn rỗng []
        self._recursive_search(self.tree_data, [], clean_query, results)
        return results

    def _search_by_semantic(self, query: str) -> list:
        """Cơ chế tìm kiếm theo ý nghĩa (Dành cho việc nâng cấp sau này)"""
        # Hiện tại chưa triển khai, trả về danh sách rỗng
        return []

    def _fuzzy_compare(self, target: str, query: str, threshold=0.6) -> bool:
        """
        Hàm so sánh mờ giữa từ khóa (query) và tên file/thư mục (target).
        Trả về True nếu độ tương đồng lớn hơn hoặc bằng threshold (mặc định là 60%).
        """
        target_lower = target.lower()
        query_lower = query.lower()

        # 1. Nếu từ khóa nằm trực tiếp trong tên (Ví dụ: "troi" nằm trong "Mặt_Trời") -> Khớp luôn
        if query_lower in target_lower:
            return True

        # 2. Tách tên file/thư mục thành các từ đơn để so sánh (loại bỏ gạch dưới và dấu chấm)
        words = target_lower.replace("_", " ").replace(".", " ").split()
        for word in words:
            # Tính tỉ lệ tương đồng giữa từ khóa và từng từ trong tên file
            similarity = SequenceMatcher(None, query_lower, word).ratio()
            if similarity >= threshold:
                return True

        return False

    def _recursive_fuzzy_search(self, current_node: dict, current_path: list, query: str, results: list):
        """Duyệt cây đệ quy tương tự như keyword search nhưng áp dụng so sánh mờ"""
        if not isinstance(current_node, dict):
            return

        for key, value in current_node.items():
            new_path = current_path + [key]

            # Sử dụng hàm so sánh mờ vừa viết ở trên
            if self._fuzzy_compare(key, query):
                path_str = "/" + "/".join(new_path)
                results.append(path_str)

            if isinstance(value, dict):
                self._recursive_fuzzy_search(value, new_path, query, results)

    def _search_by_fuzzy(self, query: str) -> list:
        """Cơ chế tìm kiếm mờ"""
        if not self.tree_data:
            return []

        results = []
        clean_query = query.strip()

        if not clean_query:
            return []

        self._recursive_fuzzy_search(self.tree_data, [], clean_query, results)
        return results

    def execute(self, query: str, strategy: str = "keyword") -> list:
        """Hàm điều phối chính hỗ trợ cả keyword và fuzzy search"""
        if strategy == "semantic":
            return self._search_by_semantic(query)
        elif strategy == "fuzzy":
            return self._search_by_fuzzy(query)
        return self._search_by_keyword(query)


# Đoạn code chạy thử độc lập để kiểm tra (Test)
if __name__ == '__main__':
    # Giả định file dữ liệu nằm cùng cấp hoặc ở thư mục gốc của dự án
    test_service = SearchService()

    # Từ khóa thử nhiệm
    keyword_to_find = "Sao mộc"
    found_paths = test_service.execute(keyword_to_find, strategy="fuzzy")

    print(f"--- Kết quả tìm kiếm cho từ khóa '{keyword_to_find}': ---")
    for path in found_paths:
        print(path)
