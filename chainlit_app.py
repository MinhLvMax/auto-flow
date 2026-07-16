import chainlit as cl
from src.chatbot.services.chatbot_service import ChatbotService
from src.loggers import main_logger
from pathlib import Path

main_logger.info('Khởi tạo dịch vụ chat')
chatbot_service = ChatbotService()


@cl.on_chat_start
async def on_chat_start():
    history = chatbot_service.create_session()
    last_turn = history.last()
    first_mess = last_turn.get('content', 'Xin chào bạn.')
    await cl.Message(
        content=first_mess
    ).send()
    cl.user_session.set('history', history)


@cl.on_message
async def on_message(message: cl.Message):
    main_logger.info('Nhận xin nhắn và xử lý')
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

    # for path in paths_result:
    #     actions.append(
    #         cl.Action(
    #             name="open_file",
    #             label=path.get('path', '').split("/")[-1],
    #             payload={"path": path}
    #         )
    #     )


    await cl.Message(
        content=response,
        actions=actions
    ).send()


@cl.action_callback("open_file")
async def open_file(action: cl.Action):
    import os
    path = action.payload["path"]
    os.startfile(path)

@cl.action_callback("show_search_results")
async def show_search_results(action: cl.Action):

    paths_result = cl.user_session.get(
        "paths_result",
        []
    )

    actions = []

    content = "## Kết quả tìm kiếm\n\n"

    for item in paths_result:

        path = item["path"]

        # content += (
        #     f"- `{path}`\n"
        #     f"  Score: {item['score']}\n\n"
        # )

        actions.append(
            cl.Action(
                name="open_file",
                label=f"{Path(path).name}\n\n{path}",
                payload={
                    "path": path
                }
            )
        )


    await cl.Message(
        content=content,
        actions=actions
    ).send()

#python -m chainlit run chainlit_app.py