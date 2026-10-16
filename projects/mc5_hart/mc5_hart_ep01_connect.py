"""mc5_hart, episode 1: MC5 + HART: Connect & Configure.

Build (from the repo root):
    python projects/mc5_hart/mc5_hart_ep01_connect.py --preview   # 480p15 -> tmp/mc5_hart_ep01_connect/preview.mp4
    python projects/mc5_hart/mc5_hart_ep01_connect.py             # 1080p30 -> output/mc5_hart_ep01_connect.mp4
"""
from explainer import *
import numpy as np
import mc5_hart_data as D
from mc5_visuals import (MC5, ma_gauge, gauge_to, panel, note_line)

# Fully diacritized narration, approved by the owner on 2026-10-16 (with his six edits).
NARRATION = [
    # 1
    'فِي هٰذِهِ الحَلْقَةِ نَتَعَلَّمُ كَيْفَ يَتَّصِلُ جِهَازُ إِمْ سِي فايْف بِالمُرْسِلَةِ الذَّكِيَّةِ عَبْرَ هارْت، وَكَيْفَ نَقْرَأُ بَيَانَاتِهَا وَنُعَدِّلُ إِعْدَادَاتِهَا مِنْ شَاشَةِ الجِهَازِ نَفْسِهَا، قَبْلَ أَنْ نَصِلَ إِلَى المُعَايَرَةِ.',
    # 2
    'قَبْلَ أَيِّ اتِّصَالٍ، نُصَفِّرُ وَحْدَةَ ضَغْطِ المَرْجِعِ وَمَنْفَذُهَا مَفْتُوحٌ لِلْهَوَاءِ. نَضْغَطُ الزِّرَّ دِي لِفَتْحِ القَائِمَةِ، ثُمَّ الزِّرَّ إِيه لِإِعْدَادِ النَّافِذَةِ الأُولَى، ثُمَّ نَخْتَارُ البَنْدَ رَقْمَ سَبْعَةٍ: تَصْفِيرُ وَحْدَةِ الضَّغْطِ. فَتَعُودُ القِرَاءَةُ إِلَى الصِّفْرِ. وَنُعِيدُ التَّصْفِيرَ كُلَّمَا تَغَيَّرَ وَضْعُ الجِهَازِ أَوِ ارْتِفَاعُهُ.',
    # 3
    'لِلِاتِّصَالِ نَضْغَطُ الزِّرَّ دِي، ثُمَّ الزِّرَّ بِي لِإِعْدَادِ النَّافِذَةِ الثَّانِيَةِ عِنْدَ الحَاجَةِ، ثُمَّ نَخْتَارُ البَنْدَ رَقْمَ خَمْسَةٍ: هارْت. يَبْحَثُ إِمْ سِي فايْف عَنِ المُرْسِلَاتِ الَّتِي عَلَى الحَلْقَةِ وَيَعْرِضُهَا فِي قَائِمَةٍ، وَيَصِلُ حَتَّى سِتَّ عَشْرَةَ مُرْسِلَةً عَلَى الحَلْقَةِ نَفْسِهَا. وَنَخْتَارُ مُرْسِلَتَنَا بِالزِّرِّ دِي.',
    # 4
    'يُمَيِّزُ هارْت كُلَّ مُرْسِلَةٍ بِعُنْوَانِ اسْتِطْلَاعٍ مِنْ صِفْرٍ إِلَى خَمْسَةَ عَشَرَ. العُنْوَانُ صِفْرٌ يَعْنِي أَنَّ خَرْجَ أَرْبَعَةٍ إِلَى عِشْرِينَ مِلِّي أَمْبِيرٍ يَعْمَلُ طَبِيعِيًّا. وَالعَنَاوِينُ مِنْ وَاحِدٍ إِلَى خَمْسَةَ عَشَرَ تَعْنِي وَضْعَ مَلْتِي دْرُوبْ، وَفِيهِ يَثْبُتُ التَّيَّارُ قُرْبَ أَرْبَعَةِ مِلِّي أَمْبِيرٍ، فَلَا يَدُلُّ عَلَى الضَّغْطِ بَعْدَ ذٰلِكَ.',
    # 5
    'وَإِنْ لَمْ يَجِدِ الجِهَازُ مُرْسِلَةً، نَتَحَقَّقُ مِنَ التَّغْذِيَةِ وَمِنْ وُجُودِ مُقَاوَمَةِ هارْت فِي الحَلْقَةِ، ثُمَّ نَضْغَطُ رِيسْتَارْت.',
    # 6
    'بَعْدَ الِاخْتِيَارِ تَحُلُّ قَائِمَةُ هارْت مَحَلَّ قَائِمَةِ النَّافِذَةِ، وَتَتَحَوَّلُ كَمِّيَّةُ النَّافِذَةِ تِلْقَائِيًّا إِلَى الخَرْجِ الرَّقْمِيِّ، وَيُسَمَّى بِي فِي. البَنْدُ الأَوَّلُ لِفَصْلِ الجِهَازِ، وَهُوَ لَازِمٌ قَبْلَ تَغْيِيرِ كَمِّيَّةِ النَّافِذَةِ. ثُمَّ مَعْلُومَاتُ الجِهَازِ، ثُمَّ إِعْدَادَاتُهُ. وَبَنْدُ الوَحْدَةِ يُغَيِّرُ العَرْضَ فِي إِمْ سِي فايْف فَقَطْ، لَا فِي المُرْسِلَةِ. وَبَعْدَهُ تْرِمْ، وَإِضَافَةُ المُرْسِلَةِ إِلَى قَاعِدَةِ البَيَانَاتِ، وَسَنَرَاهُمَا فِي الحَلْقَتَيْنِ القَادِمَتَيْنِ.',
    # 7
    'وَنَصِيحَةٌ: نَجْعَلُ نَافِذَةً عَلَى الخَرْجِ الرَّقْمِيِّ بِي فِي، وَنَافِذَةً أُخْرَى عَلَى قِيَاسِ التَّيَّارِ. فَنَرَى فِي لَحْظَةٍ وَاحِدَةٍ مَا تَعْتَقِدُهُ المُرْسِلَةُ، وَمَا تُخْرِجُهُ فِعْلًا.',
    # 8
    'فِي مَعْلُومَاتِ الجِهَازِ نَقْرَأُ الوَسْمَ، وَرَقْمَ الجِهَازِ، وَالرَّقْمَ التَّسَلْسُلِيَّ، وَالشَّرِكَةَ المُصَنِّعَةَ، وَنَوْعَ الجِهَازِ، وَإِصْدَارَيِ البَرْنَامَجِ وَالعَتَادِ، وَالتَّارِيخَ، وَالوَصْفَ، وَالرِّسَالَةَ. وَالقَابِلُ لِلتَّعْدِيلِ خَمْسَةُ حُقُولٍ فَقَطْ: الوَسْمُ، وَالرَّقْمُ التَّسَلْسُلِيُّ، وَالتَّارِيخُ، وَالوَصْفُ، وَالرِّسَالَةُ. وَالبَاقِي لِلْقِرَاءَةِ.',
    # 9
    'أَهَمُّ صَفْحَةٍ هِيَ إِعْدَادَاتُ الجِهَازِ. فِيهَا الوَسْمُ، وَعُنْوَانُ الِاسْتِطْلَاعِ، ثُمَّ وَحْدَةُ الضَّغْطِ، وَقِيمَتَا المَدَى: الدُّنْيَا وَالعُلْيَا. ثُمَّ التَّخْمِيدُ، وَهُوَ زَمَنُ تَهْدِئَةِ القِرَاءَةِ؛ وَبَعْدَ كُلِّ نُقْطَةِ ضَغْطٍ نَنْتَظِرُ نَحْوَ خَمْسَةِ أَضْعَافِهِ.',
    # 10
    'ثُمَّ دَالَّةُ التَّحْوِيلِ: خَطِّيَّةٌ لِلضَّغْطِ، وَالجَذْرُ التَّرْبِيعِيُّ لِمُرْسِلَاتِ الضَّغْطِ التَّفَاضُلِيِّ فِي قِيَاسِ الجَرَيَانِ فَقَطْ. وَأَخِيرًا وَضْعُ بِيرْسْت، وَيَبْقَى مُغْلَقًا؛ فَالمُرْسِلَةُ لَا تُجِيبُ إِلَّا عِنْدَ السُّؤَالِ.',
    # 11
    'وَفِي الأَسْفَلِ بَيَانَاتُ الحَسَّاسِ: حَدَّاهُ الفِيزِيَائِيَّانِ الأَدْنَى وَالأَعْلَى، وَأَصْغَرُ مَدًى مَسْمُوحٌ بِهِ. هٰذِهِ حُدُودٌ ثَابِتَةٌ؛ فَلَا نُبَرْمِجُ المَدَى خَارِجَهَا، وَلَا أَضْيَقَ مِنْ أَصْغَرِ مَدًى.',
    # 12
    'لِلتَّعْدِيلِ نَضْغَطُ الزِّرَّ سِي: إِدِيت. نَنْقُلُ المُؤَشِّرَ بِالأَسْهُمِ إِلَى الحَقْلِ، وَنُدْخِلُ القِيمَةَ، وَنُؤَكِّدُهَا بِالزِّرِّ إِنْتَر. وَقَبْلَ التَّعْدِيلِ نُسَجِّلُ القِيَمَ الأَصْلِيَّةَ، وَبَعْدَهُ نَفْتَحُ الصَّفْحَةَ مِنْ جَدِيدٍ لِنَتَأَكَّدَ أَنَّ القِيمَةَ كُتِبَتْ.',
    # 13
    'وَهُنَا قَاعِدَةٌ مُهِمَّةٌ: تَغْيِيرُ المَدَى لَيْسَ مُعَايَرَةً. إِنَّهُ يُغَيِّرُ الضَّغْطَ الَّذِي يُقَابِلُ نِهَايَتَيْ مَجَالِ التَّيَّارِ: أَرْبَعَةَ مِلِّي أَمْبِيرٍ، وَعِشْرِينَ مِلِّي أَمْبِيرٍ. وَلَا يُصَحِّحُ خَطَأَ الحَسَّاسِ.',
    # 14
    'مِثَالٌ: المَدَى مِنْ صِفْرٍ إِلَى أَرْبَعِينَ كِيلُوغْرَامًا لِكُلِّ سَنْتِيمِتْرٍ مُرَبَّعٍ. عِنْدَ ضَغْطِ خَمْسَةَ عَشَرَ يَكُونُ التَّيَّارُ عَشَرَةَ مِلِّي أَمْبِيرٍ. فَإِذَا خَفَّضْنَا القِيمَةَ العُلْيَا إِلَى ثَلَاثِينَ، صَارَ الضَّغْطُ نَفْسُهُ يُقَابِلُ اثْنَيْ عَشَرَ مِلِّي أَمْبِيرٍ. الضَّغْطُ لَمْ يَتَغَيَّرْ، وَالمُرْسِلَةُ لَمْ تُصَحَّحْ؛ تَغَيَّرَ التَّقْسِيمُ فَقَطْ.',
    # 15
    'وَأَيُّ تَغْيِيرٍ لِلْمَدَى نُجْرِيهِ هُنَا نُجْرِي مِثْلَهُ فِي نِظَامِ التَّحَكُّمِ، وَإِلَّا قَرَأَتْ غُرْفَةُ التَّحَكُّمِ ضَغْطًا خَاطِئًا.',
    # 16
    'فِي الخُلَاصَةِ: صَفَّرْنَا المَرْجِعَ، وَاتَّصَلْنَا بِالمُرْسِلَةِ، وَتَعَرَّفْنَا عَلَى قَائِمَةِ هارْت وَصَفْحَتَيْ مَعْلُومَاتِ الجِهَازِ وَإِعْدَادَاتِهِ، وَعَدَّلْنَا حَقْلًا بِأَمَانٍ، وَعَرَفْنَا أَنَّ تَغْيِيرَ المَدَى لَيْسَ مُعَايَرَةً. وَفِي الحَلْقَةِ القَادِمَةِ نَفْحَصُ المُرْسِلَةَ وَنُعَدِّلُهَا بِأَمْرِ تْرِمْ.',
]

# Every spoken or shown value is checked against the data module; stop if it drifts.
assert D.I_BEFORE == 10.0 and D.I_AFTER == 12.0 and D.URV_NEW == 30.0 and D.P_EX == 15.0      # seg 14
assert D.URV == 40.0 and D.LRV == 0.0 and D.UNIT == "kgf/cm²"                                # seg 12-14
assert D.DAMPING == 0.40 and D.TRANSFER_FUNCTION == "Linear" and D.BURST_MODE == "Off"       # seg 9-10
assert D.POLLING_ADDRESS == 0 and D.MIN_SPAN < D.SPAN <= D.URL                               # seg 4, 11

AUDIO_DIR = audio_dir_for(__file__)

MCX, MCY = -2.45, 0.35          # the screen's place: left; the right zone (x 2.2 … 6.9) holds the notes
RX = 4.55                       # centre of the right zone
SOFT_MENU = ("Window 1\nSetup", "Window 2\nSetup", "Others", "Close\nMENU")
SOFT_BASIC = ("Calibration\nMode", "", "", "MENU")
DEV = "0 - PT-101 - DEMO"

HART_MENU = [(1, "Disconnect\nDevice"), (2, "Device\nInformation"), (3, "Device Settings"),
             (4, f"Unit [{D.UNIT}]"), (5, None), (6, "Trim Instrument"),
             (7, "Add HART Instrument\nto Database")]
SETTINGS = [("tag", "Tag", D.TAG), ("poll", "Polling Address", str(D.POLLING_ADDRESS)), ("#", "Output"),
            ("unit", "PV/Range Unit", D.UNIT), ("lrv", "Lower Range", D.fmt(D.LRV, 2)),
            ("urv", "Upper Range", D.fmt(D.URV, 2)), ("damp", "Damping (s)", D.fmt(D.DAMPING, 2)),
            ("tf", "Transfer Function", D.TRANSFER_FUNCTION), ("burst", "Burst Mode", D.BURST_MODE),
            ("#", "Sensor"), ("sn", "Serial Number", D.SERIAL), ("lrl", "Lower Limit", D.fmt(D.LRL, 2)),
            ("url", "Upper Limit", D.fmt(D.URL, 2)), ("ms", "Minimum Span", D.fmt(D.MIN_SPAN, 2))]
SETTINGS_EDIT = ("tag", "poll", "unit", "lrv", "urv", "damp", "tf", "burst", "sn")
INFO = [("tag", "Tag", D.TAG), ("id", "Device ID", D.DEVICE_ID), ("sn", "Serial Number", D.SERIAL),
        ("man", "Manufacturer", D.MANUFACTURER), ("type", "Device Type", D.DEVICE_TYPE),
        ("sw", "Software Version", D.SW_REV), ("hw", "Hardware Revision", D.HW_REV),
        ("date", "Date", D.DATE), ("desc", "Descriptor", D.DESCRIPTOR), ("msg", "Message", D.MESSAGE)]
INFO_EDIT = ("tag", "sn", "date", "desc", "msg")


class MC5Ep01(SyncedScene):
    def construct(self):
        self.timeline(NARRATION, AUDIO_DIR)
        c = self.cue

        def at(seg, phrase, nth=1, lead=0.0):
            self.sync(c(seg, phrase, nth) - lead)

        # ---------------- 1: title, then the screen appears ----------------
        title = title_card(self, "MC5 + HART: Connect & Configure", "Calibrating smart pressure transmitters",
                           series="MC5 HART series · Episode 1", y=0.9)
        at(1, "نَقْرَأُ")
        self.play(FadeOut(title), run_time=0.5)
        mc = MC5("BASIC")
        mc.move_to([MCX, MCY, 0])
        page = mc.windows_page(
            {"title": "1 Pressure", "port": f"P1: REF 0…{D.REF_MODULE_MAX:g}", "value": D.fmt(D.REF_ZERO_DRIFT), "unit": D.UNIT},
            {"title": "2 Current", "port": "E: Current Measurement", "value": D.fmt(D.I_STORY_ZERO, 4), "unit": "mA"},
            softkeys=SOFT_BASIC)
        self.play(FadeIn(mc), run_time=0.6)
        mc.show(self, page)
        self.sync(self.end(1))

        # ---------------- 2: zero the reference module ----------------
        at(2, "مَفْتُوحٌ")
        n1 = note_line("Port open to air", "wind").move_to([RX, 1.6, 0])
        self.play(FadeIn(n1, shift=LEFT * 0.2), run_time=0.5)
        at(2, "الزِّرَّ دِي", lead=0.2)
        mc.press(self, "D")
        mc.set_softkeys(self, SOFT_MENU)
        at(2, "الزِّرَّ إِيه", lead=0.2)
        mc.press(self, "A")
        mc.open_menu(self, page, [(i, None) for i in range(1, 7)] + [(7, "Zero Pressure\nModule")])
        at(2, "رَقْمَ سَبْعَةٍ", lead=0.3)
        mc.press_digit(self, 7, page.menu)
        at(2, "فَتَعُودُ", lead=0.1)
        mc.close_menu(self, page)
        mc.set_softkeys(self, SOFT_BASIC, run_time=0.2)
        mc.set_text(self, page.parts["value1"], D.fmt(0.0), align=RIGHT)
        self.play(Indicate(page.parts["value1"], color=ACCENT_3, scale_factor=1.12), run_time=0.8)
        at(2, "كُلَّمَا")
        n2 = note_line("Repeat when the position or height changes", "refresh", width=3.9).move_to([RX - 0.3, 0.3, 0])
        self.play(FadeIn(n2, shift=LEFT * 0.2), run_time=0.5)
        self.sync(self.end(2))
        self.play(FadeOut(n1), FadeOut(n2), run_time=0.4)

        # ---------------- 3: connect ----------------
        at(3, "الزِّرَّ دِي", lead=0.2)
        mc.press(self, "D")
        mc.set_softkeys(self, SOFT_MENU)
        at(3, "الزِّرَّ بِي", lead=0.2)
        mc.press(self, "B")
        mc.open_menu(self, page, [(i, None) for i in range(1, 5)] + [(5, "HART"), (6, None), (7, None)])
        at(3, "رَقْمَ خَمْسَةٍ", lead=0.3)
        mc.press_digit(self, 5, page.menu)
        at(3, "يَبْحَثُ", lead=0.2)
        lst = mc.list_page("HART", ["Searching for HART Device at: 0", "", "Devices found:", ("dev", DEV)],
                           softkeys=("Back", "", "Restart", "Select"))
        lst.parts["dev"].set_opacity(0)
        mc.show(self, lst)
        self.play(lst.parts["dev"].animate.set_opacity(1), run_time=0.5)
        at(3, "سِتَّ عَشْرَةَ", lead=0.2)
        chip16 = VGroup(label("16", 72, ACCENT_1, weight=BOLD), fit(label("devices on one loop, at most", FS_AXIS), 3.8)
                        ).arrange(DOWN, buff=0.15).move_to([RX, 1.0, 0])
        self.play(FadeIn(chip16, shift=LEFT * 0.2), run_time=0.5)
        at(3, "بِالزِّرِّ دِي", lead=0.2)
        cur = lst.parts["cursor"]
        self.play(cur.animate.set_opacity(1), lst.parts["dev"].animate.set_color(BG), run_time=0.4)
        mc.press(self, "D")
        self.sync(self.end(3))
        self.play(FadeOut(chip16), run_time=0.4)

        # ---------------- 4: polling address ----------------
        at(4, "العُنْوَانُ صِفْرٌ", lead=0.3)
        g0 = ma_gauge("Address 0: 4–20 mA live", width=3.6)
        card0 = panel(4.6, 2.5).move_to([RX, 1.5, 0])
        g0.move_to(card0.get_center())
        self.play(Create(card0), FadeIn(g0), run_time=0.6)
        gauge_to(self, g0, 4.0, "4.0 mA", run_time=0.4)
        gauge_to(self, g0, 12.0, "12.0 mA", run_time=1.0)
        gauge_to(self, g0, 20.0, "20.0 mA", run_time=1.0)
        at(4, "وَالعَنَاوِينُ", lead=0.3)
        multi = mc.list_page("HART", ["Searching for HART Device at: 15", "", "Devices found:",
                                      "1 - PT-101 - DEMO", "2 - PT-102 - DEMO", "3 - PT-103 - DEMO"],
                             softkeys=("Back", "", "Restart", "Select"))
        mc.show(self, multi)
        g1 = ma_gauge("Addresses 1–15: Multidrop", width=3.6, color=ACCENT_4)
        card1 = panel(4.6, 2.5).move_to([RX, -1.25, 0])
        g1.move_to(card1.get_center())
        gauge_to(self, g0, 8.0, "tracks the pressure", run_time=0.5)
        self.play(Create(card1), FadeIn(g1), run_time=0.6)
        gauge_to(self, g1, 12.0, "12.0 mA", run_time=0.5)
        at(4, "يَثْبُتُ", lead=0.2)
        gauge_to(self, g1, 4.0, "fixed near 4 mA", run_time=0.9)
        lock = icon("lock", ACCENT_4, 0.45).next_to(g1.readout, RIGHT, buff=0.25)
        self.play(FadeIn(lock, scale=0.8), run_time=0.4)
        self.sync(self.end(4))

        # ---------------- 5: nothing found: supply, HART resistor, Restart ----------------
        at(5, "وَإِنْ", lead=0.1)
        self.play(FadeOut(VGroup(card0, g0, g0.readout, card1, g1, g1.readout, lock)), run_time=0.4)
        empty = mc.list_page("HART", ["Searching for HART Device at: 0", "", "Devices found:"],
                             softkeys=("Back", "", "Restart", "Select"))
        mc.show(self, empty)
        k1 = note_line("Supply", "plug").move_to([RX, 1.2, 0])
        k2 = note_line("HART resistor", "bolt").move_to([RX, 0.4, 0])
        at(5, "نَتَحَقَّقُ")
        self.play(FadeIn(k1, shift=LEFT * 0.2), run_time=0.4)
        self.play(FadeIn(k2, shift=LEFT * 0.2), run_time=0.4)
        at(5, "رِيسْتَارْت", lead=0.3)
        mc.press(self, "C")
        again = mc.list_page("HART", ["Searching for HART Device at: 0", "", "Devices found:", ("dev", DEV)],
                             softkeys=("Back", "", "Restart", "Select"), selected="dev")
        mc.show(self, again)
        self.sync(self.end(5))
        self.play(FadeOut(k1), FadeOut(k2), run_time=0.3)

        # ---------------- 6: the HART menu ----------------
        at(6, "تَحُلُّ", lead=0.3)
        mc.press(self, "D")
        hw = mc.windows_page(
            {"title": "1 Pressure", "port": f"P1: REF 0…{D.REF_MODULE_MAX:g}", "value": D.fmt(0.0), "unit": D.UNIT},
            {"title": "2 Current", "port": "E: Current Measurement", "value": D.fmt(D.I_STORY_ZERO, 4), "unit": "mA"},
            softkeys=SOFT_MENU)
        mc.show(self, hw)
        mc.open_menu(self, hw, HART_MENU)
        at(6, "تَتَحَوَّلُ")
        p = hw.parts
        mc.swap_many(self, hw, [("title2", "2 Pressure", LEFT), ("port2", "E: HART/PV", LEFT),
                                ("value2", D.fmt(D.PV_OFFSET), RIGHT), ("unit2", D.UNIT, RIGHT)])
        m = hw.menu

        def row_call(n, text, color=ACCENT_1):
            y = m.numbers[m.k(n)].get_y()
            lab = fit(label(text, FS_AXIS, color), 4.3)
            lab.move_to([2.4 + lab.width / 2, y, 0])
            arr = Arrow([2.3, y, 0], [1.75, y, 0], buff=0, stroke_width=3, color=color, max_tip_length_to_length_ratio=0.5)
            return VGroup(lab, arr)

        at(6, "البَنْدُ الأَوَّلُ", lead=0.2)
        m.select(self, 1)
        k = row_call(1, "needed before changing the quantity")
        self.play(FadeIn(k), run_time=0.4)
        at(6, "مَعْلُومَاتُ", lead=0.2)
        self.play(FadeOut(k), run_time=0.2)
        m.select(self, 2, run_time=0.35)
        at(6, "إِعْدَادَاتُهُ", lead=0.2)
        m.select(self, 3, run_time=0.35)
        at(6, "بَنْدُ الوَحْدَةِ", lead=0.2)
        m.select(self, 4, run_time=0.35)
        k = row_call(4, "changes MC5's display only")
        self.play(FadeIn(k), run_time=0.4)
        at(6, "تْرِمْ", lead=0.2)
        self.play(FadeOut(k), run_time=0.2)
        m.select(self, 6, run_time=0.35)
        at(6, "إِضَافَةُ", lead=0.2)
        m.select(self, 7, run_time=0.35)
        self.sync(self.end(6))

        # ---------------- 7: tip: two windows ----------------
        at(7, "نَافِذَةً", lead=0.3)
        mc.close_menu(self, hw)
        mc.set_softkeys(self, SOFT_BASIC, run_time=0.2)
        mc.swap_many(self, hw, [("title1", "1 Current", LEFT), ("port1", "E: Current Measurement", LEFT),
                                ("value1", D.fmt(D.I_STORY_ZERO, 4), RIGHT), ("unit1", "mA", RIGHT)])
        at(7, "مَا تَعْتَقِدُهُ", lead=0.2)
        y2 = p["value2"].get_y()
        t2 = fit(label("what the transmitter thinks (PV)", FS_AXIS, ACCENT_1), 4.3)
        t2.move_to([2.4 + t2.width / 2, y2, 0])
        r2 = Arrow([2.3, y2, 0], [1.75, y2, 0], buff=0, stroke_width=3, color=ACCENT_1)
        self.play(FadeIn(t2), Create(r2), run_time=0.5)
        at(7, "مَا تُخْرِجُهُ", lead=0.2)
        y1 = p["value1"].get_y()
        t1 = fit(label("what it outputs (current)", FS_AXIS, ACCENT_2), 4.3)
        t1.move_to([2.4 + t1.width / 2, y1, 0])
        r1 = Arrow([2.3, y1, 0], [1.75, y1, 0], buff=0, stroke_width=3, color=ACCENT_2)
        self.play(FadeIn(t1), Create(r1), run_time=0.5)
        self.sync(self.end(7))
        self.play(FadeOut(VGroup(t1, t2, r1, r2)), run_time=0.4)

        # ---------------- 8: Device Information ----------------
        at(8, "مَعْلُومَاتِ", lead=0.3)
        info = mc.form_page("DEVICE INFORMATION", INFO, editable=INFO_EDIT, softkeys=("Close", "", "", ""))
        mc.show(self, info)
        legend = VGroup(label("Editable (blue)", FS_BODY - 8, ACCENT_1, weight=BOLD)).move_to([RX, 2.0, 0])
        order = [("tag", "الوَسْمَ"), ("id", "وَرَقْمَ"), ("sn", "الرَّقْمَ التَّسَلْسُلِيَّ"), ("man", "الشَّرِكَةَ"),
                 ("type", "نَوْعَ"), ("sw", "إِصْدَارَيِ"), ("date", "التَّارِيخَ"), ("desc", "الوَصْفَ"),
                 ("msg", "الرِّسَالَةَ")]
        mc.move_form_cursor(self, info, "tag", run_time=0.3)
        for key, phrase in order[1:]:
            at(8, phrase, lead=0.15)
            mc.move_form_cursor(self, info, key, run_time=0.3)
        at(8, "خَمْسَةُ حُقُولٍ", lead=0.2)
        self.play(FadeIn(legend), run_time=0.4)
        names = {"tag": "Tag", "sn": "Serial Number", "date": "Date", "desc": "Descriptor", "msg": "Message"}
        chips = []
        for key, phrase, nth in [("tag", "الوَسْمُ", 1), ("sn", "الرَّقْمُ التَّسَلْسُلِيُّ", 1), ("date", "التَّارِيخُ", 1),
                                 ("desc", "الوَصْفُ", 1), ("msg", "الرِّسَالَةُ", 1)]:
            at(8, phrase, lead=0.1)
            ch = label(names[key], FS_LABEL, ACCENT_1).move_to([RX, 1.25 - 0.62 * len(chips), 0])
            chips.append(ch)
            mc.move_form_cursor(self, info, key, run_time=0.3)
            self.play(FadeIn(ch, shift=LEFT * 0.2), run_time=0.3)
        at(8, "وَالبَاقِي", lead=0.1)
        ro = label("the rest: read only", FS_LABEL, GREY_INK).move_to([RX, 1.25 - 0.62 * 5 - 0.2, 0])
        self.play(FadeIn(ro), run_time=0.4)
        self.sync(self.end(8))
        self.play(FadeOut(VGroup(legend, ro, *chips)), run_time=0.4)

        # ---------------- 9: Device Settings, range and damping ----------------
        at(9, "أَهَمُّ", lead=0.2)
        setA = mc.form_page("DEVICE SETTINGS", SETTINGS[:9], editable=SETTINGS_EDIT, softkeys=("Close", "", "Edit", ""))
        setA.add(mono("▼", FS_SMALL if False else 14, GREY_INK).move_to([mc.area()[1] - 0.15, mc.area()[3] + 0.18, 0]))
        mc.show(self, setA)
        mc.move_form_cursor(self, setA, "tag", run_time=0.3)
        at(9, "عُنْوَانُ", lead=0.2)
        mc.move_form_cursor(self, setA, "poll", run_time=0.3)
        at(9, "وَحْدَةُ", lead=0.2)
        mc.move_form_cursor(self, setA, "unit", run_time=0.3)
        at(9, "قِيمَتَا", lead=0.2)
        mc.move_form_cursor(self, setA, "lrv", run_time=0.3)
        at(9, "العُلْيَا", lead=0.2)
        mc.move_form_cursor(self, setA, "urv", run_time=0.3)
        at(9, "التَّخْمِيدُ", lead=0.2)
        mc.move_form_cursor(self, setA, "damp", run_time=0.3)
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 1.1, 0.5], x_length=4.0, y_length=2.2, tips=False,
                  axis_config={"include_numbers": False, "stroke_width": 3, "color": INK}).move_to([RX, 0.5, 0])
        curve = ax.plot(lambda t: 1 - np.exp(-t), x_range=[0, 5.5], color=ACCENT_2, stroke_width=5)
        yl = label("reading", FS_AXIS, INK).next_to(ax, UP, buff=0.2).align_to(ax, LEFT)
        xl = label("time (s)", FS_AXIS, INK).next_to(ax, DOWN, buff=0.45).align_to(ax, RIGHT)
        self.play(Create(ax), FadeIn(yl), FadeIn(xl), run_time=0.6)
        self.play(Create(curve), run_time=1.5)
        at(9, "نَحْوَ خَمْسَةِ", lead=0.2)
        x5 = ax.c2p(5, 0)
        vl = DashedLine(x5, ax.c2p(5, 1 - np.exp(-5)), color=ACCENT_1, stroke_width=3)
        dot = Dot(ax.c2p(5, 1 - np.exp(-5)), color=ACCENT_1, radius=0.07)
        tl = label("wait about 5 × damping", FS_AXIS, ACCENT_1).next_to(ax, DOWN, buff=1.0)
        self.play(Create(vl), FadeIn(dot), FadeIn(tl), run_time=0.6)
        self.sync(self.end(9))
        self.play(FadeOut(VGroup(ax, curve, yl, xl, vl, dot, tl)), run_time=0.4)

        # ---------------- 10: transfer function, burst mode ----------------
        at(10, "دَالَّةُ", lead=0.2)
        mc.move_form_cursor(self, setA, "tf", run_time=0.3)

        def mini(title, fn, x):
            a = Axes(x_range=[0, 1, 1], y_range=[0, 1, 1], x_length=1.9, y_length=1.5, tips=False,
                     axis_config={"include_numbers": False, "stroke_width": 3, "color": INK}).move_to([x, 0.9, 0])
            cv = a.plot(fn, x_range=[0, 1], color=ACCENT_2, stroke_width=5)
            tt = label(title, FS_AXIS, INK).next_to(a, UP, buff=0.3)
            return VGroup(a, cv, tt)
        lin = mini("Linear", lambda x: x, RX - 1.25)
        sq = mini("Square Root", lambda x: np.sqrt(x), RX + 1.25)
        self.play(FadeIn(lin), run_time=0.6)
        at(10, "الجَذْرُ", lead=0.2)
        self.play(FadeIn(sq), run_time=0.6)
        n_l = VGroup(label("Linear: for pressure", 20, GREY_INK),
                     label("Square Root: for differential", 20, GREY_INK),
                     label("pressure in flow only", 20, GREY_INK)).arrange(DOWN, buff=0.1).move_to([RX, -0.7, 0])
        self.play(FadeIn(n_l), run_time=0.4)
        at(10, "بِيرْسْت", lead=0.3)
        mc.move_form_cursor(self, setA, "burst", run_time=0.3)
        burst = VGroup(icon("wifi", ACCENT_4, 0.5), label("Burst: Off", FS_LABEL, INK, weight=BOLD)).arrange(RIGHT, buff=0.2)
        burst_n = label("it answers only when asked", FS_AXIS, GREY_INK)
        VGroup(burst, burst_n).arrange(DOWN, buff=0.2).move_to([RX, -2.45, 0])
        self.play(FadeIn(burst, shift=UP * 0.15), run_time=0.5)
        at(10, "تُجِيبُ", lead=0.2)
        self.play(FadeIn(burst_n), run_time=0.4)
        self.sync(self.end(10))
        self.play(FadeOut(VGroup(lin, sq, n_l, burst, burst_n)), run_time=0.4)

        # ---------------- 11: sensor data: limits and minimum span ----------------
        at(11, "الأَسْفَلِ", lead=0.3)
        setB = mc.form_page("DEVICE SETTINGS", SETTINGS[6:], editable=SETTINGS_EDIT, softkeys=("Close", "", "Edit", ""))
        setB.add(mono("▲", 14, GREY_INK).move_to([mc.area()[1] - 0.15, mc.area()[2] - 0.2, 0]))
        mc.show(self, setB, shift=UP * 0.5)
        mc.move_form_cursor(self, setB, "lrl", run_time=0.3)
        nl = Line(LEFT * 1.8, RIGHT * 1.8, color=INK, stroke_width=4).move_to([RX, 0.6, 0])
        def px(v):
            return nl.get_left()[0] + 3.6 * v / D.URL
        ticks = VGroup(Line([px(0), 0.5, 0], [px(0), 0.7, 0], color=INK, stroke_width=3),
                       Line([px(D.URL), 0.5, 0], [px(D.URL), 0.7, 0], color=INK, stroke_width=3))
        lbl0 = label(f"LRL {D.fmt(D.LRL, 2)}", FS_AXIS, INK)
        lbl0.move_to([px(0) - 0.15 + lbl0.width / 2, 0.1, 0])
        lbl1 = label(f"URL {D.fmt(D.URL, 2)}", FS_AXIS, INK)
        lbl1.move_to([px(D.URL) + 0.15 - lbl1.width / 2, 0.1, 0])
        self.play(Create(nl), Create(ticks), FadeIn(lbl0), FadeIn(lbl1), run_time=0.7)
        at(11, "حَدَّاهُ", lead=0.2)
        mc.move_form_cursor(self, setB, "url", run_time=0.3)
        rng = Line([px(D.LRV), 0.6, 0], [px(D.URV), 0.6, 0], color=ACCENT_3, stroke_width=9)
        rl = label(f"range {D.LRV:g}–{D.URV:g}", FS_AXIS, ACCENT_3).move_to([RX, 1.2, 0])
        self.play(Create(rng), FadeIn(rl), run_time=0.6)
        at(11, "أَصْغَرُ مَدًى", lead=0.2)
        mc.move_form_cursor(self, setB, "ms", run_time=0.3)
        ms = Line([px(0), -0.5, 0], [px(D.MIN_SPAN), -0.5, 0], color=ACCENT_1, stroke_width=9)
        mst = label(f"Minimum Span {D.fmt(D.MIN_SPAN, 2)}", FS_AXIS, ACCENT_1).move_to([RX, -0.95, 0])
        self.play(Create(ms), FadeIn(mst), run_time=0.6)
        at(11, "لَا نُبَرْمِجُ", lead=0.2)
        no = icon("x", ACCENT_4, 0.55).move_to([RX, -1.8, 0])
        nol = VGroup(label("outside the limits", 22, ACCENT_4), label("or below the minimum span", 22, ACCENT_4)
                     ).arrange(DOWN, buff=0.08).next_to(no, DOWN, buff=0.15)
        self.play(FadeIn(no, scale=0.8), FadeIn(nol), run_time=0.5)
        self.sync(self.end(11))
        self.play(FadeOut(VGroup(nl, ticks, lbl0, lbl1, rng, rl, ms, mst, no, nol)), run_time=0.4)

        # ---------------- 12: editing ----------------
        at(12, "الزِّرَّ سِي", lead=0.3)
        setA2 = mc.form_page("DEVICE SETTINGS", SETTINGS[:9], editable=SETTINGS_EDIT, selected="urv",
                             softkeys=("Close", "", "Edit", ""))
        setA2.add(mono("▼", 14, GREY_INK).move_to([mc.area()[1] - 0.15, mc.area()[3] + 0.18, 0]))
        mc.show(self, setA2, shift=DOWN * 0.5)
        steps = VGroup(*[note_line(t, ic, width=4.4) for t, ic in [
            ("1  Record the original values", "clipboard-check"), ("2  Edit, then Enter", "tool"),
            ("3  Re-open the page and verify", "eye")]]).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([RX, 0.9, 0])
        mc.press(self, "C")
        at(12, "المُؤَشِّرَ", lead=0.2)
        mc.set_mode(self, "EDIT")
        at(12, "نُدْخِلُ", lead=0.2)
        mc.set_text(self, setA2.parts["urv"], D.fmt(D.URV_NEW, 2), align=RIGHT)
        at(12, "إِنْتَر", lead=0.3)
        mc.press_chip(self, "Enter")
        mc.set_mode(self, "BASIC")
        at(12, "نُسَجِّلُ", lead=0.2)
        self.play(FadeIn(steps[0], shift=LEFT * 0.2), run_time=0.4)
        self.play(FadeIn(steps[1], shift=LEFT * 0.2), run_time=0.4)
        at(12, "نَفْتَحُ", lead=0.2)
        reopen = mc.form_page("DEVICE SETTINGS", SETTINGS[:5] + [("urv", "Upper Range", D.fmt(D.URV_NEW, 2))] + SETTINGS[6:9],
                              editable=SETTINGS_EDIT, selected="urv", softkeys=("Close", "", "Edit", ""))
        mc.show(self, reopen)
        self.play(FadeIn(steps[2], shift=LEFT * 0.2), run_time=0.4)
        self.sync(self.end(12))

        # ---------------- 13: rerange is not calibration ----------------
        self.clear()
        at(13, "قَاعِدَةٌ", lead=0.2)
        scale = Line(LEFT * 5.2, RIGHT * 5.2, color=INK, stroke_width=4).move_to([0, 0.4, 0])

        def X(v):
            return scale.get_left()[0] + 10.4 * v / D.URL
        tk = VGroup()
        for v in (0, 10, 20, 30, 40, 50):
            tk.add(Line([X(v), 0.3, 0], [X(v), 0.5, 0], color=INK, stroke_width=3))
            tk.add(label(f"{v}", FS_AXIS, INK).move_to([X(v), -0.0, 0]))
        sc_l = label(f"pressure, {D.UNIT}", FS_LABEL, INK).next_to(scale, UP, buff=1.25).align_to(scale, LEFT)
        m4 = VGroup(Triangle(color=ACCENT_1, stroke_width=0).set_fill(ACCENT_1, 1).scale(0.16).rotate(PI),
                    label("4 mA", FS_LABEL, ACCENT_1, weight=BOLD))
        m4[0].move_to([X(D.LRV), 0.85, 0]); m4[1].next_to(m4[0], UP, buff=0.1)
        m20 = VGroup(Triangle(color=ACCENT_1, stroke_width=0).set_fill(ACCENT_1, 1).scale(0.16).rotate(PI),
                     label("20 mA", FS_LABEL, ACCENT_1, weight=BOLD))
        m20[0].move_to([X(D.URV), 0.85, 0]); m20[1].next_to(m20[0], UP, buff=0.1)
        self.play(Create(scale), FadeIn(tk), FadeIn(sc_l), run_time=0.7)
        self.play(FadeIn(m4), FadeIn(m20), run_time=0.5)
        at(13, "يُغَيِّرُ الضَّغْطَ", lead=0.2)
        self.play(m20.animate.shift(RIGHT * (X(D.URV_NEW) - X(D.URV))), run_time=1.2)
        at(13, "وَلَا يُصَحِّحُ", lead=0.2)
        err_t = label("sensor error", FS_LABEL, ACCENT_4, weight=BOLD)
        e1 = Line([X(20), -1.4, 0], [X(20), -0.9, 0], color=INK, stroke_width=4)
        e2 = Line([X(20) + 0.55, -1.4, 0], [X(20) + 0.55, -0.9, 0], color=ACCENT_4, stroke_width=4)
        br = Line([X(20), -1.15, 0], [X(20) + 0.55, -1.15, 0], color=ACCENT_4, stroke_width=3)
        t_true = label("true pressure", FS_AXIS, INK).next_to(e1, LEFT, buff=0.2)
        t_read = label("reading", FS_AXIS, ACCENT_4).next_to(e2, RIGHT, buff=0.2)
        err_t.next_to(br, DOWN, buff=0.3)
        unch = label("unchanged by the range", FS_AXIS, GREY_INK).next_to(err_t, DOWN, buff=0.2)
        self.play(Create(e1), Create(e2), Create(br), FadeIn(t_true), FadeIn(t_read), FadeIn(err_t), run_time=0.8)
        self.play(FadeIn(unch), run_time=0.4)
        self.sync(self.end(13))
        self.clear()

        # ---------------- 14: the worked example ----------------
        at(14, "مِثَالٌ", lead=0.2)
        ax = Axes(x_range=[0, 40, 10], y_range=[4, 20, 4], x_length=5.0, y_length=3.4, tips=False,
                  axis_config={"include_numbers": False, "stroke_width": 3, "color": INK}).move_to([-3.6, 0.0, 0])
        xt = VGroup(*[label(f"{v}", FS_TAG, INK).move_to(ax.c2p(v, 4) + DOWN * 0.3) for v in (0, 10, 20, 30, 40)])
        yt = VGroup(*[label(f"{v}", FS_TAG, INK).move_to(ax.c2p(0, v) + LEFT * 0.35) for v in (4, 12, 20)])
        xlab = label(f"pressure, {D.UNIT}", FS_AXIS, INK).next_to(ax, DOWN, buff=0.7)
        ylab = label("current, mA", FS_AXIS, INK).next_to(ax, UP, buff=0.2).align_to(ax, LEFT)
        f1 = ax.plot(lambda x: 4 + 16 * x / D.URV, x_range=[0, D.URV], color=GREY_INK, stroke_width=5)
        eqf = label("I = 4 + 16 × (P − LRV) / (URV − LRV)", FS_BODY - 6, INK, weight=BOLD).move_to([3.3, 2.0, 0])
        fit(eqf, 6.6)
        self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xlab), FadeIn(ylab), run_time=0.7)
        self.play(Create(f1), Write(eqf), run_time=1.2)
        at(14, "خَمْسَةَ عَشَرَ", lead=0.2)
        pd = DashedLine(ax.c2p(D.P_EX, 4), ax.c2p(D.P_EX, D.I_BEFORE), color=ACCENT_1, stroke_width=3)
        pdot = Dot(ax.c2p(D.P_EX, D.I_BEFORE), color=ACCENT_1, radius=0.08)
        pl = label(f"P = {D.P_EX:g}", FS_AXIS, ACCENT_1).next_to(ax.c2p(D.P_EX, 4), DOWN, buff=0.75)
        self.play(Create(pd), FadeIn(pdot), run_time=0.5)
        at(14, "عَشَرَةَ مِلِّي", lead=0.2)
        b_eq = label(f"URV = {D.URV:g}:   I = 4 + 16 × {D.P_EX:g} / {D.URV:g} = {D.I_BEFORE:.3f} mA", FS_BODY - 8, INK)
        fit(b_eq, 6.6)
        b_eq.move_to([3.3, 0.8, 0])
        ph = DashedLine(ax.c2p(0, D.I_BEFORE), ax.c2p(D.P_EX, D.I_BEFORE), color=ACCENT_1, stroke_width=3)
        ph_l = label(f"{D.I_BEFORE:g}", FS_TAG, ACCENT_1, weight=BOLD).move_to(ax.c2p(0, D.I_BEFORE) + LEFT * 0.35)
        self.play(FadeIn(b_eq, shift=UP * 0.1), Create(ph), FadeIn(ph_l), run_time=0.6)
        at(14, "ثَلَاثِينَ", lead=0.2)
        f2 = ax.plot(lambda x: 4 + 16 * x / D.URV_NEW, x_range=[0, D.URV_NEW], color=ACCENT_2, stroke_width=5)
        urv_m = Dot(ax.c2p(D.URV_NEW, 20), color=ACCENT_2, radius=0.08)
        urv_l = label(f"URV {D.URV_NEW:g}", FS_AXIS, ACCENT_2).next_to(urv_m, UP, buff=0.2)
        self.play(Create(f2), FadeIn(urv_m), FadeIn(urv_l), run_time=1.0)
        at(14, "اثْنَيْ عَشَرَ", lead=0.2)
        pdot2 = Dot(ax.c2p(D.P_EX, D.I_AFTER), color=ACCENT_2, radius=0.08)
        a_eq = label(f"URV = {D.URV_NEW:g}:   I = 4 + 16 × {D.P_EX:g} / {D.URV_NEW:g} = {D.I_AFTER:.3f} mA", FS_BODY - 8, ACCENT_2)
        fit(a_eq, 6.6)
        a_eq.move_to([3.3, -0.3, 0])
        ph2 = DashedLine(ax.c2p(0, D.I_AFTER), ax.c2p(D.P_EX, D.I_AFTER), color=ACCENT_2, stroke_width=3)
        self.play(Transform(pdot.copy(), pdot2), FadeIn(pdot2), FadeIn(a_eq, shift=UP * 0.1), Create(ph2), run_time=0.8)
        at(14, "الضَّغْطُ لَمْ", lead=0.2)
        sa = label("same pressure, different current", FS_LABEL, INK, weight=BOLD).move_to([3.3, -1.7, 0])
        fit(sa, 6.6)
        self.play(FadeIn(sa), run_time=0.5)
        self.sync(self.end(14))
        self.clear()

        # ---------------- 15: the control system ----------------
        at(15, "نِظَامِ التَّحَكُّمِ", lead=0.3)
        tx = VGroup(panel(3.8, 1.9, ACCENT_1), label("Transmitter", FS_BODY - 8, INK, weight=BOLD),
                    label(f"{D.LRV:g}–{D.URV_NEW:g} {D.UNIT}", FS_LABEL, ACCENT_1)).arrange(DOWN, buff=0.3)
        tx[0].move_to(tx[1:].get_center())
        cs = VGroup(panel(3.8, 1.9, ACCENT_2), label("Control system", FS_BODY - 8, INK, weight=BOLD),
                    label(f"{D.LRV:g}–{D.URV:g} {D.UNIT}", FS_LABEL, ACCENT_2)).arrange(DOWN, buff=0.3)
        cs[0].move_to(cs[1:].get_center())
        VGroup(tx, cs).arrange(RIGHT, buff=2.8).move_to([0, 0.5, 0])
        wire = Arrow(tx.get_right() + RIGHT * 0.1, cs.get_left() + LEFT * 0.1, buff=0, stroke_width=5, color=INK)
        wl = label("4–20 mA", FS_AXIS, INK).next_to(wire, UP, buff=0.15)
        self.play(FadeIn(tx), FadeIn(cs), Create(wire), FadeIn(wl), run_time=0.8)
        at(15, "ضَغْطًا خَاطِئًا", lead=0.3)
        bad = label(f"actual {D.P_EX:g} → shows {D.P_MISREAD:g}", FS_LABEL, ACCENT_4, weight=BOLD).next_to(cs, DOWN, buff=0.5)
        xi = icon("alert-triangle", ACCENT_4, 0.6).next_to(bad, LEFT, buff=0.2)
        self.play(FadeIn(bad), FadeIn(xi), run_time=0.5)
        self.sync(self.end(15) - 1.6)
        new_r = label(f"{D.LRV:g}–{D.URV_NEW:g} {D.UNIT}", FS_LABEL, ACCENT_3).move_to(cs[2])
        ok = label(f"actual {D.P_EX:g} → shows {D.P_EX:g}", FS_LABEL, ACCENT_3, weight=BOLD).move_to(bad)
        self.play(Transform(cs[2], new_r), Transform(bad, ok), FadeOut(xi), run_time=0.8)
        self.sync(self.end(15))
        self.clear()

        # ---------------- 16: summary ----------------
        summary_box(self, "Summary",
                    ["Zero the reference module", "Connect: the polling address", "HART menu: information and settings",
                     "Edit safely: record, edit, verify", "A range change is not a calibration"],
                    cues=[c(16, "صَفَّرْنَا"), c(16, "اتَّصَلْنَا"), c(16, "تَعَرَّفْنَا"), c(16, "عَدَّلْنَا"), c(16, "عَرَفْنَا")])
        self.sync(self.end(16) + 0.8)


if __name__ == "__main__":
    main(__file__, "MC5Ep01", NARRATION)
