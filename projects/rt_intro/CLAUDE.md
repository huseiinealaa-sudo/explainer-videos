# Project: rt_intro — Industrial radiography: principle and geometric unsharpness (single video)

Project-specific rules. The general rules in the root `CLAUDE.md` also apply; where they differ, this file wins for this project.

## Video
- One episode, about 4:10 (measured narration 4:29), six segments; storyboard in `storyboard/rt_intro_principle.md`.
- Script `projects/rt_intro/rt_intro_principle.py` → `output/rt_intro_principle.mp4` (build folder `tmp/rt_intro_principle/`).
- Drawings before text: segments 1–5 each have a custom animated drawing made from scratch in code; no images copied from the sources.

## Source and verification
- Primary reference: `sources/rt_intro_source.md` (the owner's cleaned source, kept verbatim).
- Official sources first (priority 1): IAEA Training Course Series No. 3, *Industrial Radiography* (manual for the syllabi of IAEA-TECDOC-628, 1992) for the principle and the sources; ASME BPVC Section V, Article 2, T-274 for Ug, its symbols and limits.
- Where the cleaned source differs from an official source, the narration follows the official source and the correction is listed (claim, correction, source with page or paragraph) in `sources/rt_intro_principle.md`.
- Research only verifies: nothing is added except to correct an error or fill a gap the explanation needs.

## Narration
- Arabic, ar-SA-HamedNeural, normal speed (`project.toml`); fully diacritized.
- Foreign terms written in Arabic letters:
  | Term | Narration spelling |
  |---|---|
  | RT | آرْ تِي |
  | Ug | يُو جِي |
  | F | إِفْ |
  | d / D | دِي الصَّغِيرَةُ / دِي الكَبِيرَةُ |
  | kV | الكِيلُوفُولْت |
  | Ir-192 | الإِيرِيدْيُوم مِئَةٍ وَاثْنَيْنِ وَتِسْعِينَ |
  | Tungsten | التَّنْغِسْتِن |
  | ASME | أَزْمِي |
- Terminology: شِبْهُ الظِّلِّ = penumbra; عَدَمُ الوُضُوحِ الهَنْدَسِيِّ = geometric unsharpness; البُقْعَةُ البُؤْرِيَّةُ = focal spot; جِهَةُ المَصْدَرِ فِي القِطْعَةِ = source side of the object.

## Terminology and on-screen conventions
- On screen: English labels and equations only.
- D = source → source side of the object; d = source side of the object → film (ASME V T-274.1).
- Colours: ACCENT_1 = radiation (rays, beam), ACCENT_2 = the source (focal spot, capsule, size F), ACCENT_3 = within the limit, ACCENT_4 = defects and out of limit.
- Film darkness in grey: darker = more radiation reached the film.

## Data
- All numbers come from `projects/rt_intro/rt_intro_data.py`, which runs `self_test()` on import.
- Illustrative inputs:
  | Item | Value |
  |---|---|
  | F (source size) | 3.0 mm |
  | d (source side → film, film in contact) | 20.0 mm |
  | D1 / D2 | 400.0 / 200.0 mm |
  | Ug limit (illustrative; ASME V recommended maximum for thickness under 2 in) | 0.51 mm |
  | Ir-192 half-life (published, approximate) | 74 days |

## Owner decisions
- 2026-09-27: project created; single episode, six segments, storyboard as in the request; left out: radiation safety, inverse square law, source decay, IQI, film density, digital radiography, defect interpretation.
