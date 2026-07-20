from pydantic import BaseModel


class History(BaseModel):
    # Chỉ nên lưu hội thoại, còn system thì gọi ở đâu thì chỗ đó thêm, vì mỗi chỗ có system prompt nó khác
    messages: list[dict] = []

    def add(self, role: str, content: str):
        if role == 'system':
            return
        self.messages.append({
            "role": role,
            "content": content
        })

    def last(self):
        return self.messages[-1]

    def to_messages(self, system_prompt: str | None = None, last_n: int = 7):
        '''
        Tùy chỗ gọi mà nó sẽ thêm system prompt khác nhau
        :param system_prompt:
        :return:
        '''
        # Loại bỏ các tin system message ra để ghi đề system mess mới tránh lẫn vai trò
        messages = [msg for msg in self.messages if msg.get("role") in ("user", "assistant")]

        if last_n is not None:
            messages = messages[-last_n:]
            
        if system_prompt:
            return [
                {
                    "role": "system",
                    "content": system_prompt
                },
                *messages
            ]

        return self.messages
