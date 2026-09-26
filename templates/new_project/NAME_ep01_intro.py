"""NAME, episode 1: <topic>.

Build (from the repo root):
    python projects/NAME/NAME_ep01_intro.py --preview   # 480p15 -> tmp/NAME_ep01_intro/preview.mp4
    python projects/NAME/NAME_ep01_intro.py             # 1080p30 -> output/NAME_ep01_intro.mp4
"""
from explainer import *
import NAME_data as D           # delete with the data module if the topic has no numbers

# Fully diacritized narration (owner-approved <date>) — one entry per scene.
NARRATION = [
    # 1 title (episode 1 of a technical topic opens with the educational-material sentence)
    "هٰذِهِ مَادَّةٌ تَعْلِيمِيَّةٌ؛ وَالمَرْجِعُ المُلْزِمُ هُوَ الوَثَائِقُ الرَّسْمِيَّةُ وَالإِجْرَاءَاتُ المُعْتَمَدَةُ. نَتَعَرَّفُ فِي هٰذِهِ الحَلْقَةِ عَلَى الفِكْرَةِ الأَسَاسِيَّةِ.",
    # 2 key points
    "نَبْدَأُ بِثَلَاثِ نِقَاطٍ: التَّعْرِيفُ، ثُمَّ المُكَوِّنَاتُ، ثُمَّ طَرِيقَةُ العَمَلِ.",
    # 3 a number from the data module
    "إِذَا كَانَ الحَجْمُ رُبْعَ مِتْرٍ مُكَعَّبٍ، وَالتَّدَفُّقُ مِئَتَيْنِ وَخَمْسِينَ مِتْرًا مُكَعَّبًا فِي السَّاعَةِ، فَزَمَنُ المَلْءِ ثَلَاثُ ثَوَانٍ وَسِتَّةُ أَعْشَارٍ.",
    # 4 summary
    "إِذَنْ: عَرَفْنَا الفِكْرَةَ، وَالمُكَوِّنَاتِ، وَحَسَبْنَا مِثَالًا بَسِيطًا.",
]

# Every spoken or shown value is checked against the data module; stop if it drifts.
assert f"{D.FILL_TIME:.1f}" == "3.6"                                          # seg 3

AUDIO_DIR = audio_dir_for(__file__)


class NAMEEp01(SyncedScene):
    def construct(self):
        self.timeline(NARRATION, AUDIO_DIR)

        # ---------------- Segment 1: title ----------------
        title_card(self, "Episode title", "One-line subtitle", series="Series name · Episode 1")
        self.sync(self.end(1) - 0.8)
        self.clear()

        # ---------------- Segment 2: key points ----------------
        head = section_title(self, "1  Key points")
        bullet_list(self, ["Definition", "Components", "How it works"],
                    cues=[self.cue(2, "التَّعْرِيفُ"), self.cue(2, "المُكَوِّنَاتُ"),
                          self.cue(2, "طَرِيقَةُ")])
        self.sync(self.end(2) - 0.6)
        self.clear(head)

        # ---------------- Segment 3: worked example ----------------
        section_title(self, "2  Worked example", prev=head)
        worked_calculation(self, ["t", "=", "V", "÷", "Q"],
                           ["=", f"{D.VOLUME:.2f} m³", "÷", f"{D.FLOW_RATE:.1f} m³/h"],
                           f"= {D.FILL_TIME:.1f} s",
                           cues=[self.cue(3, "إِذَا"), self.cue(3, "وَالتَّدَفُّقُ"),
                                 self.cue(3, "فَزَمَنُ")])
        self.sync(self.end(3) - 0.6)
        self.clear()

        # ---------------- Segment 4: summary ----------------
        summary_box(self, "Summary", ["The idea", "The components", "A simple example"],
                    cues=[self.cue(4, "الفِكْرَةَ"), self.cue(4, "وَالمُكَوِّنَاتِ"),
                          self.cue(4, "وَحَسَبْنَا")])
        self.sync(self.end(4) + 1.0)


if __name__ == "__main__":
    main(__file__, "NAMEEp01", NARRATION)
