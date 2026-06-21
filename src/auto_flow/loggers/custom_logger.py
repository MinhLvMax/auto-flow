from logging import Logger
import inspect
from src.core.constants.format_strings import MESSAGE_FORMAT
from src.core.util_funcs import normalize_message
import json


class CustomLogger(Logger):

    def debug(self, msg, *args, **kwargs):
        '''
        Format lại msg của mỗi dòng log để in nhiều thông tin hơn là 1 chuỗi msg
        :param msg:
        :param args:
        :param kwargs:
        :return:
        '''
        # frame_info = inspect.stack()[1] # Lấy đối tượng frame vừa gọi tới hàm này
        # if hasattr(msg, "model_dump"): # Kiểm tra để phòng msg là đối tượng Pydantic thì không thể chạy json.dumps bên dưới được
        #     msg = msg.model_dump()
        #
        # msg = json.dumps(msg, indent=2, ensure_ascii=False)
        # filename = frame_info.filename
        # lineno = frame_info.lineno
        # function = frame_info.function
        # code_context = frame_info.code_context
        # msg = MESSAGE_FORMAT.format(filename, lineno, function, code_context, msg)
        msg = normalize_message(msg)
        super().debug(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        msg = normalize_message(msg)
        super().error(msg, *args, **kwargs)

    def info(
            self,
            msg,
            *args,
            exc_info=None,
            stack_info=False,
            stacklevel=1,
            extra=None,
    ):

        msg = normalize_message(msg)

        super().info(msg, *args, exc_info=None,
                     stack_info=False,
                     stacklevel=1,
                     extra=None, )
