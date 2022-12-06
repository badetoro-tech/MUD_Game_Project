from sty import fg, bg, ef, rs
from sty import Style, RgbFg, RgbBg


def format_font(message, font_color_type, color):
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


# foo = fg.red + 'This is red text!' + fg.rs
# bar = bg.blue + 'This has a blue background!' + bg.rs
# baz = ef.italic + 'This is italic text' + rs.italic
#
# # Add custom colors:
# fg.orange = Style(RgbFg(255, 150, 50))
#
# buf = fg.orange + 'Yay, Im orange.' + fg.rs
#
# print(foo, bar, baz, buf, sep='\n')
#
# msg = 'This is a text of color'
# print(format_font(msg, 'fg', 'red'))
