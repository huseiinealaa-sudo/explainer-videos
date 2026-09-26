"""svp_winsfc: the Calibron Small Volume Prover and WinSFC for the SFC332P (one video, ~14:30).

First half: the prover (Honeywell Enraf Calibron SVP and its SVP Controller); second half:
WinSFC with the Dynamic Flow Computers SFC332P; then a short wrap-up. Sources and the
owner's decisions: sources/svp_winsfc_full.md and CLAUDE.md in this folder.

Build (from the repo root):
    python projects/svp_winsfc/svp_winsfc_full.py --preview   # 480p15 -> tmp/svp_winsfc_full/preview.mp4
    python projects/svp_winsfc/svp_winsfc_full.py             # 1080p30 -> output/svp_winsfc_full.mp4
"""
from explainer import *
import svp_winsfc_data as D

# Fully diacritized narration (owner-approved 2026-09-26) — one entry per segment.
NARRATION = [
    # 1 what an SVP is, why small, the system
    "هٰذِهِ مَادَّةٌ تَعْلِيمِيَّةٌ؛ وَالمَرْجِعُ المُلْزِمُ هُوَ الوَثَائِقُ الرَّسْمِيَّةُ وَالإِجْرَاءَاتُ المُعْتَمَدَةُ. البُرُوفَرُ وِعَاءٌ حَجْمُهُ مَعْرُوفٌ بِدِقَّةٍ: يَمُرُّ المُنْتَجُ نَفْسُهُ فِي العَدَّادِ ثُمَّ فِي البُرُوفَرِ، فَيَدْفَعُ السَّائِلُ مِكْبَسًا بَيْنَ كَاشِفَيْنِ. نَعْرِفُ الحَجْمَ المُزَاحَ، وَنَعُدُّ نَبَضَاتِ العَدَّادِ فِي المُدَّةِ نَفْسِهَا، وَالنِّسْبَةُ بَيْنَهُمَا هِيَ مُعَامِلُ العَدَّادِ. وَيُصَنِّفُهُ دَلِيلُهُ بُرُوفَرَ إِزَاحَةٍ بِمِكْبَسٍ، يَقِيسُ فِي اتِّجَاهٍ وَاحِدٍ. وَهُوَ صَغِيرُ الحَجْمِ لِأَنَّ البُرُوفَرَ الكَبِيرَ، وَهُوَ أُنْبُوبِيٌّ عَادَةً، يَحْتَاجُ أَكْثَرَ مِنْ عَشَرَةِ آلَافِ نَبْضَةٍ لِيُخْرِجَ المُعَامِلَ، أَمَّا هٰذَا فَيُخْرِجُهُ بِأَقَلَّ مِنْهَا، بِفَضْلِ الكْرُونُومِتْرِي المُزْدَوِجِ. وَالمَنْظُومَةُ أَرْبَعَةُ أَطْرَافٍ: البُرُوفَرُ يَرْسُمُ الحَجْمَ، وَالعَدَّادُ يَعُدُّ النَّبَضَاتِ، وَالحَاسِبَةُ تُقَارِنُ وَتُصَحِّحُ وَتَتَحَكَّمُ، وَبَرْنَامَجُ وِين إِسْ إِفْ سِي نَافِذَةُ المُهَنْدِسِ عَلَى الحَاسِبَةِ.",
    # 2 mechanical layout
    "أُنْبُوبُ التَّدَفُّقِ مَصْقُولٌ، وَتَجْوِيفُهُ مَطْلِيٌّ بِالكْرُومِ، وَفِيهِ المِكْبَسُ، وَفِي مَرْكَزِهِ صِمَامُ بُوبِت. لِلْمِكْبَسِ عَمُودٌ عَلَى كُلِّ جَانِبٍ، فَالحَجْمُ المُزَاحُ وَاحِدٌ، وَلِذٰلِكَ يَصِحُّ تَرْكِيبُ البُرُوفَرِ قَبْلَ العَدَّادِ أَوْ بَعْدَهُ. العَمُودُ الأَعْلَى يَصِلُ المِكْبَسَ بِكُتْلَةِ التَّوْجِيهِ، وَهِيَ تَسِيرُ بِعَجَلَاتٍ عَلَى قَضِيبَيْنِ، وَتَحْمِلُ العَلَمَ وَمُنْحَدَرَ الإِيقَافِ. وَيُعِيدُ المِكْبَسَ مُحَرِّكٌ وَعُلْبَةُ تُرُوسٍ وَسِلْسِلَةٌ. أَمَّا الكَاشِفَانِ الضَّوْئِيَّانِ فَخَارِجَ السَّائِلِ، فِي نِهَايَةِ القِيَادَةِ: الكَاشِفُ لَا يَرَى المِكْبَسَ، بَلْ يَرَى العَلَمَ يَقْطَعُ شُعَاعَهُ. فَهُوَ خَارِجَ السَّائِلِ، لِذٰلِكَ يَسْهُلُ فَحْصُهُ وَاسْتِبْدَالُهُ؛ وَيَسْتَجِيبُ فِي نَحْوِ خَمْسِ مِيكْرُوثَوَانٍ. وَالدَّلِيلُ يُقَرِّرُ أَنَّ اسْتِبْدَالَ كَاشِفٍ وَاحِدٍ لَا يَسْتَلْزِمُ إِعَادَةَ المُعَايَرَةِ. وَالثَّمَنُ: الكَاشِفَانِ عَلَى قَضِيبٍ مَعْدِنِيٍّ يَتَمَدَّدُ بِالحَرَارَةِ، فَلَهُ حَسَّاسُ حَرَارَةٍ وَمُعَامِلُ تَمَدُّدٍ خَاصٌّ بِهِ، إِلَى جَانِبِ حَرَارَةِ البُرُوفَرِ وَضَغْطِهِ.",
    # 3 the six stages of a pass
    "دَوْرَةُ الشَّوْطِ سِتُّ مَرَاحِلَ. فِي الانْتِظَارِ يَقِفُ المِكْبَسُ فِي أَسْفَلِ المَجْرَى، وَصِمَامُهُ مَفْتُوحٌ فَيَعْبُرُهُ السَّائِلُ. فِي السَّحْبِ تَشُدُّهُ السِّلْسِلَةُ إِلَى أَعْلَى المَجْرَى، حَتَّى يَلْمِسَ المُنْحَدَرُ مِفْتَاحَ الإِيقَافِ. فِي التَّحْرِيرِ يَنْفَصِلُ عَنِ السِّلْسِلَةِ، وَيُغْلِقُ نَابِضٌ الصِّمَامَ، فَيَصِيرُ المِكْبَسُ سَدًّا حُرًّا يَتَحَرَّكُ مَعَ السَّائِلِ. ثُمَّ التَّسَارُعُ حَتَّى تُسَاوِيَ سُرْعَتُهُ سُرْعَةَ السَّائِلِ؛ وَمَعَ عَدَّادَاتِ كُورْيُولِيس يُوصِي الدَّلِيلُ بِإِبْطَاءِ البُرُوفَرِ لِإِطَالَتِهِ. ثُمَّ القِيَاسُ: الكَاشِفُ الأَوَّلُ يُرْسِلُ نَبْضَةَ حَجْمٍ تَبْدَأُ العَدَّ، وَالثَّانِي يُوقِفُهُ، فِي أَرْبَعِ ثَوَانٍ وَنِصْفٍ فِي مِثَالِنَا. وَأَخِيرًا يُوقَفُ العَمُودُ، فَيَفْتَحُ ضَغْطُ السَّائِلِ الصِّمَامَ، وَيَسْتَمِرُّ الجَرَيَانُ بِلَا نَبْضَةِ ضَغْطٍ تُذْكَرُ. لَاحِظْ أَنَّ العَلَمَ يَعْبُرُ الكَاشِفَيْنِ فِي السَّحْبِ أَيْضًا، لٰكِنَّ نَبَضَاتِ الحَجْمِ لَا تُرْسَلُ إِلَّا فِي شَوْطِ القِيَاسِ.",
    # 4 three devices, two signals, terminals 12-17
    "البُرُوفَرُ لَا يَحْسُبُ شَيْئًا؛ فَالحِسَابُ كُلُّهُ فِي الحَاسِبَةِ. وَحَوْلَهَا ثَلَاثَةُ أَجْهِزَةٍ: العَدَّادُ يُرْسِلُ إِلَيْهَا نَبَضَاتِهِ، وَاللَّابْتُوبُ يُكَلِّمُهَا بِمُودْبَاس، وَالبُرُوفَرُ لَا يُكَلِّمُ غَيْرَهَا، وَبِإِشَارَتَيْنِ فَقَطْ: إِذْنُ التَّشْغِيلِ، رَن بِيرْمِيسِيف، مِنَ الحَاسِبَةِ، وَنَبْضَةُ الحَجْمِ، فُولْيُوم بَلْس، مِنَ المُتَحَكِّمِ عِنْدَ كُلِّ كَاشِفٍ. تَدْخُلَانِ صُنْدُوقَ تَوْصِيلِ العَمِيلِ: الطَّرَفَانِ ثَلَاثَةَ عَشَرَ وَأَرْبَعَةَ عَشَرَ لِلْإِذْنِ، وَسِتَّةَ عَشَرَ وَسَبْعَةَ عَشَرَ لِلنَّبْضَةِ، وَكِلْتَاهُمَا تَعْبُرُ عَازِلًا ضَوْئِيًّا. وَبِجَانِبِهِ صُنْدُوقُ القُدْرَةِ بِتَغْذِيَتَيْنِ مُنْفَصِلَتَيْنِ لِلْمُحَرِّكِ وَلِلْأَجْهِزَةِ، وَصُنْدُوقُ المُتَحَكِّمِ، وَتَوْصِيلَاتُهُ مِنَ المَصْنَعِ لَا تُعَدَّلُ. فَإِذَا لَمْ يَدُرِ البُرُوفَرُ، فَابْدَأْ بِالتَّغْذِيَةِ، وَكَابِلِ الرَّبْطِ، وَوَضْعِ المُتَحَكِّمِ.",
    # 5 controller modes and error messages
    "المُتَحَكِّمُ عَقْلُ البُرُوفَرِ المَحَلِّيُّ: يُشَغِّلُ المُحَرِّكَ، وَيَقْرَأُ الكَاشِفَيْنِ وَمِفْتَاحَ الإِيقَافِ، وَيُبَرْمَجُ بِجِهَازٍ يَدَوِيٍّ اسْمُهُ لَاد. وَلَهُ ثَلَاثَةُ أَوْضَاعٍ: مِيتَر كَالِيبْرِيشِن هُوَ الافْتِرَاضِيُّ، وَفِيهِ يَبْدَأُ الإِذْنُ الجَوْلَةَ. وَبْرُوفَر تِسْت لِتَجْرِبَةِ الحَرَكَةِ، وَلَا يَعْمَلُ إِلَّا فِي غِيَابِ الإِذْنِ. وَبْرُوفَر كَالِيبْرِيشِن لِلْوُوتَر دْرُو، يَتَجَاهَلُ الإِذْنَ تَمَامًا، وَيَبْقَى بَعْدَ انْقِطَاعِ الطَّاقَةِ. فَانْظُرْ شَاشَةَ الحَالَةِ قَبْلَ أَوَّلِ جَوْلَةٍ. أَمَّا رَسَائِلُ الخَطَأِ فَأَرْبَعٌ: تَسَلْسُلٌ لَمْ يَكْتَمِلْ بِالتَّرْتِيبِ المُتَوَقَّعِ، وَمِفْتَاحُ إِيقَافٍ لَمْ تَصِلْ إِشَارَتُهُ فِي المُهْلَةِ، وَكَاشِفٌ فَعَّالٌ مُنْذُ بِدَايَةِ الجَوْلَةِ، أَيِ العَلَمُ وَاقِفٌ فِيهِ، وَتَذْكِيرٌ بِالصِّيَانَةِ عِنْدَ أَلْفِ دَوْرَةٍ افْتِرَاضِيًّا. وَمُهْلَةُ المُحَرِّكِ مَضْبُوطَةٌ فِي المَصْنَعِ لِكُلِّ طِرَازٍ، فَلَا تُغَيَّرُ دُونَ اسْتِشَارَةِ الشَّرِكَةِ.",
    # 6 double chronometry and the MF chain
    "لِنَبْدَأْ بِالمُشْكِلَةِ: البَوَّابَةُ قَدْ تُفْتَحُ فِي مُنْتَصَفِ نَبْضَةٍ، وَتُغْلَقُ فِي مُنْتَصَفِ أُخْرَى. وَفِي مِثَالِنَا خَمْسَةَ عَشَرَ أَلْفَ نَبْضَةٍ، فَالنَّبْضَةُ الوَاحِدَةُ نَحْوُ سَبْعَةٍ مِنْ أَلْفٍ فِي المِئَةِ، أَيْ قُرَابَةُ سُبْعِ حَدِّ التَّكْرَارِيَّةِ. وَالحَلُّ سَاعَتَانِ: الأُولَى مِنَ الكَاشِفِ الأَوَّلِ إِلَى الثَّانِي، وَالثَّانِيَةُ مِنْ أَوَّلِ نَبْضَةٍ كَامِلَةٍ بَعْدَ الأَوَّلِ، إِلَى أَوَّلِ نَبْضَةٍ كَامِلَةٍ بَعْدَ الثَّانِي، وَنَعُدُّ فِيهَا النَّبَضَاتِ الكَامِلَةَ. وَلِأَنَّ الجَرَيَانَ ثَابِتٌ خِلَالَ ثَوَانٍ، نَضْرِبُ العَدَدَ فِي نِسْبَةِ الزَّمَنَيْنِ: فَثَمَانِيَ عَشْرَةَ نَبْضَةً تَصِيرُ ثَمَانِيَ عَشْرَةَ وَثَلَاثَةَ أَعْشَارٍ. ثُمَّ حَجْمُ البُرُوفَرِ المُصَحَّحُ: الحَجْمُ الأَسَاسِيُّ مَضْرُوبًا فِي تَصْحِيحِ حَرَارَةِ المَعْدِنِ، وَلَهُ حَدَّانِ: لِلْأُنْبُوبِ وَلِقَضِيبِ الكَاشِفَاتِ، ثُمَّ تَصْحِيحِ الضَّغْطِ، ثُمَّ تَصْحِيحِ السَّائِلِ. وَحَجْمُ العَدَّادِ: مُتَوَسِّطُ النَّبَضَاتِ مَقْسُومًا عَلَى مُعَامِلِ كَيْ، مَضْرُوبًا فِي تَصْحِيحِ السَّائِلِ عِنْدَهُ. وَالنِّسْبَةُ بَيْنَهُمَا مُعَامِلُ العَدَّادِ، وَاحِدٌ فَاصِلَةُ صِفْرٍ صِفْرٍ وَاحِدٍ اثْنَيْنِ، وَمِنْهُ مُعَامِلُ كَيْ الفِعْلِيُّ.",
    # 7 maintenance, static leak test, water draw
    "الصِّيَانَةُ عَلَى مَحَطَّاتٍ. قَبْلَ كُلِّ جَلْسَةٍ: فَحْصٌ نَظَرِيٌّ لِلْأَجْزَاءِ الحَامِلَةِ لِلضَّغْطِ، وَلِلْأَغْطِيَةِ وَأَجْهِزَةِ الأَمَانِ. شَهْرِيًّا: آلِيَّةُ الإِرْجَاعِ وَالسَّلَاسِلُ، وَقَضِيبُ الكَاشِفَاتِ، وَالكَابِلَاتُ. وَكُلَّ نِصْفِ سَنَةٍ: مِنْظَارٌ دَاخِلِيٌّ لِحَشَوَاتِ المِكْبَسِ وَالصِّمَامِ وَطَبَقَةِ الكْرُومِ. ثُمَّ اخْتِبَارُ التَّسَرُّبِ السَّاكِنِ: نَعْزِلُ البُرُوفَرَ مَمْلُوءًا، وَنَرْفَعُ الفَرْقَ عَبْرَ المِكْبَسِ إِلَى سِتَّةِ أَرْطَالٍ عَلَى البُوصَةِ المُرَبَّعَةِ، وَبَعْدَ خَمْسِ دَقَائِقَ نُرَاقِبُهُ عِشْرِينَ؛ فَهُبُوطٌ فَوْقَ الرُّبُعِ يَعْنِي تَسَرُّبًا فِي الحَشَوَاتِ. وَأَخِيرًا الوُوتَر دْرُو، أَيْ قِيَاسُ الحَجْمِ الحَقِيقِيِّ بِالمَاءِ: ثَلَاثُ سَحَبَاتٍ مُتَتَالِيَةٍ ضِمْنَ صِفْرٍ فَاصِلَةِ صِفْرٍ اثْنَيْنِ بِالمِئَةِ، إِحْدَاهَا بِجَرَيَانٍ يَخْتَلِفُ بِالرُّبُعِ، سَنَوِيًّا أَوْ بِحَسَبِ الجِهَةِ المَسْؤُولَةِ. فَالتَّكْرَارِيَّةُ المُمْتَازَةُ لَا تُثْبِتُ صِحَّةَ الحَجْمِ.",
    # 8 where WinSFC sits, Online / Offline
    "النِّصْفُ الثَّانِي: البَرْنَامَجُ. وِين إِسْ إِفْ سِي بَرْنَامَجٌ عَلَى لَابْتُوبٍ مَيْدَانِيٍّ، يَقْرَأُ إِعْدَادَ الحَاسِبَةِ وَيَكْتُبُهُ، وَيَعْرِضُ قِرَاءَاتِهَا الحَيَّةَ وَتَقَارِيرَهَا. وَهُوَ لَا يَرَى البُرُوفَرَ وَلَا العَدَّادَ، بَلْ يَرَى مَا تَقُولُهُ الحَاسِبَةُ فَقَطْ. يَتَّصِلُ بِهَا بِمُودْبَاس، مَثَلًا عَلَى مَنْفَذٍ تَسَلْسُلِيٍّ بِسُرْعَةِ تِسْعَةِ آلَافٍ وَسِتِّمِئَةِ بِتٍّ فِي الثَّانِيَةِ. وَالحَاسِبَةُ تَعْمَلُ وَتَحْسُبُ وَحْدَهَا حَتَّى لَوْ فُصِلَ اللَّابْتُوبُ، لٰكِنَّكَ تَفْقِدُ التَّشْخِيصَ وَالتَّقَارِيرَ لَحْظَتَهَا. وَفِي طَرَفِ شَرِيطِ الأَدَوَاتِ حَقْلُ حَالَةِ الاتِّصَالِ: أُونْلَايْن أَوْ أُوفْلَايْن. فِي أُوفْلَايْن تَتَعَطَّلُ قَائِمَتَا كَالِيبْرِيشِن وَأُوفَرْرَايْد، وَكُلُّ مَا تُعَدِّلُهُ مِلَفٌّ عَلَى اللَّابْتُوبِ، لَا الجِهَازُ نَفْسُهُ.",
    # 9 direction rule
    "القَاعِدَةُ الأُولَى هِيَ الاتِّجَاهُ. أَبْلُود يَنْسَخُ الإِعْدَادَ مِنَ الحَاسِبَةِ إِلَى اللَّابْتُوبِ، وَهُوَ قِرَاءَةٌ آمِنَةٌ. أَمَّا دَاوْنْلُود فَيَكْتُبُ مِلَفًّا مِنَ اللَّابْتُوبِ فَوْقَ إِعْدَادِ الحَاسِبَةِ، فَيُغَيِّرُ جِهَازَ عُهْدَةٍ يَحْسُبُ أَمْوَالًا. فَلَا دَاوْنْلُود إِلَّا بِقَرَارٍ صَرِيحٍ مِنَ المَسْؤُولِ، وَبَعْدَ ثَلَاثِ خُطُوَاتٍ: أَبْلُود جَدِيدٌ، ثُمَّ حِفْظُهُ بِاسْمٍ مُؤَرَّخٍ، ثُمَّ مُقَارَنَةُ الحُقُولِ الَّتِي سَتَتَغَيَّرُ. وَتَذَكَّرْ أَنَّ مِلَفَّاتِ الإِعْدَادِ لَقَطَاتٌ مُؤَرَّخَةٌ، قَدْ لَا تُطَابِقُ الجِهَازَ اليَوْمَ؛ وَاسْمُ المِلَفِّ فِي شَرِيطِ العُنْوَانِ يُخْبِرُكَ أَيَّ مِلَفٍّ فُتِحَ، لَا أَنَّ الجِهَازَ يُطَابِقُهُ. وَلِمَعْرِفَةِ الحَقِيقَةِ: أَبْلُود جَدِيدٌ، ثُمَّ قَارِنْ. فَقَبْلَ أَيِّ زِرٍّ اسْأَلْ نَفْسَكَ: فِي أَيِّ اتِّجَاهٍ تَسِيرُ البَيَانَاتُ؟",
    # 10 main window and menus
    "فِي أَعْلَى النَّافِذَةِ الرَّئِيسِيَّةِ شَرِيطُ العُنْوَانِ، بِاسْمِ الحَاسِبَةِ وَمِلَفِّ الإِعْدَادِ المَفْتُوحِ، وَتَحْتَهُ القَوَائِمُ. وَعَلَى الجَانِبِ الأَزْرَارُ: الاتِّصَالُ وَقَطْعُهُ، وَشَاشَةُ التَّشْخِيصِ، وَالتَّقَارِيرُ، وَمُخَطَّطُ البُرُوفَرِ، وَطَلَبُ المُعَايَرَةِ، وَلَوْحَةُ إِعْدَادِ الجِهَازِ. وَفِي هٰذِهِ اللَّوْحَةِ صَفَحَاتُ العَدَّادَاتِ، وَبَيَانَاتُ البُرُوفَرِ، وَالمَنَافِذُ، وَإِسْنَادُ المَدَاخِلِ وَالمَخَارِجِ، وَلِكُلِّ صَفْحَةٍ زِرَّا أَبْلُود وَدَاوْنْلُود خَاصَّانِ بِهَا؛ فَالخَطَرُ لَيْسَ فِي الزِّرِّ الكَبِيرِ وَحْدَهُ. ثُمَّ نُقَسِّمُ القَوَائِمَ: الآمِنُ قِرَاءَةُ التَّقَارِيرِ التَّارِيخِيَّةِ. وَالخَطِرُ قَائِمَتَانِ: كَالِيبْرِيشِن، لِأَنَّهُ يُغَيِّرُ تَحْوِيلَ الإِشَارَةِ الخَامِ إِلَى قِيمَةٍ هَنْدَسِيَّةٍ؛ وَأُوفَرْرَايْد، لِأَنَّهُ يَسْتَبْدِلُ قِرَاءَةً حَيَّةً بِقِيمَةٍ يَدَوِيَّةٍ تُحْسَبُ كَأَنَّهَا حَقِيقِيَّةٌ؛ وَأَخْطَرُ بُنُودِهِ مَحْوُ بَيَانَاتِ المُعَايَرَاتِ السَّابِقَةِ، وَمَسْحُ النِّظَامِ كُلِّهِ.",
    # 11 Prove Data
    "شَاشَةُ بْرُوف دَاتَا تُخْبِرُ الحَاسِبَةَ بِكُلِّ مَا لَا تَسْتَطِيعُ قِيَاسَهُ، فِي سِتِّ مَجْمُوعَاتٍ. هُوِيَّةُ البُرُوفَرِ، وَتُطْبَعُ فِي تَرْوِيسَةِ التَّقْرِيرِ. وَقَوَاعِدُ الجَلْسَةِ: نَوْعُ البُرُوفَرِ الَّذِي يَخْتَارُ مَنْطِقَ التَّسَلْسُلِ، وَالطَّرِيقَةُ الحَجْمِيَّةُ، وَعَدَدُ الجَوْلَاتِ لِلْمُتَوَسِّطِ، وَأَقْصَى عَدَدٍ لَهَا، وَحَدُّ التَّكْرَارِيَّةِ، وَمُهْلَةُ الإِلْغَاءِ. ثُمَّ الحَجْمُ وَالهَنْدَسَةُ: الحَجْمُ المَرْجِعِيُّ مِنْ آخِرِ وُوتَر دْرُو، وَالقُطْرُ، وَسُمْكُ الجِدَارِ، وَمُعَامِلُ المُرُونَةِ، وَالثَّلَاثَةُ الأَخِيرَةُ تَدْخُلُ فِي تَصْحِيحِ الضَّغْطِ. ثُمَّ المُعَامِلَاتُ الحَرَارِيَّةُ لِلْأُنْبُوبِ وَلِلْقَضِيبِ، وَحَرَارَةُ الأَسَاسِ، خَمْسَ عَشْرَةَ دَرَجَةً فِي مِثَالِنَا. ثُمَّ فُحُوصُ الاسْتِقْرَارِ، وَأَخِيرًا إِعْدَادَاتُ الكَاشِفِ وَقُطْبِيَّةُ الإِشَارَاتِ. وَانْتَبِهْ: رَقْمٌ خَاطِئٌ هُنَا خَطَأٌ مَنْهَجِيٌّ فِي كُلِّ جَلْسَةٍ، وَلَا يَظْهَرُ فِي التَّكْرَارِيَّةِ، لِأَنَّ كُلَّ الجَوْلَاتِ تُحْسَبُ بِهِ.",
    # 12 Diagnostic and three mental checks
    "شَاشَةُ التَّشْخِيصِ تَعْرِضُ فِي تَرْوِيسَتِهَا عُنْوَانَ الحَاسِبَةِ، وَتَرَدُّدَ نَبَضَاتِ العَدَّادِ الحَيَّ، وَحَالَةَ المَدَاخِلِ وَالمَخَارِجِ الرَّقْمِيَّةِ. وَفِي جَدْوَلِهَا لِكُلِّ قَنَاةٍ: الإِشَارَةُ الخَامُ، وَالقِيمَةُ الهَنْدَسِيَّةُ، وَفِيل كُود، وَهُوَ اخْتِيَارُ سُلُوكِ القَنَاةِ لَا رَمْزُ عُطْلٍ: صِفْرٌ يَعْنِي القِرَاءَةَ الحَيَّةَ دَائِمًا، وَوَاحِدٌ القِيمَةَ البَدِيلَةَ دَائِمًا، وَاثْنَانِ البَدِيلَةَ عِنْدَ فَشَلِ الإِشَارَةِ. ثُمَّ ثَلَاثَةُ فُحُوصٍ ذِهْنِيَّةٍ: التَّرَدُّدُ مَضْرُوبًا فِي ثَلَاثَةِ آلَافٍ وَسِتِّمِئَةٍ، مَقْسُومًا عَلَى مُعَامِلِ كَيْ، يُعْطِي مِئَتَيْ مِتْرٍ مُكَعَّبٍ فِي السَّاعَةِ، فَقَارِنْهُ بِشَاشَةِ المُرْسِلَةِ. وَمُقَاوَمَةُ مِئَةٍ وَخَمْسَةَ عَشَرَ فَاصِلَةِ خَمْسَةٍ أَرْبَعَةٍ أُومٍ تُقَابِلُ أَرْبَعِينَ دَرَجَةً بِالمُعَادَلَةِ القِيَاسِيَّةِ، وَالتَّقْرِيبُ الخَطِّيُّ لِلتَّحَقُّقِ السَّرِيعِ فَقَطْ. وَالقِيمَةُ المُسْتَدِيرَةُ، كَكَثَافَةِ سَبْعِمِئَةٍ تَمَامًا، بَدِيلَةٌ حَتَّى يَثْبُتَ العَكْسُ.",
    # 13 Status Input / Switch Output
    "فِي نَافِذَةِ سْتَاتَس إِنْبُت وَسْوِتْش أَوْتْبُت تُعَيَّنُ وَظِيفَةُ كُلِّ طَرَفٍ رَقْمِيٍّ فِي الحَاسِبَةِ. المَدَاخِلُ تَسْتَقْبِلُ أَوَامِرَ مِنَ الخَارِجِ، كَطَلَبِ المُعَايَرَةِ أَوْ جَاهِزِيَّةِ البُرُوفَرِ. وَالمَخَارِجُ تُخْبِرُ الخَارِجَ أَوْ تَأْمُرُهُ: أَطْلِقِ البُرُوفَرَ، وَالمُعَايَرَةُ جَارِيَةٌ، أَوِ اكْتَمَلَتْ، أَوْ أُلْغِيَتْ. وَالرَّقْمُ فِي كُلِّ خَانَةٍ يَخْتَارُ الوَظِيفَةَ؛ فَالحَاسِبَةُ عَامَّةُ الاسْتِعْمَالِ، وَتَغْيِيرُ الرَّقْمِ يُغَيِّرُ مَعْنَى السِّلْكِ دُونَ لَمْسِهِ. فَإِذَا كَانَتْ وَظِيفَةُ الطَّرَفِ المَوْصُولِ بِالمُتَحَكِّمِ خَاطِئَةً، لَمْ يَصِلِ الطَّلَبُ، وَلَمْ يَتَحَرَّكِ المِكْبَسُ، مَعَ أَنَّ كُلَّ مَا عَدَاهُ سَلِيمٌ. وَقَدْ يَمْحُو الإِسْنَادَ العَامِلَ دَاوْنْلُود مِنْ مِلَفٍّ أَقْدَمَ؛ فَاحْفَظْ نُسْخَةً مِنْ مِلَفِّ الإِعْدَادِ العَامِلِ فِي مَكَانَيْنِ خَارِجَ اللَّابْتُوبِ.",
    # 14 proving sequence and checklist
    "الآنَ نَرْبِطُ الصُّورَةَ: يُطْلِقُ المُهَنْدِسُ طَلَبَ المُعَايَرَةِ، فَتَقْرَأُ الحَاسِبَةُ عَدَدَ الجَوْلَاتِ وَحَدَّ التَّكْرَارِيَّةِ، وَتَرْفَعُ إِذْنَ التَّشْغِيلِ. يُسْحَبُ المِكْبَسُ وَيُحَرَّرُ، فَتَصِلُ نَبْضَةُ الحَجْمِ الأُولَى، وَتُعَدُّ النَّبَضَاتُ وَتُوَقَّتُ حَتَّى النَّبْضَةِ الثَّانِيَةِ. وَتَتَكَرَّرُ الجَوْلَاتُ حَتَّى تَتَّفِقَ خَمْسُ جَوْلَاتٍ مُتَتَالِيَةٍ ضِمْنَ الحَدِّ، أَوْ يَنْفَدَ أَقْصَى عَدَدِهَا. وَالتَّكْرَارِيَّةُ هِيَ الفَرْقُ بَيْنَ أَعْلَى جَوْلَةٍ وَأَدْنَاهَا مَقْسُومًا عَلَى الأَدْنَى، وَفِي مِثَالِنَا صِفْرٌ فَاصِلَةُ صِفْرٍ وَاحِدٍ ثَمَانِيَةٍ سَبْعَةٍ بِالمِئَةِ، ضِمْنَ حَدِّ صِفْرٍ فَاصِلَةِ صِفْرٍ خَمْسَةٍ. ثُمَّ يَخْرُجُ مُعَامِلُ العَدَّادِ وَالتَّقْرِيرُ. وَقَبْلَ الطَّلَبِ قَائِمَةٌ قَصِيرَةٌ: عَدَّادٌ وَاحِدٌ فِي العَمَلِيَّةِ وَالآخَرُ مَعْزُولٌ. المُتَحَكِّمُ فِي مِيتَر كَالِيبْرِيشِن. العَدَّادُ المَقْصُودُ بِوَسْمِهِ وَخَطِّهِ، لَا بِرَقْمِهِ التَّسَلْسُلِيِّ. التَّرَدُّدُ قَرِيبٌ مِنْ شَاشَةِ المُرْسِلَةِ. كُلُّ القَنَوَاتِ حَيَّةٌ. الجَوْلَاتُ وَالحَدُّ مَضْبُوطَةٌ. وَالحَرَارَةُ مُسْتَقِرَّةٌ.",
    # 15 troubleshooting and golden rules
    "وَعِنْدَ العُطْلِ لَا تَبْدَأْ مِنَ البُرُوفَرِ، بَلْ مِنَ التَّسَلْسُلِ: حَدِّدْ آخِرَ خُطْوَةٍ نَجَحَتْ، فَالعُطْلُ فِي الَّتِي تَلِيهَا. وَالقَوَاعِدُ الذَّهَبِيَّةُ: أَبْلُود آمِنٌ وَدَاوْنْلُود قَرَارٌ. المُتَحَكِّمُ فِي مِيتَر كَالِيبْرِيشِن قَبْلَ أَوَّلِ جَوْلَةٍ. افْحَصْ فِيل كُود وَلَوْ قَالَتِ الإِنْذَارَاتُ لَا شَيْءَ. تَكْرَارِيَّةٌ صِفْرِيَّةٌ مَعَ جَوْلَةٍ وَاحِدَةٍ إِنْذَارٌ لَا جَوْدَةٌ. احْفَظْ مِلَفَّ الإِعْدَادِ خَارِجَ اللَّابْتُوبِ. التَّكْرَارِيَّةُ الجَيِّدَةُ لَا تُثْبِتُ صِحَّةَ الحَجْمِ. وَالسَّلَامَةُ قَبْلَ ذٰلِكَ كُلِّهِ: لَا تَشْغِيلَ دُونَ الأَغْطِيَةِ، وَارْفَعِ الضَّغْطَ بِبُطْءٍ، وَفَرِّغْهُ قَبْلَ أَيِّ فَكٍّ. وَاعْتِمَادُ مُعَامِلِ العَدَّادِ لِلْمُهَنْدِسِ المَسْؤُولِ وَالتَّوْثِيقِ الرَّسْمِيِّ.",
]

# Every spoken or shown value is checked against the data module; stop if it drifts.
assert D.LARGE_PROVER_PULSES == 10000                                       # seg 1
assert D.DETECTOR_RESPONSE_US == 5                                          # seg 2
assert f"{D.SWEEP_TIME:.1f}" == "4.5"                                       # seg 3
assert [t for t, _ in D.CCB_TERMINALS][1:3] == [13, 14]                     # seg 4
assert [t for t, _ in D.CCB_TERMINALS][4:6] == [16, 17]
assert D.SERVICE_DUE_CYCLES == 1000                                         # seg 5
assert D.NOMINAL_PULSES == 15000 and f"{D.PULSE_FRACTION_PCT:.3f}" == "0.007"  # seg 6
assert D.CHRONO_N == 18 and f"{D.CHRONO_INTERP:.1f}" == "18.3"
assert f"{D.MF:.4f}" == "1.0012"
assert (D.LEAK_DP_PSID, D.LEAK_SETTLE_MIN, D.LEAK_WATCH_MIN) == (6, 5, 20)  # seg 7
assert D.LEAK_MAX_DROP_PCT == 25 and D.WD_FLOW_CHANGE_PCT == 25
assert D.WD_MIN_DRAWS == 3 and D.WD_REPEAT_PCT == 0.02 and D.WD_INTERVAL_YEARS == 1
assert D.BAUD_EXAMPLE == 9600                                               # seg 8
assert D.T_BASE == 15.0                                                     # seg 11
assert f"{D.Q_FROM_FREQ:.0f}" == "200" and D.PT100_R == 115.54             # seg 12
assert f"{D.PT100_T_CVD:.0f}" == "40" and D.DENSITY_SUSPECT == 700.0
assert D.RUNS_TO_AVERAGE == 5 and f"{D.REPEATABILITY:.4f}" == "0.0187"     # seg 14
assert D.REPEATABILITY_LIMIT == 0.050

AUDIO_DIR = audio_dir_for(__file__)

# Colours (project CLAUDE.md): prover/fluid, meter/pulses/flow computer, OK/safe, alarm.
PROVER_C, METER_C = ACCENT_1, ACCENT_2
SMALL = FS_TAG


def box(text, w, h, color=INK, size=FS_TAG - 2, fill=None, font=FONT):
    r = Rectangle(width=w, height=h, stroke_width=3, color=color)
    if fill:
        r.set_fill(fill, 1)
    t = Text(text, font_size=size, color=color, font=font)
    if t.width > w - 0.15:
        t.scale_to_fit_width(w - 0.15)
    return VGroup(r, t.move_to(r))


class SvpWinsfcFull(SyncedScene):
    def construct(self):
        self.timeline(NARRATION, AUDIO_DIR)
        self.head = None
        for seg in range(1, len(NARRATION) + 1):
            getattr(self, f"seg{seg}")(seg)
            self.sync(self.end(seg) - 0.6)
            if seg < len(NARRATION):
                self.clear(self.head)
        self.sync(self.end(len(NARRATION)) + 1.0)

    # ---------------- helpers ----------------
    def c(self, seg, phrase, nth=1):
        return self.cue(seg, phrase, nth)

    def heading(self, text):
        if self.head is None:
            self.head = section_title(self, text)
        else:
            section_title(self, text, prev=self.head)

    @staticmethod
    def anchor():
        """Invisible drawing for a later batch of labeled_diagram callouts."""
        return Dot(radius=0.001).set_opacity(0)

    def part(self, text, hold=1.2):
        self.heading(text)
        self.wait(hold)

    # ================= Part A: the prover =================
    def seg1(self, s):
        title_card(self, "Calibron Small Volume Prover & WinSFC",
                   "The SVP, its controller and the SFC332P flow computer",
                   series="Honeywell Enraf  ·  Dynamic Flow Computers  ·  educational")
        self.say("Educational material — the binding reference is the official documentation",
                 GREY_INK)
        self.sync(self.c(s, "البُرُوفَرُ وِعَاءٌ") - 0.6)
        self.clear()
        self.part("Part A  ·  The prover")
        self.heading("A1  What an SVP is")
        self.say("A known volume: the product pushes a piston between two detectors", PROVER_C)
        self.sync(self.c(s, "وَالنِّسْبَةُ بَيْنَهُمَا"))
        eq = equation(self, ["MF", "=", "prover volume", "÷", "meter volume"],
                      colors={0: ACCENT_3, 2: PROVER_C, 4: METER_C}, pos=UP * 1.6)
        self.sync(self.c(s, "وَيُصَنِّفُهُ"))
        self.say("Small Volume Unidirectional Piston Displacement Prover", GREY_INK)
        bullet_list(self, [f"Large (pipe) prover: more than {D.LARGE_PROVER_PULSES:,} pulses for an MF",
                           "SVP: fewer pulses, thanks to double chronometry"],
                    cues=[self.c(s, "لِأَنَّ البُرُوفَرَ الكَبِيرَ"), self.c(s, "أَمَّا هٰذَا")],
                    pos=DOWN * 0.4, size=FS_LABEL)
        self.sync(self.c(s, "وَالمَنْظُومَةُ") - 0.5)
        self.clear(self.head)
        concept_map(self, "Proving system",
                    ["Prover\ndefines the volume", "Meter (Coriolis)\ncounts pulses",
                     "SFC332P flow computer\ncompares · corrects · controls",
                     "WinSFC\nengineer's window"],
                    cues=[self.c(s, "البُرُوفَرُ يَرْسُمُ"), self.c(s, "وَالعَدَّادُ يَعُدُّ"),
                          self.c(s, "وَالحَاسِبَةُ تُقَارِنُ"), self.c(s, "وَبَرْنَامَجُ")],
                    colors=[PROVER_C, METER_C, METER_C, ACCENT_3], radius=(4.4, 2.2),
                    pos=DOWN * 0.1)

    def prover_drawing(self):
        tube = Rectangle(width=6.6, height=1.2, stroke_width=4, color=PROVER_C)
        tube.set_fill(PROVER_C, 0.08).move_to([0.3, 0, 0])
        fl_up = Rectangle(width=0.18, height=1.7, stroke_width=3).move_to([-3.0, 0, 0])
        fl_dn = Rectangle(width=0.18, height=1.7, stroke_width=3).move_to([3.6, 0, 0])
        piston = Rectangle(width=0.4, height=1.12, stroke_width=3, color=INK)
        piston.set_fill(LIGHT_INK, 1).move_to([0.9, 0, 0])
        poppet = Circle(radius=0.2, stroke_width=3, color=INK).set_fill(BG, 1).move_to(piston)
        shaft_up = Line([-5.1, 0, 0], [0.7, 0, 0], stroke_width=5)
        shaft_dn = Line([1.1, 0, 0], [5.0, 0, 0], stroke_width=5)
        cover = VGroup(DashedVMobject(Rectangle(width=3.4, height=3.0).move_to([-4.95, 0, 0]),
                                      num_dashes=40, color=GREY_INK))
        bars = VGroup(Line([-6.4, 0.7, 0], [-3.4, 0.7, 0], stroke_width=4, color=GREY_INK),
                      Line([-6.4, -0.7, 0], [-3.4, -0.7, 0], stroke_width=4, color=GREY_INK))
        block = Rectangle(width=0.7, height=1.2, stroke_width=3).set_fill(PANEL_FILL, 1)
        block.move_to([-5.1, 0, 0])
        cams = VGroup(*[Circle(radius=0.1, stroke_width=2).set_fill(BG, 1).move_to([-5.1 + dx, y, 0])
                        for dx in (-0.22, 0.22) for y in (0.6, -0.6)])
        flag = Rectangle(width=0.12, height=0.75, stroke_width=0).set_fill(ACCENT_2, 1)
        flag.next_to(block, UP, buff=0).shift(UP * 0.12)
        ramp = Polygon([-5.45, -0.6, 0], [-4.75, -0.6, 0], [-4.75, -0.95, 0], stroke_width=3)
        det_bar = Line([-6.4, 1.28, 0], [-3.4, 1.28, 0], stroke_width=6, color=INK)
        dets = VGroup(*[VGroup(Rectangle(width=0.36, height=0.5, stroke_width=3, color=ACCENT_3)
                               .set_fill(BG, 1).move_to([x, 1.28, 0]))
                        for x in (-5.9, -4.2)])
        motor = box("M", 0.9, 0.6, size=FS_TAG).move_to([-6.0, -1.15, 0])
        chain = DashedLine([-5.55, -1.15, 0], [-3.6, -1.15, 0], stroke_width=3, color=GREY_INK)
        flow = Arrow([4.2, 0.9, 0], [5.6, 0.9, 0], buff=0, stroke_width=4, color=PROVER_C,
                     max_tip_length_to_length_ratio=0.25)
        flow_t = label("flow", FS_TAG, PROVER_C).next_to(flow, UP, 0.05)
        g = VGroup(tube, fl_up, fl_dn, shaft_up, shaft_dn, piston, poppet, cover, bars, block,
                   cams, flag, ramp, det_bar, dets, motor, chain, flow, flow_t)
        parts = dict(tube=tube, piston=piston, shaft_dn=shaft_dn, block=block, flag=flag,
                     motor=motor, dets=dets, det_bar=det_bar)
        return g, parts

    def seg2(self, s):
        self.heading("A2  Mechanical layout")
        g, p = self.prover_drawing()
        g.move_to(UP * 0.35)
        callouts = [("Flow tube, chrome-plated bore", p["tube"], UP),
                    ("Piston + poppet valve", p["piston"], DOWN),
                    ("A shaft on each side", p["shaft_dn"], DOWN),
                    ("Guide block on bars", p["block"], DOWN),
                    ("Flag + motor stop ramp", p["flag"], UP),
                    ("Motor · gearbox · chain", p["motor"], DOWN),
                    ("Optical detectors", p["dets"], UP),
                    ("Detector bar: Td + Gl", p["det_bar"], UR)]
        labeled_diagram(self, g, callouts[:3],
                        cues=[self.c(s, "أُنْبُوبُ التَّدَفُّقِ"), self.c(s, "وَفِيهِ المِكْبَسُ"),
                              self.c(s, "لِلْمِكْبَسِ عَمُودٌ")], draw_time=1.6)
        self.sync(self.c(s, "وَلِذٰلِكَ يَصِحُّ"))
        self.say("Same displaced volume both ways → upstream or downstream of the meter", GREY_INK)
        labeled_diagram(self, self.anchor(), callouts[3:7],
                        cues=[self.c(s, "بِكُتْلَةِ التَّوْجِيهِ"), self.c(s, "وَتَحْمِلُ العَلَمَ"),
                              self.c(s, "وَيُعِيدُ المِكْبَسَ"), self.c(s, "أَمَّا الكَاشِفَانِ")],
                        draw_time=0.05, start=4)
        self.sync(self.c(s, "بَلْ يَرَى العَلَمَ"))
        self.play(Indicate(p["flag"], color=ACCENT_2, scale_factor=1.4), run_time=1.0)
        self.sync(self.c(s, "فَهُوَ خَارِجَ"))
        self.say(f"Outside the liquid: easy to check and replace  ·  ~{D.DETECTOR_RESPONSE_US} µs"
                 f"  ·  ±{D.DETECTOR_REPEAT_PCT}%", ACCENT_3)
        self.sync(self.c(s, "وَالدَّلِيلُ يُقَرِّرُ"))
        self.say("One detector replaced → no recalibration (manual)", ACCENT_3)
        labeled_diagram(self, self.anchor(), callouts[7:], cues=[self.c(s, "وَالثَّمَنُ")],
                        draw_time=0.05, start=8)
        self.say("Detector bar expands with heat → own temperature (Td) and coefficient (Gl)",
                 ALERT_C)

    def seg3(self, s):
        self.heading("A3  The six stages of a pass")
        stages = ["Standby", "Retract", "Release", "Run-up", "Measure", "Stop"]
        chart = line_chart(self, D.CYCLE_T, D.CYCLE_POS, x_label="time (s)",
                           y_label="piston position (%)", x_range=[0, 22, 2],
                           y_range=[0, 100, 25], size=(8.8, 3.3), pos=UP * 0.95 + LEFT * 0.6,
                           color=PROVER_C, run_time=1.5, decimals=0)
        ax = chart[0]
        dlines = VGroup()
        for pos, name in ((D.DET_UP_POS, "upstream detector"), (D.DET_DN_POS, "downstream detector")):
            ln = DashedLine(ax.c2p(0, pos), ax.c2p(22, pos), stroke_width=2, color=ACCENT_3)
            tx = label(name, FS_TAG - 2, ACCENT_3).next_to(ln, RIGHT, 0.1)
            dlines.add(VGroup(ln, tx))
        self.play(FadeIn(dlines), run_time=0.6)
        bar = stage_bar(self, stages, active=0, y=-2.55)
        dot = Dot(ax.c2p(D.CYCLE_T[0], D.CYCLE_POS[0]), radius=0.12, color=ALERT_C)
        self.play(FadeIn(dot, scale=1.5), run_time=0.4)
        cues = ["فِي الانْتِظَارِ", "فِي السَّحْبِ", "فِي التَّحْرِيرِ", "ثُمَّ التَّسَارُعُ",
                "ثُمَّ القِيَاسُ", "وَأَخِيرًا يُوقَفُ"]
        # point index reached at the end of each stage
        ends = [1, 2, 2, 3, 4, 5]
        for k, (cu, e) in enumerate(zip(cues, ends)):
            if k:
                self.sync(self.c(s, cu))
                set_stage(self, bar, k)
            if k == 4:
                seg_line = Line(ax.c2p(D.CYCLE_T[3], D.CYCLE_POS[3]),
                                ax.c2p(D.CYCLE_T[4], D.CYCLE_POS[4]), stroke_width=9, color=ACCENT_3)
                sweep = label(f"{D.SWEEP_TIME:.1f} s", FS_LABEL, ACCENT_3, weight=BOLD)
                sweep.next_to(seg_line.get_center(), RIGHT, 0.25)
                self.play(dot.animate.move_to(ax.c2p(D.CYCLE_T[e], D.CYCLE_POS[e])),
                          Create(seg_line), FadeIn(sweep), run_time=2.0)
            elif k == 0:
                self.play(dot.animate.move_to(ax.c2p(D.CYCLE_T[e], D.CYCLE_POS[e])), run_time=0.6)
            elif k == 2:
                self.play(Flash(dot, color=ALERT_C), run_time=0.6)
            else:
                self.play(dot.animate.move_to(ax.c2p(D.CYCLE_T[e], D.CYCLE_POS[e])), run_time=1.2)
            if k == 1:
                self.say("Chain pulls the piston until the ramp hits the motor stop switch", GREY_INK)
            if k == 2:
                self.say("Released: the spring closes the poppet, the piston moves with the liquid",
                         GREY_INK)
            if k == 3:
                self.say("Coriolis meters: slow the prover to lengthen the run-up", GREY_INK)
            if k == 4:
                self.say(f"Detector 1 → volume pulse ({D.VOLUME_PULSE_MS} ms) starts the count; "
                         "detector 2 stops it", ACCENT_3)
            if k == 5:
                self.say("Shaft stopped → pressure opens the poppet → flow goes on, no surge",
                         GREY_INK)
        self.sync(self.c(s, "لَاحِظْ"))
        crosses = VGroup()
        t1, t2 = D.CYCLE_T[1], D.CYCLE_T[2]
        for pos in (D.DET_DN_POS, D.DET_UP_POS):
            t = t1 + (t2 - t1) * pos / 100
            crosses.add(label("✗", FS_LABEL, ALERT_C, weight=BOLD).move_to(ax.c2p(t, pos)))
        self.play(FadeIn(crosses, scale=1.6), run_time=0.6)
        self.say("Retract: the flag crosses both detectors — no volume pulse", ALERT_C)

    def seg4(self, s):
        self.heading("A4  Three devices, two signals")
        cmap = concept_map(self, "SFC332P\nflow computer",
                           ["Meter", "Laptop · WinSFC", "Prover controller"],
                           links=["pulses (Freq#1)", "Modbus", "Run Permissive / Volume Pulse"],
                           cues=[self.c(s, "العَدَّادُ يُرْسِلُ"), self.c(s, "وَاللَّابْتُوبُ"),
                                 self.c(s, "وَالبُرُوفَرُ لَا يُكَلِّمُ")],
                           colors=[METER_C, ACCENT_3, PROVER_C], radius=(4.3, 2.3), pos=UP * 0.3)
        self.say("The prover computes nothing: all calculation is in the flow computer", GREY_INK)
        self.sync(self.c(s, "رَن بِيرْمِيسِيف"))
        self.say("Run Permissive: flow computer → controller   ·   Volume Pulse: controller → "
                 "flow computer", PROVER_C)
        self.sync(self.c(s, "تَدْخُلَانِ") - 0.3)
        self.play(FadeOut(self.caption), cmap.animate.scale(0.55).move_to([-4.2, 0.6, 0]),
                  run_time=0.8)
        self.caption = VMobject()
        rows = [[str(t), n] for t, n in D.CCB_TERMINALS]
        c1, c2 = self.c(s, "الطَّرَفَانِ ثَلَاثَةَ"), self.c(s, "وَسِتَّةَ عَشَرَ")
        tab = data_table(self, ["CCB", "Customer Connection Box"], rows,
                         cues=[c1, c1, c1, c2, c2, c2], pos=[2.6, 0.9, 0], size=FS_TAG,
                         width=8.0)
        note = label("SFC332P switch outputs: open collector, external DC supply", FS_TAG - 2,
                     GREY_INK).next_to(tab, DOWN, 0.3)
        self.play(FadeIn(note), run_time=0.4)
        self.sync(self.c(s, "وَكِلْتَاهُمَا"))
        self.say(f"Both cross an optical isolator  ·  {D.LIMIT_RESISTOR_OHM} Ω at 12–24 VDC, "
                 "jumper at 6–12 VDC", ACCENT_3)
        self.sync(self.c(s, "وَبِجَانِبِهِ"))
        self.say("Power Box: motor + clean instrument supply  ·  Controller Box: factory wiring",
                 GREY_INK)
        self.sync(self.c(s, "فَإِذَا لَمْ يَدُرِ"))
        self.say("Prover does not cycle?  power  →  interface cable  →  controller mode", ALERT_C)

    def seg5(self, s):
        self.heading("A5  Controller: modes and errors")
        self.say("Runs the motor, reads the detectors and stop switch · programmed with the LAD",
                 GREY_INK)
        comparison(self, ("Meter Calibration", "default mode", "Run Permissive starts a run",
                          "daily meter proving"),
                   ("Test / Calibration", "Prover Test: only without Run Permissive",
                    "Prover Calibration: water draw", "ignores Run Permissive,",
                    "kept after a power loss"),
                   colors=(ACCENT_3, GREY_INK), verdict="left", pos=UP * 0.6,
                   cues=[self.c(s, "مِيتَر كَالِيبْرِيشِن"), self.c(s, "وَبْرُوفَر تِسْت"),
                         self.c(s, "فَانْظُرْ")])
        self.say("Look at the Prover Status screen before the first run", ACCENT_3)
        self.sync(self.c(s, "أَمَّا رَسَائِلُ") - 0.3)
        self.clear(self.head)
        rows = [["Sensor out of sequence", "run sequence not completed in order"],
                ["Motor time out", "no motor stop switch signal in time"],
                ["Sensor stuck", "a detector active at run start (flag inside)"],
                ["Service due", f"cycle count reached the threshold ({D.SERVICE_DUE_CYCLES})"]]
        data_table(self, ["Error message", "Meaning"], rows, pos=UP * 0.7, size=FS_TAG + 2,
                   cues=[self.c(s, "تَسَلْسُلٌ لَمْ"), self.c(s, "وَمِفْتَاحُ إِيقَافٍ"),
                         self.c(s, "وَكَاشِفٌ فَعَّالٌ"), self.c(s, "وَتَذْكِيرٌ")])
        self.sync(self.c(s, "وَمُهْلَةُ المُحَرِّكِ"))
        self.say(f"Motor switch timeout: factory set per model (e.g. {D.MOTOR_SWITCH_TIMEOUT_EXAMPLE} s)"
                 " — consult Honeywell before changing", ALERT_C)

    def seg6(self, s):
        self.heading("A6  From pulses to MF")
        # timing sketch: meter pulses, detector gates, the two clocks
        p = 0.6
        x0 = -5.4
        ratio = D.CHRONO_TD / D.CHRONO_TP
        tP = D.CHRONO_N * p
        d1 = x0 - 0.22
        d2 = d1 + tP * ratio
        y0, hp = 0.6, 0.55
        pts = [[-6.3, y0, 0]]
        for k in range(-2, D.CHRONO_N + 2):
            xr = x0 + k * p
            if xr < -6.3 or xr + p / 2 > 6.0:
                continue
            pts += [[xr, y0, 0], [xr, y0 + hp, 0], [xr + p / 2, y0 + hp, 0], [xr + p / 2, y0, 0]]
        pts.append([6.0, y0, 0])
        wave = VMobject(color=METER_C, stroke_width=3).set_points_as_corners(pts)
        wl = label("meter pulses", FS_TAG, METER_C).next_to(wave, LEFT, 0.1).shift(UP * 0.3)
        gates = VGroup(*[DashedLine([x, -0.3, 0], [x, 2.3, 0], color=PROVER_C, stroke_width=3)
                         for x in (d1, d2)])
        gl = VGroup(label("D1", FS_TAG, PROVER_C).next_to(gates[0], UP, 0.05),
                    label("D2", FS_TAG, PROVER_C).next_to(gates[1], UP, 0.05))
        self.play(Create(wave), run_time=1.5)
        self.play(Create(gates), FadeIn(gl), run_time=0.8)
        self.sync(self.c(s, "وَفِي مِثَالِنَا"))
        self.say(f"One pulse of {D.NOMINAL_PULSES:,} = {D.PULSE_FRACTION_PCT:.5f} %  ≈ 1/7 of the "
                 f"{D.REPEATABILITY_LIMIT:.3f} % limit", ALERT_C)
        tD = DoubleArrow([d1, 1.7, 0], [d2, 1.7, 0], buff=0, stroke_width=3, color=PROVER_C,
                         tip_length=0.15)
        tDl = label("t_D", FS_LABEL, PROVER_C).next_to(tD, UP, 0.05)
        tPa = DoubleArrow([x0, -0.05, 0], [x0 + tP, -0.05, 0], buff=0, stroke_width=3,
                          color=METER_C, tip_length=0.15)
        tPl = label("t_P", FS_LABEL, METER_C).next_to(tPa, DOWN, 0.05)
        self.sync(self.c(s, "الأُولَى مِنَ الكَاشِفِ"))
        self.play(GrowFromCenter(tD), FadeIn(tDl), run_time=0.8)
        self.sync(self.c(s, "وَالثَّانِيَةُ مِنْ"))
        self.play(GrowFromCenter(tPa), FadeIn(tPl), run_time=0.8)
        self.sync(self.c(s, "وَنَعُدُّ"))
        nl = label(f"N = {D.CHRONO_N} whole pulses", FS_LABEL, METER_C).next_to(tPl, DOWN, 0.1)
        self.play(FadeIn(nl), run_time=0.5)
        sketch = VGroup(wave, wl, gates, gl, tD, tDl, tPa, tPl, nl)
        self.sync(self.c(s, "نَضْرِبُ") - 0.4)
        self.play(FadeOut(self.caption), sketch.animate.scale(0.55).move_to(UP * 2.0), run_time=0.8)
        self.caption = VMobject()
        worked_calculation(self, ["N_i", "=", "N", "×", "t_D", "÷", "t_P"],
                           ["=", f"{D.CHRONO_N}", "×", f"{D.CHRONO_TD:.3f} ms", "÷",
                            f"{D.CHRONO_TP:.3f} ms"],
                           f"= {D.CHRONO_INTERP:.1f} pulses", pos=DOWN * 1.1,
                           cues=[self.c(s, "نَضْرِبُ"), self.c(s, "فَثَمَانِيَ"), self.c(s, "تَصِيرُ")])
        self.sync(self.c(s, "ثُمَّ حَجْمُ") - 0.4)
        self.clear(self.head)
        worked_calculation(self, ["F", "=", "BPV", "×", "CTSp", "×", "CPSp", "×", "CTPLp"],
                           ["=", f"{D.BPV:.5f}", "×", f"{D.CTSP:.7f}", "×", f"{D.CPSP:.7f}", "×",
                            f"{D.CTPL_P:.5f}"],
                           f"= {D.F_VOL:.6f} m³", pos=UP * 1.3, color=PROVER_C, size=FS_EQUATION - 4,
                           cues=[self.c(s, "ثُمَّ حَجْمُ"), self.c(s, "مَضْرُوبًا فِي تَصْحِيحِ"),
                                 self.c(s, "وَلَهُ حَدَّانِ") - 0.2])
        self.say(f"CTSp = [1 + (Tp − {D.T_BASE:.0f})·Ga] × [1 + (Td − {D.T_BASE:.0f})·Gl] = "
                 f"{D.CTS_TUBE:.6f} × {D.CTS_DET:.6f}", GREY_INK, size=FS_TAG + 2)
        self.sync(self.c(s, "وَحَجْمُ العَدَّادِ"))
        wl2 = worked_calculation(self, ["L", "=", "(N_avg", "÷", "K)", "×", "CTPLm"],
                                 ["=", f"({D.AVG_PULSES:.2f}", "÷", f"{D.K_FACTOR})", "×",
                                  f"{D.CTPL_M:.5f}"],
                                 f"= {D.L_VOL:.6f} m³", pos=DOWN * 1.5, color=METER_C,
                                 size=FS_EQUATION - 8)
        self.sync(self.c(s, "وَالنِّسْبَةُ بَيْنَهُمَا"))
        self.play(FadeOut(self.caption), run_time=0.3)
        self.caption = VMobject()
        mf = label(f"MF = F ÷ L = {D.MF:.5f}     Actual K = K ÷ MF = {D.ACTUAL_K:.0f}",
                   FS_BODY - 4, ACCENT_3, weight=BOLD).move_to([0, -3.3, 0])
        fit(mf)
        self.play(Write(mf), run_time=1.2)

    def seg7(self, s):
        self.heading("A7  Maintenance and water draw")
        tl = timeline(self, [("Each session", "pressure parts · covers · safety devices"),
                             ("Monthly", "drive, chains, detector bar, cables"),
                             ("Semi-annual", "borescope: piston + poppet seals, chrome")],
                      cues=[self.c(s, "قَبْلَ كُلِّ جَلْسَةٍ"), self.c(s, "شَهْرِيًّا"),
                            self.c(s, "وَكُلَّ نِصْفِ")],
                      y=1.55, width=12.4)
        self.sync(self.c(s, "ثُمَّ اخْتِبَارُ") - 0.3)
        t1 = label("Static leak test", FS_LABEL, ALERT_C, weight=BOLD).move_to([-3.4, -0.35, 0])
        self.play(FadeIn(t1), run_time=0.4)
        ck1 = checklist(self, ["Isolated full, piston pulled up",
                               f"ΔP raised to {D.LEAK_DP_PSID} psid",
                               f"Wait {D.LEAK_SETTLE_MIN} min, watch {D.LEAK_WATCH_MIN} min",
                               f"Drop > {D.LEAK_MAX_DROP_PCT} % → seal leak"],
                        pos=[-3.4, -1.75, 0], size=FS_TAG + 4,
                        cues=[self.c(s, "نَعْزِلُ"), self.c(s, "وَنَرْفَعُ"), self.c(s, "وَبَعْدَ خَمْسِ"),
                              self.c(s, "فَهُبُوطٌ")])
        self.sync(self.c(s, "وَأَخِيرًا الوُوتَر") + 0.8)
        t2 = label("Water draw", FS_LABEL, PROVER_C, weight=BOLD).move_to([3.4, -0.35, 0])
        self.play(FadeIn(t2), run_time=0.4)
        checklist(self, [f"≥ {D.WD_MIN_DRAWS} consecutive draws",
                         f"within {D.WD_REPEAT_PCT} %",
                         f"one at a {D.WD_FLOW_CHANGE_PCT} % different flow",
                         "every year, or per the authority"],
                  pos=[3.4, -1.75, 0], size=FS_TAG + 4,
                  cues=[self.c(s, "ثَلَاثُ سَحَبَاتٍ"), self.c(s, "ضِمْنَ صِفْرٍ"),
                        self.c(s, "إِحْدَاهَا"), self.c(s, "سَنَوِيًّا")])
        self.sync(self.c(s, "فَالتَّكْرَارِيَّةُ"))
        self.say("Excellent repeatability does not prove the volume is right", ALERT_C)

    # ================= Part B: WinSFC =================
    def seg8(self, s):
        self.part("Part B  ·  WinSFC")
        self.heading("B8  Where WinSFC sits")
        concept_map(self, "SFC332P\nflow computer",
                    ["Laptop · WinSFC\nreads / writes configuration", "Prover", "Meter"],
                    links=["Modbus", "", ""],
                    cues=[self.c(s, "وِين إِسْ إِفْ سِي بَرْنَامَجٌ"), self.c(s, "لَا يَرَى البُرُوفَرَ"),
                          self.c(s, "وَلَا العَدَّادَ")],
                    colors=[ACCENT_3, LIGHT_INK, LIGHT_INK], radius=(4.3, 2.2), pos=UP * 0.3)
        self.say("WinSFC sees only what the flow computer reports", GREY_INK)
        self.sync(self.c(s, "يَتَّصِلُ بِهَا"))
        self.say(f"Modbus, e.g. RTU on RS-485 at {D.BAUD_EXAMPLE} bit/s", GREY_INK)
        self.sync(self.c(s, "وَالحَاسِبَةُ تَعْمَلُ"))
        self.say("The flow computer keeps computing without the laptop — you lose Diagnostic "
                 "and reports", GREY_INK)
        self.sync(self.c(s, "وَفِي طَرَفِ") - 0.3)
        self.clear(self.head)
        tab = data_table(self, ["Comm. Status", "You edit", "Calibration / Override"],
                         [["IDLE (ONLINE)", "the flow computer", "available"],
                          ["OFFLINE", "a file on the laptop", "disabled"]],
                         cues=[self.c(s, "أُونْلَايْن"), self.c(s, "فِي أُوفْلَايْن")],
                         pos=UP * 0.6, size=FS_LABEL)
        self.sync(self.c(s, "وَكُلُّ مَا"))
        highlight_row(self, tab, 1, ALERT_C)

    def seg9(self, s):
        self.heading("B9  The direction rule")
        comparison(self, ("Upload from FC", "flow computer → laptop", "a safe read"),
                   ("Download to FC", "laptop file → flow computer", "changes a custody device"),
                   colors=(ACCENT_3, ALERT_C), pos=UP * 1.35, card_w=5.4,
                   cues=[self.c(s, "أَبْلُود يَنْسَخُ"), self.c(s, "أَمَّا دَاوْنْلُود")])
        self.sync(self.c(s, "فَلَا دَاوْنْلُود"))
        self.say("No Download without an explicit decision by the responsible engineer", ALERT_C)
        checklist(self, ["1  a fresh Upload", "2  save it under a dated name",
                         "3  compare the fields that will change"],
                  pos=DOWN * 1.6, size=FS_LABEL,
                  cues=[self.c(s, "أَبْلُود جَدِيدٌ"), self.c(s, "ثُمَّ حِفْظُهُ"),
                        self.c(s, "ثُمَّ مُقَارَنَةُ")])
        self.sync(self.c(s, "وَتَذَكَّرْ"))
        self.say("A configuration file is a dated snapshot — the title bar names the file, "
                 "not the device state", GREY_INK)
        self.sync(self.c(s, "فَقَبْلَ أَيِّ زِرٍّ"))
        self.say("Before any button: which way does the data go?", ACCENT_3)

    def window_drawing(self):
        W, H = 9.6, 4.3
        frame = Rectangle(width=W, height=H, stroke_width=4)
        title = box("WinSFC  —  SFC332P  ·  demo_config.sfc", W, 0.45, size=FS_TAG - 2,
                    fill=PANEL_FILL).move_to(frame.get_top() + DOWN * 0.225)
        menus = Text("Configuration File   View   Tools   Calibration   Override   "
                     "Historical Data   Window   Help", font_size=FS_TAG - 6)
        menus.scale_to_fit_width(W - 2.6).next_to(title, DOWN, 0.12).align_to(frame, LEFT).shift(RIGHT * 0.15)
        status = box("IDLE (ONLINE)", 2.0, 0.34, color=ACCENT_3, size=FS_TAG - 6)
        status.next_to(title, DOWN, 0.06).align_to(frame, RIGHT).shift(LEFT * 0.1)
        names = ["Connect to Device", "Go Offline", "Diagnostic", "Historical Reports",
                 "Prover Diagram", "Prove Request", "Configure Device"]
        btns = VGroup(*[box(n, 2.3, 0.36, size=FS_TAG - 6) for n in names])
        btns.arrange(DOWN, buff=0.09).next_to(menus, DOWN, 0.2).align_to(frame, LEFT).shift(RIGHT * 0.15)
        pages = ["Meter 1-60 Data", "Prove Data", "Communication Ports", "Input Assignments",
                 "Analog Output", "Status Input & Switch Outs", "Display Assignment", "Modbus Shift"]
        plist = VGroup(*[Text(n, font_size=FS_TAG - 6) for n in pages]).arrange(DOWN, aligned_edge=LEFT,
                                                                           buff=0.07)
        panel = Rectangle(width=6.6, height=3.0, stroke_width=3, color=GREY_INK)
        panel.next_to(btns, RIGHT, 0.25).align_to(btns, UP)
        ptitle = Text("Configure Device", font_size=FS_TAG - 4, weight=BOLD).next_to(panel.get_corner(UL),
                                                                                      DR, 0.1)
        plist.next_to(ptitle, DOWN, 0.1).align_to(ptitle, LEFT)
        full = VGroup(box("Upload Full from Flow Computer", 3.0, 0.34, color=ACCENT_3, size=FS_TAG - 7),
                      box("Download Full to Flow Computer", 3.0, 0.34, color=ALERT_C, size=FS_TAG - 7))
        full.arrange(DOWN, buff=0.1).next_to(panel.get_corner(DR), UL, 0.12)
        small = VGroup(box("Upload from FC", 1.45, 0.3, color=ACCENT_3, size=FS_TAG - 8),
                       box("Download to FC", 1.45, 0.3, color=ALERT_C, size=FS_TAG - 8))
        small.arrange(RIGHT, buff=0.1).next_to(full, UP, 0.15).align_to(full, RIGHT)
        g = VGroup(frame, title, menus, status, btns, panel, ptitle, plist, full, small)
        return g, dict(title=title, menus=menus, btns=btns, panel=panel, small=small)

    def seg10(self, s):
        self.heading("B10  Main window")
        g, p = self.window_drawing()
        g.move_to(DOWN * 0.35 + RIGHT * 0.7)
        labeled_diagram(self, g, [("Title bar: device + open file", p["title"], UP),
                                  ("Menus", p["menus"], UR),
                                  ("Buttons", p["btns"], LEFT),
                                  ("Configure Device panel", p["panel"], UP)],
                        cues=[self.c(s, "فِي أَعْلَى النَّافِذَةِ"), self.c(s, "وَتَحْتَهُ القَوَائِمُ"),
                              self.c(s, "وَعَلَى الجَانِبِ"), self.c(s, "وَفِي هٰذِهِ اللَّوْحَةِ")],
                        draw_time=1.6)
        self.sync(self.c(s, "وَلِكُلِّ صَفْحَةٍ"))
        emphasize(self, p["small"], ALERT_C)
        self.sync(self.c(s, "ثُمَّ نُقَسِّمُ") - 0.3)
        self.clear(self.head)
        cmp = comparison(self, ("Safe", "Historical Data", "Historical Reports", "(read only)"),
                         ("Dangerous", "Calibration: changes raw → engineering",
                          "Override: manual value used as live",
                          "Reset Prev. Prove Data  ·  Clear System"),
                         colors=(ACCENT_3, ALERT_C), pos=UP * 0.5, card_w=5.9,
                         cues=[self.c(s, "الآمِنُ"), self.c(s, "وَالخَطِرُ")])
        self.sync(self.c(s, "وَأَخْطَرُ بُنُودِهِ"))
        emphasize(self, cmp[0][1][1][3], ALERT_C)

    def seg11(self, s):
        self.heading("B11  Prove Data")
        rows = [["Identity", "maker · type · ID · size · serial · model → report"],
                ["Session rules", "Prover Type · Method · Runs to Avg · Total Runs · Repeat %"],
                ["Volume, geometry", "Prove Volume (last water draw) · D · wall · E → CPSp"],
                ["Thermal", f"Area coeff. Ga · Displacer Shaft coeff. Gl · base {D.T_BASE:.0f} °C"],
                ["Stability checks", "temp change · sample period · flow change · Tp–Tm"],
                ["Detector, signals", "switch type · single delay · upstream / run polarity"]]
        self.say("Tells the flow computer everything it cannot measure", GREY_INK)
        tab = data_table(self, ["Group", "Fields (examples)"], rows, pos=UP * 0.45, size=FS_TAG,
                         cues=[self.c(s, "هُوِيَّةُ البُرُوفَرِ"), self.c(s, "وَقَوَاعِدُ الجَلْسَةِ"),
                               self.c(s, "ثُمَّ الحَجْمُ"), self.c(s, "ثُمَّ المُعَامِلَاتُ"),
                               self.c(s, "ثُمَّ فُحُوصُ"), self.c(s, "وَأَخِيرًا إِعْدَادَاتُ")])
        self.sync(self.c(s, "وَانْتَبِهْ"))
        highlight_row(self, tab, 2, ALERT_C)
        self.say("A wrong number here is a systematic error in every run — invisible in repeatability",
                 ALERT_C)

    def diag_drawing(self):
        W = 11.2
        frame = Rectangle(width=W, height=3.3, stroke_width=4)
        hdr = Text(f"Unit ID 1     Freq#1  {D.FREQ_SHOWN:.1f} Hz     ST#1–#4  ○ ○ ○ ○     "
                   "#1–#5  ○ ○ ○ ○ ○", font=MONO, font_size=FS_TAG - 4)
        hdr.next_to(frame.get_top(), DOWN, 0.18)
        head = ["Input", "mA/Ohm", "Numerical", "Fail Code", ""]
        rows = [["Prover temp (RTD)", f"{D.PT100_R:.2f}", f"{D.T_PROVER:.1f}", "0", "Calibrate"],
                ["Prover pressure", "…", f"{D.P_PROVER:.1f}", "0", "Calibrate"],
                ["Density", "…", f"{D.DENSITY_SUSPECT:.1f}", "1", "Calibrate"]]
        xs = [-4.1, -1.2, 0.6, 2.4, 4.2]
        grid = VGroup()
        for r, row in enumerate([head] + rows):
            for k, (x, t) in enumerate(zip(xs, row)):
                m = Text(t, font=MONO, font_size=FS_TAG - 4, weight=BOLD if r == 0 else NORMAL)
                if k == 4 and r > 0:
                    m = box(t, 1.5, 0.32, size=FS_TAG - 7)
                m.move_to([x, 0.55 - r * 0.45, 0])
                grid.add(m)
        cols = VGroup(*[grid[i] for i in range(len(grid)) if i % 5 in (1, 2)])
        fcol = VGroup(*[grid[i] for i in range(len(grid)) if i % 5 == 3])
        alarms = Text("Alarms: NONE", font=MONO, font_size=FS_TAG - 4, color=ACCENT_3)
        alarms.next_to(frame.get_corner(DL), UR, 0.15)
        g = VGroup(frame, hdr, grid, alarms)
        return g, dict(hdr=hdr, cols=cols, fcol=fcol, alarms=alarms)

    def seg12(self, s):
        self.heading("B12  Diagnostic")
        g, p = self.diag_drawing()
        g.move_to(UP * 0.6)
        labeled_diagram(self, g, [("Header: address · live frequency · digital I/O", p["hdr"], UP),
                                  ("Raw signal → engineering value", p["cols"], DOWN)],
                        cues=[self.c(s, "فِي تَرْوِيسَتِهَا"), self.c(s, "وَفِي جَدْوَلِهَا")],
                        draw_time=1.6)
        self.sync(self.c(s, "وَفِيل كُود"))
        emphasize(self, p["fcol"], ALERT_C)
        self.sync(self.c(s, "صِفْرٌ يَعْنِي"))
        codes = "   ".join(f"{n}: {t}" for n, t in D.FAIL_CODES)
        self.say(f"Fail Code   {codes}", ALERT_C, size=FS_TAG)
        self.sync(self.c(s, "ثُمَّ ثَلَاثَةُ فُحُوصٍ") - 0.3)
        self.clear(self.head)
        worked_calculation(self, ["Q", "=", "f", "×", "3600", "÷", "K"],
                           ["=", f"{D.FREQ_SHOWN:.1f} Hz", "×", "3600", "÷", f"{D.K_FACTOR}"],
                           f"= {D.Q_FROM_FREQ:.1f} m³/h", pos=UP * 1.35, size=FS_EQUATION - 6,
                           color=METER_C,
                           cues=[self.c(s, "التَّرَدُّدُ مَضْرُوبًا"), self.c(s, "مَقْسُومًا"),
                                 self.c(s, "يُعْطِي")])
        self.sync(self.c(s, "وَمُقَاوَمَةُ"))
        pt = VGroup(label(f"Pt100  {D.PT100_R:.2f} Ω  →  {D.PT100_T_CVD:.1f} °C  (Callendar–Van Dusen)",
                          FS_LABEL, PROVER_C, weight=BOLD),
                    label(f"quick linear check: (R − 100) ÷ 0.385 = {D.PT100_T_LINEAR:.2f} °C",
                          FS_TAG + 2, GREY_INK)).arrange(DOWN, buff=0.15).move_to(DOWN * 1.2)
        self.play(FadeIn(pt[0], shift=UP * 0.1), run_time=0.6)
        self.sync(self.c(s, "وَالتَّقْرِيبُ الخَطِّيُّ"))
        self.play(FadeIn(pt[1], shift=UP * 0.1), run_time=0.5)
        self.sync(self.c(s, "وَالقِيمَةُ المُسْتَدِيرَةُ"))
        self.say(f"Density {D.DENSITY_SUSPECT:.1f} exactly? A substitute (Maintenance) value until "
                 "proven live", ALERT_C)

    def seg13(self, s):
        self.heading("B13  Status Input / Switch Output")
        concept_map(self, "SFC332P\ndigital terminals",
                    ["ST in: Prove Request", "ST in: Prover Ready", "SW out: launch prover",
                     "SW out: prove in progress", "SW out: prove complete", "SW out: prove abort"],
                    colors=[PROVER_C, PROVER_C, METER_C, METER_C, METER_C, METER_C],
                    radius=(4.5, 2.25), pos=UP * 0.35,
                    cues=[self.c(s, "كَطَلَبِ المُعَايَرَةِ"), self.c(s, "أَوْ جَاهِزِيَّةِ"),
                          self.c(s, "أَطْلِقِ"), self.c(s, "وَالمُعَايَرَةُ جَارِيَةٌ"),
                          self.c(s, "أَوِ اكْتَمَلَتْ"), self.c(s, "أَوْ أُلْغِيَتْ")])
        self.sync(self.c(s, "وَالرَّقْمُ فِي كُلِّ خَانَةٍ"))
        self.say("The number in each box picks the function — it changes what the wire means",
                 GREY_INK)
        self.sync(self.c(s, "فَإِذَا كَانَتْ"))
        self.say("Wrong function on the terminal wired to the controller → no request, no piston",
                 ALERT_C)
        self.sync(self.c(s, "وَقَدْ يَمْحُو"))
        self.say("Keep the working configuration file in two places off the laptop", ACCENT_3)

    def seg14(self, s):
        self.heading("B14  The proving sequence")
        flow = process_flow(self, ["Prove Request", "Run Permissive", "Retract · release",
                                   "Pulse 1: count", "Pulse 2: stop", "Repeat → MF + report"],
                            pos=UP * 1.7, size=FS_LABEL,
                            cues=[self.c(s, "يُطْلِقُ المُهَنْدِسُ"), self.c(s, "وَتَرْفَعُ إِذْنَ"),
                                  self.c(s, "يُسْحَبُ المِكْبَسُ"), self.c(s, "فَتَصِلُ نَبْضَةُ"),
                                  self.c(s, "حَتَّى النَّبْضَةِ"), self.c(s, "وَتَتَكَرَّرُ")])
        t1 = label(f"Repeat until {D.RUNS_TO_AVERAGE} consecutive runs are within the limit, "
                   "or Total Runs is used up", FS_LABEL, GREY_INK).move_to(UP * 0.1)
        fit(t1)
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.6)
        self.sync(self.c(s, "وَالتَّكْرَارِيَّةُ هِيَ"))
        rep = equation(self, ["Repeatability", "=", "(max − min) ÷ min", "=",
                              f"{D.REPEATABILITY:.4f} %", "≤", f"{D.REPEATABILITY_LIMIT:.3f} %"],
                       colors={4: ACCENT_3, 6: ACCENT_3}, size=FS_EQUATION - 8, pos=DOWN * 1.2)
        self.sync(self.c(s, "ثُمَّ يَخْرُجُ") + 0.8)
        highlight_step(self, flow, 5, ACCENT_3)
        self.sync(self.c(s, "وَقَبْلَ الطَّلَبِ") - 0.3)
        self.clear(self.head)
        checklist(self, ["One meter in service, the other stream isolated",
                         "Controller in Meter Calibration (Prover Status)",
                         "The meter by its TAG and stream, not its serial number",
                         "Freq#1 close to the transmitter display",
                         "Every channel live (Fail Code), no Maintenance value",
                         "Total Runs · Runs to Average · Repeatability set",
                         "Prover and meter temperatures stable"],
                  pos=DOWN * 0.1, size=FS_LABEL,
                  cues=[self.c(s, "عَدَّادٌ وَاحِدٌ"), self.c(s, "المُتَحَكِّمُ فِي مِيتَر"),
                        self.c(s, "العَدَّادُ المَقْصُودُ"), self.c(s, "التَّرَدُّدُ قَرِيبٌ"),
                        self.c(s, "كُلُّ القَنَوَاتِ"), self.c(s, "الجَوْلَاتُ وَالحَدُّ"),
                        self.c(s, "وَالحَرَارَةُ مُسْتَقِرَّةٌ")])

    # ================= Wrap-up =================
    def seg15(self, s):
        self.part("Wrap-up", hold=0.8)
        self.heading("Troubleshooting and golden rules")
        rule = label("Find the last step that worked — the fault is in the next one",
                     FS_LABEL + 2, ACCENT_2, weight=BOLD).move_to(UP * 2.75)
        fit(rule)
        self.play(Write(rule), run_time=1.2)
        import explainer.scenes as _sc
        old = _sc.FS_SUMMARY, _sc.FS_HEADING
        _sc.FS_SUMMARY, _sc.FS_HEADING = FS_LABEL - 2, FS_BODY - 4
        try:
            summary_box(self, "Golden rules",
                        ["Upload is safe · Download is a decision",
                         "Controller in Meter Calibration before the first run",
                         "Check Fail Codes even when Alarms say NONE",
                         "Repeat% 0.000 with one run: an alarm, not quality",
                         "Keep the configuration file off the laptop",
                         "Good repeatability does not prove the volume",
                         "Safety: covers on · pressurise slowly · depressurise first"],
                        pos=DOWN * 0.55,
                        cues=[self.c(s, "أَبْلُود آمِنٌ"), self.c(s, "المُتَحَكِّمُ فِي مِيتَر"),
                              self.c(s, "افْحَصْ فِيل"), self.c(s, "تَكْرَارِيَّةٌ صِفْرِيَّةٌ"),
                              self.c(s, "احْفَظْ مِلَفَّ"), self.c(s, "التَّكْرَارِيَّةُ الجَيِّدَةُ"),
                              self.c(s, "وَالسَّلَامَةُ")])
        finally:
            _sc.FS_SUMMARY, _sc.FS_HEADING = old
        self.sync(self.c(s, "وَاعْتِمَادُ"))
        self.say("MF approval: the responsible engineer and the official records", GREY_INK)


if __name__ == "__main__":
    main(__file__, "SvpWinsfcFull", NARRATION)
