JSON_RESPONSE_PROMPT = '''
{text}
Return ONLY a valid JSON object.

Schema:
{schema}

Rules:
- Do not wrap in ```json
- Do not include explanations
- Do not add extra fields
- All required fields must be present
'''

SENTENCE_BOUNDARY_PROMPT = """
Bạn là chuyên gia phân tích kịch bản.

Nhiệm vụ:
Xác định xem câu hiện tại có bắt đầu một đơn vị nội dung (new unit) mới hay không.

Đơn vị mới có thể xuất hiện khi có sự thay đổi rõ ràng về:
- Chủ đề chính.
- Bối cảnh hoặc địa điểm.
- Thời gian.
- Đối tượng hoặc nhân vật được tập trung.
- Mạch nội dung chuyển sang ý lớn khác.

Ngữ cảnh trước:
{context}

Câu hiện tại:
{sentence}

Hãy đưa ra quyết định dựa trên ngữ cảnh và câu hiện tại.
"""