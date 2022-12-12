from sty import fg, bg, ef, rs
from sty import Style, RgbFg, RgbBg


def format_font(message, font_color_type, color):
    """
    Used to format the font displayed by colour
    :param message: The message to be formatted
    :param font_color_type: Used to format the font (accepts 'fg') or background (accepts 'bg')
    :param color: colour of the font
    :return: the colour-formatted font
    """
    cl_msg = ''
    if font_color_type == 'ef':
        cl_msg = ef.italic + message + rs.italic
    elif color == 'orange':
        fg.orange = Style(RgbFg(255, 150, 50))
        bg.orange = Style(RgbBg(255, 150, 50))
        if font_color_type == 'fg':
            cl_msg = fg.orange + message + fg.rs
        elif font_color_type == 'bg':
            cl_msg = bg.orange + message + bg.rs
    elif color == 'red':
        if font_color_type == 'fg':
            cl_msg = fg.red + message + fg.rs
        elif font_color_type == 'bg':
            cl_msg = bg.red + message + bg.rs
    elif color == 'blue':
        if font_color_type == 'fg':
            cl_msg = fg.blue + message + fg.rs
        elif font_color_type == 'bg':
            cl_msg = bg.blue + message + bg.rs
    elif color == 'green':
        if font_color_type == 'fg':
            cl_msg = fg.green + message + fg.rs
        elif font_color_type == 'bg':
            cl_msg = bg.green + message + bg.rs
    return cl_msg


