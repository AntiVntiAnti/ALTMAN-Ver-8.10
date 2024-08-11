# from sexy_logger import logger
from logger_setup import logger
from typing import Any


def change_stack_page(mainStack: Any, index: int) -> None:
    """
    Change the current index of the alpha stack.

    Args:
    mainStack (Any): The alpha stack object.
    index (int): The new index to set.

    Returns:
    None

    Raises:
    Exception: If an error occurs while changing the stack page.
    """
    try:
        mainStack.setCurrentIndex(index)
        logger.info("Minder Stack Page Change")
    except Exception as e:
        logger.error(f"Minder Stack Page Change Error: {e}", exc_info=True)


