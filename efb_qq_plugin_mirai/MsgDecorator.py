import logging
from typing import Mapping, Tuple, Union, IO

import magic
from ehforwarderbot import MsgType, Chat
from ehforwarderbot.chat import ChatMember, SelfChatMember
from ehforwarderbot.message import Substitutions, Message


def efb_text_simple_wrapper(text: str, ats: Union[Mapping[Tuple[int, int], Union[Chat, ChatMember, SelfChatMember]], None] = None) -> Message:
    """
    A simple EFB message wrapper for plain text. Emojis are presented as is (plain text).

    :param text: The content of the message
    :param ats: The substitutions of at messages, must follow the Substitution format when not None
                [[begin_index, end_index], {Chat or ChatMember}]
    :return: EFB Message
    """
    efb_msg = Message(
        type=MsgType.Text,
        text=text
    )
    if ats:
        efb_msg.substitutions = Substitutions(ats)
    return efb_msg


def efb_unsupported_wrapper(text: str) -> Message:
    """
    A simple EFB message wrapper for unsupported message

    :param text: The content of the message
    :return: EFB Message
    """
    efb_msg = Message(
        type=MsgType.Unsupported,
        text=text
    )
    return efb_msg


def efb_image_wrapper(file: IO, filename: str = None, text: str = None) -> Message:
    """
    A EFB message wrapper for images.

    :param file: The file handle
    :param filename: The actual filename
    :param text: The attached text
    :return: EFB Message
    """
    efb_msg = Message()
    efb_msg.file = file
    mime = magic.from_file(file.name, mime=True)
    if isinstance(mime, bytes):
        mime = mime.decode()

    if "gif" in mime:
        efb_msg.type = MsgType.Animation
    else:
        efb_msg.type = MsgType.Image

    if filename:
        efb_msg.filename = filename
    else:
        efb_msg.filename = file.name
        efb_msg.filename += '.' + str(mime).split('/')[1]  # Add extension suffix
    if text:
        efb_msg.text = text
    efb_msg.path = efb_msg.file.name
    efb_msg.mime = mime
    return efb_msg


def efb_voice_wrapper(file: IO, filename: str = None, text: str = None) -> Message:
    """
    A EFB message wrapper for voices.

    :param file: The file handle
    :param filename: The actual filename
    :param text: The attached text
    :return: EFB Message
    """
    efb_msg = Message()
    efb_msg.type = MsgType.Audio
    efb_msg.file = file
    mime = magic.from_file(efb_msg.file.name, mime=True)
    if isinstance(mime, bytes):
        mime = mime.decode()
    if filename:
        efb_msg.filename = filename
    else:
        efb_msg.filename = file.name
        efb_msg.filename += '.' + str(mime).split('/')[1]  # Add extension suffix
    efb_msg.path = efb_msg.file.name
    efb_msg.mime = mime
    if text:
        efb_msg.text = text
    return efb_msg
