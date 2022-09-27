
import unittest
import helpers.renderers as renderers
import pupil

class TestLexer(unittest.TestCase):
 def test_dismemberment(self):
  self.assertEqual(
    pupil.cut_you_up('[(ffffff,310000) this will be [(200,30,30) ooh!] this will be [(200,30,30) aah!] this will be [(200,30,30) absolutely [(200,0,200) whee!]] this will be nice]'),
    (['ffffff', '310000'], ['this will be ', '[(200,30,30) ooh!]', ' this will be ', '[(200,30,30) aah!]', ' this will be ', '[(200,30,30) absolutely [(200,0,200) whee!]]', ' this will be nice']))


class TestCompile(unittest.TestCase):
 def test_discriminate_nested(self):
  brains, members = pupil.cut_you_up('[(ffffff,310000) this will be [(200,30,30) ooh!] this will be [(200,30,30) aah!] this will be [(200,30,30) absolutely [(200,0,200) whee!]]]')
  self.assertEqual([pupil.is_styled_nest(i) for i in members], [False, True, False, True, False, True])

 def test_ansi_compilation(self):
  rendfunctions = [renderers.render_fore_color, renderers.render_back_color, renderers.render_bold, renderers.render_italic]
  values = [
        """[(ffffff,000000,1) this is no orthodox [(,555555) beheading] [(,,0) I'm cuting you [(ff0000) up] cutting you up] cutting you up will be so refreshing to me]""",
        '[(ff0000,440000,1) bold red on dark red]',
        '[(00ff00,440000,1) Im green over dark red and bold! [(0000ff) but I feel all blue]]',
        '[(ff00ff,000000) [(,bbbb00) magenta over yellow] [(,00bbbb) magenta over cyan] [(,0000bb) magenta over blue] just magenta]',
        '[(ffffff,007700,0,0) white over green darkish [(,,1) Im just bold [(,,,1) Im bold and italic!] just bold again] Ive been restored to my previous glory]',
        ]

  results = [
        "\x1b[38;2;255;255;255m\x1b[48;2;0;0;0m\x1b[1mthis is no orthodox \x1b[48;2;85;85;85mbeheading\x1b[48;2;0;0;0m \x1b[22mI'm cuting you \x1b[38;2;255;0;0mup\x1b[38;2;255;255;255m cutting you up\x1b[1m cutting you up will be so refreshing to me",
        '\x1b[38;2;255;0;0m\x1b[48;2;68;0;0m\x1b[1mbold red on dark red',
        '\x1b[38;2;0;255;0m\x1b[48;2;68;0;0m\x1b[1mIm green over dark red and bold! \x1b[38;2;0;0;255mbut I feel all blue',
        '\x1b[38;2;255;0;255m\x1b[48;2;187;187;0mmagenta over yellow\x1b[48;2;0;0;0m \x1b[48;2;0;187;187mmagenta over cyan\x1b[48;2;0;0;0m \x1b[48;2;0;0;187mmagenta over blue\x1b[48;2;0;0;0m just magenta',
        '\x1b[38;2;255;255;255m\x1b[48;2;0;119;0m\x1b[22m\x1b[23mwhite over green darkish \x1b[1mIm just bold \x1b[3mIm bold and italic!\x1b[23m just bold again\x1b[22m Ive been restored to my previous glory'
        ]
  self.assertEqual([pupil.StackRenderer(i).compa(rendfunctions) for i in values], results)

if __name__ == "__main__":
 unittest.main()

