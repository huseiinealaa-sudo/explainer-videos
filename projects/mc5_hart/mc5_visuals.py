"""mc5_hart: the MC5 screen drawn as one reusable component (no logo, no brand name).

    from mc5_visuals import MC5

    mc = MC5()                                       # the screen: status bar, soft keys, A B C D keys
    page = mc.windows_page(w1, w2, menu=[...])       # two windows + numbered side menu
    page = mc.calibration_page(inp, out, menu=[...]) # Input / Output / Error graph (+ side menu)
    page = mc.form_page("DEVICE SETTINGS", rows)     # a settings page, rows of (label, value)
    page = mc.list_page("HART", lines)               # a plain list (device search)
    mc.show(self, page)                              # the page appears (the previous one fades)
    mc.press(self, "D")                              # a key is pressed (A B C D)
    mc.press_digit(self, 6, page.menu)               # a numeric key chip, the cursor jumps to item 6
    page.menu.select(self, 3)                        # the cursor moves to item 3
    mc.set_text(self, page.parts["urv"], "30.00")    # a value changes on the screen

One look for every episode: a monospaced LCD-style screen (PANEL_FILL) on a plain body. The
selected menu row is inverted (INK fill, BG text); editable values are ACCENT_1; a menu item the
video does not name is drawn as a faint bar, never as invented text. The pages show only the
values the caller passes (from `mc5_hart_data`); the screen invents none.
"""
from manim import *

from explainer import *   # noqa: F401,F403  (theme colours, mono, label, fit, ...)

SCREEN_W, SCREEN_H = 7.8, 4.7
BAR_H, SOFT_H = 0.36, 0.56
FS = 15                    # screen text
FS_SMALL = 14              # port lines, axis ticks (MIN_FONT_SIZE)
FS_BIG = 30                # the big reading of a window
PAD = 0.14


def _txt(s, size=FS, color=INK, weight=None):
    kw = {} if weight is None else {"weight": weight}
    return mono(s, size, color, **kw)


class Menu(VGroup):
    """A numbered side menu. Items are (number, text) or (number, None) for an item the video does
    not name (a faint bar). `select(scene, n)` moves the inverted cursor to the row numbered n.
    Geometry is kept relative to `ref`, an invisible rectangle, so the menu can be moved freely."""

    def __init__(self, items, width, selected=None, size=FS):
        super().__init__()
        self.items, self.width_ = items, width
        heights, bodies, nums = [], [], []
        for n, text in items:
            if text is None:
                body = Line(ORIGIN, RIGHT * width * 0.4, color=LIGHT_INK, stroke_width=3)
                num, h = _txt(str(n), size, GREY_INK), 0.34
            else:
                lines = text.split("\n")
                body = _txt("\n".join([lines[0]] + ["  " + t for t in lines[1:]]), size)
                num, h = _txt(str(n), size), 0.17 + 0.24 * len(lines)
            heights.append(h)
            bodies.append(body)
            nums.append(num)
        self.row_h = heights
        total = sum(heights)
        self.ref = Rectangle(width=width, height=total, stroke_width=0, fill_opacity=0)
        self.cursor = Rectangle(width=width, height=0.3, stroke_width=0).set_fill(INK, 1)
        self.numbers, self.texts, self.row_y = nums, bodies, []
        y = total / 2                                   # relative to the ref's centre
        for h, num, body, (n, t) in zip(heights, nums, bodies, items):
            y -= h / 2
            self.row_y.append(y)
            num.move_to([-width / 2 + 0.1 + num.width / 2, y, 0])
            left = -width / 2 + 0.1 + 0.3
            body.move_to([left + body.width / 2, y, 0])
            y -= h / 2
        self.add(self.ref, self.cursor, *nums, *bodies)
        self.selected = None
        if selected is not None:
            self._style(selected)
            self._cursor_to(selected)
        else:
            self.cursor.set_opacity(0)

    # -- helpers --
    def k(self, n):
        return [i for i, (num, _) in enumerate(self.items) if num == n][0]

    def _target(self, k):
        return self.ref.get_center() + np.array([0, self.row_y[k], 0])

    def _style(self, n):
        k = self.k(n)
        for j, (_, t) in enumerate(self.items):
            sel = j == k and t is not None
            col = BG if sel else (INK if t is not None else GREY_INK)
            if t is not None:
                self.texts[j].set_color(col)
            self.numbers[j].set_color(col)
        self.selected = n

    def _cursor_to(self, n):
        k = self.k(n)
        self.cursor.stretch_to_fit_height(self.row_h[k] - 0.04)
        self.cursor.move_to(self._target(k))

    def select(self, scene, n, run_time=0.45):
        """Animate the cursor to the row numbered n."""
        k = self.k(n)
        if self.cursor.fill_opacity == 0:          # first selection: appear in place
            self.cursor.stretch_to_fit_height(self.row_h[k] - 0.04).move_to(self._target(k))
        anims = [self.cursor.animate.set_opacity(1).stretch_to_fit_height(self.row_h[k] - 0.04)
                 .move_to(self._target(k))]
        for j, (_, t) in enumerate(self.items):
            sel = j == k and t is not None
            col = BG if sel else (INK if t is not None else GREY_INK)
            if t is not None:
                anims.append(self.texts[j].animate.set_color(col))
            anims.append(self.numbers[j].animate.set_color(col))
        self.selected = n
        scene.play(*anims, run_time=run_time)

    def row(self, n):
        return self.texts[self.k(n)]


class Page(VGroup):
    """One screen page. `parts` names its changeable mobjects, `menu` is its Menu (or None),
    `softkeys` the four soft key labels (A B C D)."""

    def __init__(self, *mobs, softkeys=("", "", "", ""), parts=None, menu=None):
        super().__init__(*mobs)
        self.softkeys, self.parts, self.menu = list(softkeys), parts or {}, menu


class MC5(VGroup):
    """The calibrator screen with its A B C D keys. Parts: body, screen, bar, soft (the soft key
    labels), keys {"A": ..}. `self.page` is the page now shown."""

    def __init__(self, mode="BASIC"):
        super().__init__()
        W, H = SCREEN_W, SCREEN_H
        self.screen = Rectangle(width=W, height=H, color=INK, stroke_width=3).set_fill(PANEL_FILL, 1)
        self.body = RoundedRectangle(width=W + 0.4, height=H + 0.2 + 0.78 + 0.16, corner_radius=0.2,
                                     color=GREY_INK, stroke_width=3).set_fill(BG, 1)
        self.screen.move_to(ORIGIN)
        self.body.move_to(self.screen.get_center() + DOWN * ((0.78 + 0.16 - 0.2) / 2))
        # status bar
        self.bar_line = Line(self.screen.get_corner(UL) + DOWN * BAR_H,
                             self.screen.get_corner(UR) + DOWN * BAR_H, color=INK, stroke_width=2)
        self.mode_text = _txt(mode, FS, INK, "BOLD").next_to(self.screen.get_corner(UL) + DOWN * BAR_H / 2,
                                                              RIGHT, buff=0.0).shift(RIGHT * PAD)
        self.mode_text.set_y(self.screen.get_top()[1] - BAR_H / 2)
        tag = _txt("Illustrative", FS, GREY_INK)
        tag.move_to([self.screen.get_center()[0], self.screen.get_top()[1] - BAR_H / 2, 0])
        clock = _txt("12:00", FS, INK)
        batt = VGroup(Rectangle(width=0.42, height=0.2, color=INK, stroke_width=2),
                      Rectangle(width=0.3, height=0.1, stroke_width=0).set_fill(INK, 1))
        batt[1].move_to(batt[0])
        batt_x = self.screen.get_right()[0] - PAD - 0.21
        batt.move_to([batt_x, self.screen.get_top()[1] - BAR_H / 2, 0])
        clock.next_to(batt, LEFT, buff=0.15)
        self.bar = VGroup(self.bar_line, self.mode_text, tag, clock, batt)
        # soft key row
        top = self.screen.get_bottom()[1] + SOFT_H
        self.soft_line = Line([self.screen.get_left()[0], top, 0], [self.screen.get_right()[0], top, 0],
                              color=INK, stroke_width=2)
        self.cell_w = W / 4
        dividers = [Line([self.screen.get_left()[0] + self.cell_w * i, top, 0],
                         [self.screen.get_left()[0] + self.cell_w * i, self.screen.get_bottom()[1], 0],
                         color=GREY_INK, stroke_width=2) for i in (1, 2, 3)]
        self.soft_y = (top + self.screen.get_bottom()[1]) / 2
        self.soft_cells = [self.screen.get_left()[0] + self.cell_w * (i + 0.5) for i in range(4)]
        self.soft = VGroup(*[VGroup() for _ in range(4)])
        self.soft_frame = VGroup(self.soft_line, *dividers)
        # keys A B C D
        key_y = self.screen.get_bottom()[1] - 0.16 - 0.3
        self.keys = {}
        for i, ch in enumerate("ABCD"):
            r = RoundedRectangle(width=1.35, height=0.46, corner_radius=0.12, color=INK,
                                 stroke_width=3).set_fill(PANEL_FILL, 1)
            t = _txt(ch, 22, INK, "BOLD")
            g = VGroup(r, t)
            g.move_to([self.soft_cells[i], key_y, 0])
            t.move_to(r)
            self.keys[ch] = g
        self.add(self.body, self.screen, self.bar, self.soft_frame, self.soft, *self.keys.values())
        self.page = None
        self.top_y = top

    # ------------- geometry -------------
    def area(self):
        """(left, right, top, bottom) of the page area, inside the status bar and the soft keys."""
        return (self.screen.get_left()[0] + PAD, self.screen.get_right()[0] - PAD,
                self.screen.get_top()[1] - BAR_H - 0.1, self.screen.get_bottom()[1] + SOFT_H + 0.1)

    def _origin_shift(self):
        return self.screen.get_center()

    # ------------- soft keys -------------
    def _soft_labels(self, labels):
        out = []
        for i, s in enumerate(labels):
            if not s:
                out.append(VGroup())
                continue
            t = _txt(s, FS, INK).move_to([self.screen.get_left()[0] + self.cell_w * (i + 0.5),
                                          self.screen.get_bottom()[1] + SOFT_H / 2, 0])
            if t.width > self.cell_w - 0.2:
                t.scale_to_fit_width(self.cell_w - 0.2)
            out.append(t)
        return out

    # ------------- pages -------------
    def windows_page(self, w1, w2, menu=None, selected=None, softkeys=("Calibration\nMode", "", "", "MENU"),
                     menu_w=3.05):
        """Two measurement windows and, optionally, a numbered menu on the right (opened here or later
        with `open_menu`). w = {"title": "1 Pressure", "port": "P1: REF", "value": "0.012", "unit": "kgf/cm²"}."""
        L, R, T, B = self.area()
        lw = R - L
        mobs, parts = [], {}
        h = (T - B) / 2
        shift = []
        for idx, w in enumerate((w1, w2)):
            top = T - idx * h
            title = _txt(w["title"], FS).move_to([L + 0.05, top - 0.22, 0], aligned_edge=LEFT)
            port = _txt(w["port"], FS_SMALL, GREY_INK).next_to(title, DOWN, buff=0.08, aligned_edge=LEFT)
            value = _txt(w["value"], FS_BIG, INK, "BOLD")
            unit = _txt(w["unit"], FS, INK)
            value.move_to([L + lw - 0.05 - value.width / 2, top - h + 0.72, 0])
            unit.next_to(value, DOWN, buff=0.1, aligned_edge=RIGHT)
            parts.update({f"title{idx + 1}": title, f"port{idx + 1}": port,
                          f"value{idx + 1}": value, f"unit{idx + 1}": unit})
            mobs += [title, port, value, unit]
            shift += [value, unit]
            if idx == 0:
                hline = Line([L, T - h, 0], [L + lw, T - h, 0], color=GREY_INK, stroke_width=2)
                parts["hline"] = hline
                mobs.append(hline)
        parts["_shift"] = shift
        page = Page(*mobs, softkeys=softkeys, parts=parts, menu=None)
        if menu:
            dx = menu_w + 0.12
            for m_ in shift:
                m_.shift(LEFT * dx)
            hline = parts["hline"]
            hline.put_start_and_end_on(hline.get_start(), hline.get_end() + LEFT * dx)
            sep, m = self._menu_parts(menu, selected, menu_w)
            page.add(sep, m)
            page.menu, page.parts["_sep"] = m, sep
        return page

    def _menu_parts(self, items, selected, menu_w):
        L, R, T, B = self.area()
        sep = Line([R - menu_w - 0.06, T, 0], [R - menu_w - 0.06, B, 0], color=GREY_INK, stroke_width=2)
        m = Menu(items, menu_w - 0.06, selected)
        m.move_to([R - (menu_w - 0.06) / 2, T - m.ref.height / 2, 0])
        if selected is not None:
            m._cursor_to(selected)
        return sep, m

    def open_menu(self, scene, page, items, selected=None, menu_w=3.05, run_time=0.7):
        """The windows slide left and a numbered menu opens on the right."""
        dx = menu_w + 0.12
        hline = page.parts["hline"]
        anims = [m_.animate.shift(LEFT * dx) for m_ in page.parts["_shift"]]
        anims.append(hline.animate.put_start_and_end_on(hline.get_start(), hline.get_end() + LEFT * dx))
        sep, m = self._menu_parts(items, selected, menu_w)
        page.add(sep, m)
        page.menu, page.parts["_sep"] = m, sep
        scene.play(*anims, FadeIn(sep), FadeIn(m), run_time=run_time)
        return m

    def close_menu(self, scene, page, menu_w=3.05, run_time=0.6):
        dx = menu_w + 0.12
        hline = page.parts["hline"]
        anims = [m_.animate.shift(RIGHT * dx) for m_ in page.parts["_shift"]]
        anims.append(hline.animate.put_start_and_end_on(hline.get_start(), hline.get_end() + RIGHT * dx))
        scene.play(*anims, FadeOut(page.menu), FadeOut(page.parts["_sep"]), run_time=run_time)
        page.remove(page.menu, page.parts["_sep"])
        page.menu = None

    def set_softkeys(self, scene, labels, run_time=0.3):
        new = VGroup(*self._soft_labels(labels))
        scene.play(FadeOut(self.soft), FadeIn(new), run_time=run_time)
        self.remove(self.soft)
        self.soft = new
        self.add(new)

    def calibration_page(self, inp, out, menu=None, selected=None, field=None, err=None,
                         softkeys=("", "", "", ""), points=None, menu_w=3.05):
        """Input window, Output window, an optional field row and the Error graph; menu on the right.
        inp / out = {"title": "Input  Pressure [P1: REF]", "value": "0.000", "unit": "kgf/cm²"}.
        field = (label, value): the trim field under the Output window. err = "−0.40" (% of span).
        points = [(x_pct, err_pct), ...] drawn in the error graph (x 0–100, error ±1)."""
        L, R, T, B = self.area()
        mw = menu_w if menu else 0
        lw = (R - L) - mw - (0.12 if menu else 0)
        mobs, parts = [], {}
        y = T
        for key, w in (("in", inp), ("out", out)):
            title = _txt(w["title"], FS).move_to([L + 0.05, y - 0.2, 0], aligned_edge=LEFT)
            value = _txt(w["value"], 26, INK, "BOLD")
            unit = _txt(w["unit"], FS, INK)
            value.move_to([L + lw - 0.05 - value.width / 2 - unit.width - 0.12, y - 0.55, 0])
            unit.next_to(value, RIGHT, buff=0.12, aligned_edge=DOWN)
            parts.update({f"{key}_title": title, f"{key}_value": value, f"{key}_unit": unit})
            mobs += [title, value, unit]
            y -= 0.82
        if field:
            lab = _txt(field[0], FS).move_to([L + 0.05, y - 0.2, 0], aligned_edge=LEFT)
            val = _txt(field[1], FS, ACCENT_1, "BOLD")
            val.move_to([L + lw - 0.2 - val.width / 2, y - 0.2, 0])
            box = SurroundingRectangle(val, buff=0.07, color=ACCENT_1, stroke_width=2)
            parts.update({"field_label": lab, "field_value": val, "field_box": box})
            mobs += [lab, val, box]
        y = T - 0.82 * 2 - (0.46 if field else 0.04)
        # error graph: title, readout, plot
        gt = _txt("Error", FS_SMALL, GREY_INK).move_to([L + 0.05, y - 0.12, 0], aligned_edge=LEFT)
        readout = _txt((err or "") + (" % of span" if err else ""), FS, INK)
        readout.move_to([L + lw - 0.05 - readout.width / 2, y - 0.12, 0])
        parts.update({"err_readout": readout})
        gh = max(0.5, y - 0.3 - B - 0.28)
        gx0, gx1 = L + 0.55, L + lw - 0.1
        gy1 = y - 0.34
        gy0 = gy1 - gh
        plot = Rectangle(width=gx1 - gx0, height=gh, color=GREY_INK, stroke_width=2)
        plot.move_to([(gx0 + gx1) / 2, (gy0 + gy1) / 2, 0])
        zero = DashedLine(plot.get_left(), plot.get_right(), color=GREY_INK, stroke_width=2, dash_length=0.1)
        ylab = VGroup(_txt("+", FS_SMALL, INK).move_to([gx0 - 0.2, gy1 - 0.1, 0]),
                      _txt("0", FS_SMALL, INK).move_to([gx0 - 0.2, (gy0 + gy1) / 2, 0]),
                      _txt("−", FS_SMALL, INK).move_to([gx0 - 0.2, gy0 + 0.1, 0]))
        xlab = VGroup(*[_txt(s, FS_SMALL, INK).move_to([gx0 + (gx1 - gx0) * f, gy0 - 0.17, 0])
                        for s, f in (("0%", 0.0), ("50%", 0.5), ("100%", 1.0))])
        xlab[0].shift(RIGHT * 0.12)
        xlab[2].shift(LEFT * 0.2)
        mobs += [gt, readout, plot, zero, ylab, xlab]
        parts.update({"plot": plot})
        if points:
            dots = VGroup(*[Dot([gx0 + (gx1 - gx0) * x / 100.0,
                                 (gy0 + gy1) / 2 + (gh / 2) * max(-1.0, min(1.0, e)), 0],
                                radius=0.06, color=ACCENT_2) for x, e in points])
            parts["dots"] = dots
            mobs.append(dots)
        m = None
        if menu:
            mobs.append(Line([L + lw + 0.06, T, 0], [L + lw + 0.06, B, 0], color=GREY_INK, stroke_width=2))
            m = Menu(menu, mw - 0.06, selected)
            m.move_to([L + lw + 0.12 + (mw - 0.06) / 2, T - m.ref.height / 2, 0])
            if selected is not None:
                m._cursor_to(selected)
            mobs.append(m)
        return Page(*mobs, softkeys=softkeys, parts=parts, menu=m)

    def form_page(self, title, rows, editable=(), selected=None, softkeys=("Close", "", "Edit", ""),
                  row_h=0.32, label_w=3.2):
        """A settings page. rows = [(key, label, value)] or ("#", "Section") for a section header.
        Editable rows (by key) show their value in ACCENT_1; `selected` is a key (inverted row)."""
        L, R, T, B = self.area()
        ttl = _txt(title, FS, INK, "BOLD").move_to([(L + R) / 2, T - 0.13, 0])
        rule = Line([L, T - 0.28, 0], [R, T - 0.28, 0], color=GREY_INK, stroke_width=2)
        mobs, parts = [ttl, rule], {"title": ttl}
        cursor = Rectangle(width=R - L, height=row_h - 0.01, stroke_width=0).set_fill(INK, 1)
        mobs.insert(0, cursor)
        y = T - 0.3
        ycur = None
        keys_y = {}
        for r in rows:
            y -= row_h / 2
            if r[0] == "#":
                sec = _txt(r[1], FS_SMALL, GREY_INK, "BOLD").move_to([L + 0.05, y, 0], aligned_edge=LEFT)
                mobs.append(sec)
            else:
                key, lab, val = r
                lt = _txt(lab, FS_SMALL).move_to([L + 0.05, y, 0], aligned_edge=LEFT)
                vt = _txt(val, FS_SMALL, ACCENT_1 if key in editable else INK)
                vt.move_to([R - 0.05 - vt.width / 2, y, 0])
                parts[key], parts[key + "_label"] = vt, lt
                mobs += [lt, vt]
                keys_y[key] = y
            y -= row_h / 2
        assert y >= B - 0.02, f"form page {title!r} has too many rows ({len(rows)}): split it in two pages"
        first = selected or next(iter(keys_y), None)
        if first:
            cursor.move_to([(L + R) / 2, keys_y[first], 0])
        if selected:
            parts[selected].set_color(BG)
            parts[selected + "_label"].set_color(BG)
        else:
            cursor.set_opacity(0)
        parts["cursor"], parts["_rows_y"], parts["_edit"] = cursor, keys_y, set(editable)
        return Page(*mobs, softkeys=softkeys, parts=parts)

    def move_form_cursor(self, scene, page, key, run_time=0.4):
        """Move the inverted cursor of a form page to row `key`."""
        p = page.parts
        cur = p["cursor"]
        anims = []
        for k in p["_rows_y"]:
            col = INK if k not in p["_edit"] else ACCENT_1
            if (cur.fill_opacity > 0) and abs(p[k].get_y() - cur.get_y()) < 0.01:
                anims += [p[k].animate.set_color(col), p[k + "_label"].animate.set_color(INK)]
        target = cur.get_center() * [1, 0, 0] + np.array([0, p[key].get_y(), 0])
        if cur.fill_opacity == 0:
            cur.move_to(target)
            anims.append(cur.animate.set_opacity(1))
        else:
            anims.append(cur.animate.move_to(target))
        anims += [p[key].animate.set_color(BG), p[key + "_label"].animate.set_color(BG)]
        scene.play(*anims, run_time=run_time)

    def list_page(self, title, lines, selected=None, softkeys=("Back", "", "Restart", "Select")):
        """A plain list (device search). lines = [text | (key, text)]; `selected` is a key."""
        L, R, T, B = self.area()
        ttl = _txt(title, FS, INK, "BOLD").move_to([(L + R) / 2, T - 0.14, 0])
        rule = Line([L, T - 0.3, 0], [R, T - 0.3, 0], color=GREY_INK, stroke_width=2)
        cursor = Rectangle(width=R - L, height=0.27, stroke_width=0).set_fill(INK, 1)
        mobs, parts = [cursor, ttl, rule], {"title": ttl, "cursor": cursor}
        y, keys_y = T - 0.3 - 0.08, {}
        for ln in lines:
            key, text = (ln if isinstance(ln, tuple) else (None, ln))
            y -= 0.14
            t = _txt(text, FS).move_to([L + 0.05, y, 0], aligned_edge=LEFT)
            mobs.append(t)
            if key is not None:
                parts[key] = t
                keys_y[key] = y
            y -= 0.14
        first = selected if selected is not None else next(iter(keys_y), None)
        if first is not None:
            cursor.move_to([(L + R) / 2, keys_y[first], 0])
        if selected is not None:
            parts[selected].set_color(BG)
        else:
            cursor.set_opacity(0)
        parts["_rows_y"] = keys_y
        return Page(*mobs, softkeys=softkeys, parts=parts)

    def popup(self, items, selected=None, anchor=None, width=3.2, title=None):
        """A small pop-up list laid over the page (add it with `mc.add_overlay`)."""
        rows = [(i + 1, t) for i, t in enumerate(items)]
        m = Menu(rows, width - 0.2, selected, size=FS)
        frame = Rectangle(width=width, height=m.ref.height + 0.2, color=INK, stroke_width=3).set_fill(BG, 1)
        m.move_to(frame.get_center())
        g = VGroup(frame, m)
        g.menu = m
        if anchor is not None:
            g.move_to(anchor)
        return g

    # ------------- animations -------------
    def show(self, scene, page, run_time=0.6, shift=ORIGIN):
        """Show `page` on the screen; the previous page and its soft keys fade out (`shift`: a slide)."""
        new_soft = VGroup(*self._soft_labels(page.softkeys))
        outs = []
        if self.page is not None:
            outs.append(FadeOut(self.page, shift=shift))
        outs.append(FadeOut(self.soft))
        scene.play(*outs, FadeIn(page, shift=shift), FadeIn(new_soft), run_time=run_time)
        self.remove(self.soft)
        if self.page is not None:
            self.remove(self.page)
        self.soft, self.page = new_soft, page
        self.add(page, new_soft)
        return page

    def set_text(self, scene, mob, new, run_time=0.5, color=None, align=None):
        """Change a text on the screen (keeps the edge named in `align`, default the right edge for
        numbers, the left edge otherwise) and returns the new mobject."""
        edge = align if align is not None else (RIGHT if new.replace("−", "-").replace(".", "").lstrip("-+").isdigit() else LEFT)
        new_t = _txt(new, mob.font_size, mob.color if color is None else color,
                     "BOLD" if getattr(mob, "weight", None) == "BOLD" else None)
        new_t.move_to(mob.get_center())
        new_t.align_to(mob, edge)
        scene.play(Transform(mob, new_t), run_time=run_time)
        return mob

    def press(self, scene, ch, run_time=0.4):
        """Press the key A B C D: it dips and fills, its soft key label inverts for a moment."""
        key = self.keys[ch]
        i = "ABCD".index(ch)
        rect = key[0]
        scene.play(key.animate.shift(DOWN * 0.07), rect.animate.set_fill(ACCENT_1, 1),
                   key[1].animate.set_color(BG), run_time=run_time * 0.45)
        scene.play(key.animate.shift(UP * 0.07), rect.animate.set_fill(PANEL_FILL, 1),
                   key[1].animate.set_color(INK), run_time=run_time * 0.55)

    def key_chip(self, text):
        """A keypad chip (a number or a word such as "Enter") drawn under the screen, right of the keys."""
        w = 0.55 if len(str(text)) == 1 else 1.25
        r = RoundedRectangle(width=w, height=0.55, corner_radius=0.12, color=INK,
                             stroke_width=3).set_fill(PANEL_FILL, 1)
        t = _txt(str(text), 22 if len(str(text)) == 1 else FS, INK, "BOLD").move_to(r)
        g = VGroup(r, t)
        g.move_to([self.body.get_right()[0] + 0.45 + w / 2, self.keys["D"].get_y(), 0])
        return g

    def press_digit(self, scene, n, menu=None, run_time=0.7):
        """A numeric key chip lights up beside the keys; if `menu` is given, its cursor jumps to n."""
        self.press_chip(scene, n, then=(lambda: menu.select(scene, n, run_time=run_time * 0.6)) if menu else None)

    def press_chip(self, scene, text, then=None):
        chip = self.key_chip(text)
        scene.play(FadeIn(chip, scale=0.8), run_time=0.2)
        scene.play(chip[0].animate.set_fill(ACCENT_1, 1), chip[1].animate.set_color(BG), run_time=0.15)
        if then is not None:
            then()
        scene.play(FadeOut(chip), run_time=0.2)

    def set_mode(self, scene, text, run_time=0.3):
        """The status bar's mode text changes (BASIC → EDIT …)."""
        new = _txt(text, FS, INK, "BOLD")
        new.move_to(self.mode_text.get_left() + RIGHT * new.width / 2)
        scene.play(FadeOut(self.mode_text), FadeIn(new), run_time=run_time)
        self.bar.remove(self.mode_text)
        self.bar.add(new)
        self.mode_text = new

    def swap_many(self, scene, page, changes, run_time=0.5):
        """Texts of different length change: cross-fade (no morphing). changes = [(key, new_text, edge)];
        page.parts[key] is replaced by the new text."""
        outs, ins = [], []
        for key, new, edge in changes:
            mob = page.parts[key]
            new_t = _txt(new, mob.font_size, mob.color, "BOLD" if getattr(mob, "weight", None) == "BOLD" else None)
            new_t.move_to(mob.get_center()).align_to(mob, edge)
            outs.append(FadeOut(mob))
            ins.append(FadeIn(new_t))
            page.remove(mob)
            page.add(new_t)
            page.parts[key] = new_t
            if "_shift" in page.parts and mob in page.parts["_shift"]:
                page.parts["_shift"][page.parts["_shift"].index(mob)] = new_t
        scene.play(*outs, *ins, run_time=run_time)

    def set_many(self, scene, changes, run_time=0.6):
        """Several texts change together. changes = [(mob, new_text, align_edge)]; the edge stays put."""
        anims = []
        for mob, new, edge in changes:
            new_t = _txt(new, mob.font_size, mob.color, "BOLD" if getattr(mob, "weight", None) == "BOLD" else None)
            new_t.move_to(mob.get_center()).align_to(mob, edge)
            anims.append(Transform(mob, new_t))
        scene.play(*anims, run_time=run_time)


# ---------------- the one-frame proof used to approve the look ----------------
if __name__ == "__main__":
    pass


# ---------------- drawing helpers shared by the episodes ----------------
def ma_gauge(title, width=4.2, color=ACCENT_1, lo=4.0, hi=20.0, ticks=(4, 12, 20)):
    """A horizontal 4–20 mA bar with ticks and a marker (a triangle above the bar).
    `.x_of(v)` is the x of a value, `.marker` the marker, `.readout` the text; `.to(scene, v, text)`."""
    bar = Line(LEFT * width / 2, RIGHT * width / 2, color=INK, stroke_width=4)
    tk = VGroup()
    for v in ticks:
        x = -width / 2 + width * (v - lo) / (hi - lo)
        tk.add(Line([x, -0.09, 0], [x, 0.09, 0], color=INK, stroke_width=3))
        tk.add(_txt(f"{v:g}", FS_SMALL, INK).move_to([x, -0.3, 0]))
    ttl = _txt(title, FS, INK, "BOLD").next_to(bar, UP, buff=0.75)
    marker = Triangle(color=color, stroke_width=0).set_fill(color, 1).scale(0.13).rotate(PI)
    marker.move_to([-width / 2, 0.2, 0])
    readout = _txt("fixed near 4 mA", FS, color, "BOLD").next_to(bar, DOWN, buff=0.6)
    readout.set_opacity(0)
    g = VGroup(ttl, bar, tk, marker, readout)
    g.bar, g.marker, g.ttl, g.width_, g.lo, g.hi, g.readout, g.color_ = bar, marker, ttl, width, lo, hi, readout, color
    return g


def gauge_x(g, v):
    return g.bar.get_left()[0] + g.width_ * (v - g.lo) / (g.hi - g.lo)


def gauge_to(scene, g, v, text=None, run_time=1.0, rate=smooth):
    """Move the gauge marker to value v (and swap the readout text)."""
    x = gauge_x(g, v)
    new = _txt(text if text is not None else f"{v:.1f} mA", FS, g.color_, "BOLD")
    new.next_to(g.bar, DOWN, buff=0.6)
    old = g.readout
    g.remove(old)
    g.readout = new
    scene.play(g.marker.animate.move_to([x, g.marker.get_y(), 0]), FadeOut(old), FadeIn(new),
               run_time=run_time, rate_func=rate)


def panel(width, height, color=GREY_INK, fill=None, corner=0.15):
    r = RoundedRectangle(width=width, height=height, corner_radius=corner, color=color, stroke_width=3)
    if fill is not None:
        r.set_fill(fill, 1)
    return r


def note_line(text, icon_name=None, color=INK, size=FS_AXIS, width=4.4):
    """A short note: an optional Tabler icon and the text (wrapped in two lines when needed)."""
    parts = []
    if icon_name:
        parts.append(icon(icon_name, color, 0.42))
    t = label(text, size, color)
    if t.width > width - (0.6 if icon_name else 0):
        words = text.split()
        best = None
        for i in range(1, len(words)):
            a, b = " ".join(words[:i]), " ".join(words[i:])
            ta, tb = label(a, size, color), label(b, size, color)
            w = max(ta.width, tb.width)
            if best is None or w < best[0]:
                best = (w, VGroup(ta, tb).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
        t = best[1]
    parts.append(t)
    return VGroup(*parts).arrange(RIGHT, buff=0.18)
