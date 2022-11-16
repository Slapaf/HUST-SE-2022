from urllib.request import quote, unquote
import base64


def encryption(message: str) -> str:
    """加密函数，采用 base64

    Args:
        message: 待加密的信息

    Returns:
        加密后的信息
    """
    return base64.b64encode(quote(message).encode()).decode()


def decryption(message: str) -> str:
    """解密函数，采用 base64

    Args:
        message: 待解密的信息

    Returns:
        解密后的信息
    """
    return unquote(base64.b64decode(message).decode())
