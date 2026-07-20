from pathlib import Path
import os
import chainlit as cl
from chainlit.input_widget import Select, Slider
from src.chatbot.services.groq_llm_services import GroqServices


# chainlit run research_chainlit.py -w

@cl.on_chat_start
async def start():
    await cl.ChatSettings(
        [
            Select(
                id="model",
                label="Model",
                values=["GPT-4o", "GPT-4o-mini", "Llama3"],
                initial_index=0
            ),
            Slider(
                id="temperature",
                label="Temperature",
                initial=0.7,
                min=0,
                max=2,
                step=0.1
            )
        ]
    ).send()

    await cl.Message(
        content="Xin chào! Tôi có thể giúp gì cho bạn?",
    ).send()

@cl.on_settings_update
async def update(settings):
    print(settings)

@cl.on_message
async def on_message(message: cl.Message):
    actions = [
        cl.Action(
            name="yes",
            label="Đồng ý",
            payload={"value": "yes"}
        ),
        cl.Action(
            name="no",
            label="Không",
            payload={"value": "no"}
        )
    ]

    # files = [cl.File(
    #     name="Ảnh",
    #     path=r"C:\Users\Admin\Downloads\LD518.jpg",
    # ), cl.File(
    #     name="Video",
    #     path=r"C:\Users\Admin\Downloads\AI.mp4",
    # )]

    actions += [cl.Action(
        name="view_file",
        label=r"LD518.jpg",
        payload={"path": r"C:\Users\Admin\Downloads\LD518.jpg"}
    ), cl.Action(
        name="view_file",
        label=r"AI.mp4",
        payload={"path": r"C:\Users\Admin\Downloads\AI.mp4"}
    )]

    await cl.Message(
        content=f"Bạn vừa gửi: {message.content}",
        actions=actions,
        # elements=files,
    ).send()


@cl.action_callback("yes")
async def on_yes(action: cl.Action):
    await cl.Message(
        content=f"Bạn chọn: {action.payload['value']}"
    ).send()


@cl.action_callback("no")
async def on_no(action: cl.Action):
    await cl.Message(
        content=f"Bạn chọn: {action.payload['value']}"
    ).send()

@cl.action_callback("view_file")
async def view_file(action: cl.Action):

    path = Path(action.payload["path"])

    if Path(path).exists():
        os.startfile(path)
    else:
        await cl.Message(
            content=f"Không tìm thấy file: {path}"
        ).send()

