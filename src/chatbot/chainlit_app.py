import chainlit as cl
import asyncio
import subprocess
from src.chatbot.services.chatbot_service import ChatbotService
from src.chatbot.indexing.indexer_old import Indexer
from src.chatbot.config import DEDAULT_ROOT_PATH
from src.loggers import main_logger
from pathlib import Path

main_logger.info('Khởi tạo dịch vụ chat')
chatbot_service = ChatbotService()

async def index_folder(path_to_index):
    loading_msg = cl.Message(
        content="⚙️ Hệ thống đang tiến hành lập chỉ mục cây thư mục dữ liệu, vui lòng đợi trong giây lát..."
    )
    await loading_msg.send()

    # Xây dựng index
    # path_to_index = r'C:\Users\Admin\Downloads'
    indexer = Indexer()
    await asyncio.to_thread(
        indexer.build_index_v2,
        path_to_index,
    )

    loading_msg.content = "✅ Đã lập chỉ mục cây thư mục dữ liệu thành công!"
    await loading_msg.update()

@cl.action_callback('re_index')
async def re_index(action: cl.Action):
    path = cl.user_session.get('path_to_index', None)
    await index_folder(path)
    pass

@cl.on_chat_start
async def on_chat_start():
    # await cl.ChatSettings(
    #     [
    #         TextInput(
    #             id="index_path",
    #             label="📂 Folder cần index",
    #             initial=r"C:\Users\Admin\Downloads"
    #         )
    #     ]
    # ).send()
    default_path_to_index = DEDAULT_ROOT_PATH # Nên cải tiến lấy từ người dùng
    history = chatbot_service.create_session(path_to_index=default_path_to_index)
    last_turn = history.last()
    first_mess = last_turn.get('content', 'Xin chào bạn.')
    await cl.Message(
        content=first_mess
    ).send()
    cl.user_session.set('history', history)
    cl.user_session.set('path_to_index', default_path_to_index)


@cl.on_message
async def on_message(message: cl.Message):
    main_logger.info('Nhận xin nhắn và xử lý')
    try:
        history = cl.user_session.get('history', None)
        if history:
            history.add('user', message.content)
            new_history, paths_result = chatbot_service.chat(history=history)
            response = new_history.last().get('content', 'None')
            history.add('assistant', response)
        else:
            response = 'Thử lại'
            paths_result = []

        cl.user_session.set('history', history)
        cl.user_session.set('paths_result', paths_result)

        actions = []

        if paths_result:
            actions.append(
                cl.Action(
                    name="show_search_results",
                    label=f"Xem {len(paths_result)} tài liệu",
                    payload={}
                )
            )
        actions.append(
            cl.Action(
                name="re_index",
                label='Re-index thư mục',
                payload={}
            )
        )

        await cl.Message(
            content=response,
            actions=actions
        ).send()
    except Exception as e:
        await cl.Message(
            content= f'Có lỗi xảy ra: {e}'
        ).send()


@cl.action_callback("open_file")
async def open_file(action: cl.Action):
    path = Path(action.payload["path"]).resolve()

    subprocess.Popen(
        f'explorer.exe /select,"{path}"'
    )



@cl.action_callback("show_search_results")
async def show_search_results(action: cl.Action):
    paths_result = cl.user_session.get("paths_result", [])

    paths_result = paths_result[:70]  # Lấy tối đa 100 link thôi

    actions = []

    content = " **Kết quả tìm kiếm**\n\n"

    for item in paths_result:
        path = item["path"]

        # content += (
        #     f"- `{path}`\n"
        #     f"  Score: {item['score']}\n\n"
        # )

        actions.append(
            cl.Action(
                name="open_file",
                label=f"{path} score:{item['score']}",
                payload={
                    "path": path
                }
            )
        )

    await cl.Message(
        content=content,
        actions=actions
    ).send()

# python -m chainlit run chainlit_app.py
