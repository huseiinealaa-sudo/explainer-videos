"""mc5_hart: ONE still frame that fixes the look of the MC5 screen (shown to the owner before any render).

    EXPLAINER_SCRIPT=projects/mc5_hart/mc5_screen_frame.py manim -s -qh --media_dir tmp/mc5_frame \
        projects/mc5_hart/mc5_screen_frame.py ScreenFrame
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from explainer import *
from mc5_visuals import MC5
import mc5_hart_data as D


class ScreenFrame(Scene):
    def construct(self):
        mc = MC5(mode="CALIBRATION")
        menu = [(1, "Trim Lower\n0% Range"), (2, "Trim Upper\n100% Range"), (3, "Check Any Value"),
                (4, "Select Output"), (5, "Device Information"), (6, "Device Settings"),
                (7, "End HART\nAdjustment")]
        page = mc.calibration_page(
            {"title": "Input  Current [Keyed]", "value": D.fmt(4.0, 4), "unit": "mA"},
            {"title": "Output Current [E: Meas]", "value": D.fmt(D.I_STORY_ZERO, 4), "unit": "mA"},
            menu=menu, selected=1, field=("Enter measured 0%", D.fmt(D.I_STORY_ZERO, 4)),
            err=D.fmt(D.ERR_STORY_ZERO, 2), points=[(0, D.ERR_STORY_ZERO)],
            softkeys=("End\nTrim", "", "Fetch", "Send"))
        mc.page = page
        mc.add(page)
        mc.soft = VGroup(*mc._soft_labels(page.softkeys))
        mc.add(mc.soft)
        mc.keys["D"][0].set_fill(ACCENT_1, 1)
        mc.keys["D"][1].set_color(BG)
        mc.move_to(LEFT * 2.3 + DOWN * 0.1)
        # a side note to show how callouts sit beside the screen
        note = VGroup(label("Input = what MC5 commands", FS_NOTE, INK),
                      label("Output = what MC5 measures", FS_NOTE, INK),
                      label("Error graph, % of span", FS_NOTE, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        note.move_to(RIGHT * 3.9)
        note.scale_to_fit_width(4.6).align_to(RIGHT * 6.9, RIGHT)
        self.add(mc, note)
