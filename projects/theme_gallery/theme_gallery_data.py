"""theme_gallery: every value shown on screen (all illustrative, no real plant or device).

DURATIONS are the silent segments in seconds, in the order of the video.
"""

DURATIONS = {
    "title": 6.0,
    "dark_a": 15.0, "dark_b": 15.0,
    "blueprint_a": 15.0, "blueprint_b": 15.0,
    "light_a": 15.0, "light_b": 15.0,
    "bg_base": 24.0,
    "bg_gradient": 9.0, "bg_grid": 9.0, "bg_particles": 9.0,
    "zoom": 11.0, "stagger": 9.0, "path": 10.0, "pulse": 10.0, "parallax": 11.0,
    "end": 8.0,
}

THEMES = ["dark", "blueprint", "light"]

# Structure sample (a): an equation, a worked calculation and a table.
EQUATION = ["MF", "=", "Vp", "÷", "Vm"]
CALC_FORMULA = ["MF", "=", "Vp", "÷", "Vm"]
CALC_VALUES = ["MF", "=", "50.0", "÷", "50.1"]
CALC_RESULT = "= 0.99800"
TABLE_HEADER = ["Run", "Vp", "Vm", "MF"]
TABLE_ROWS = [["1", "50.0", "50.1", "0.9980"],
              ["2", "50.0", "50.0", "1.0000"],
              ["3", "50.0", "49.9", "1.0020"],
              ["4", "50.0", "50.1", "0.9980"]]
TABLE_HIGHLIGHT = 1

# Structure sample (b): a flow, a loop drawing with symbols, a bar chart.
FLOW_STEPS = ["Collect", "Compare", "Decide", "Report"]
FLOW_ACTIVE = 2
LOOP_TAG = ("FT", "101")
BARS = {"labels": ["A", "B", "C", "D"], "values": [4.2, 5.1, 6.8, 4.9], "unit": " u",
        "limit": 6.0}

# Backgrounds: a custom colour, a custom gradient (any Manim colours) and a picture.
BG_SOLID = "#0f3a3a"
BG_GRADIENT = ("#0b1d3a", "#3b1d5e")
BG_IMAGE = "assets/plate.png"
BG_IMAGE_DIM = 0.55

# Motion tools.
ZOOM_FACTOR = 2.4
STAGGER_STEPS = [("Source", "file-text"), ("Storyboard", "list-check"), ("Narration", "bulb"),
                 ("Render", "cpu")]
PATH_POINTS = [(-5.4, -1.2), (-2.6, 1.6), (0.4, -1.4), (3.2, 1.4), (5.4, -0.6)]
PARALLAX_SHIFT = 1.5
PARALLAX_DEPTHS = (0.25, 0.6, 1.0)
