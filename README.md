# explainer-videos
فيديوهات شرح بإنتاج Claude Code

## سلسلة Daniel Compact Prover (7 حلقات)

مادة تعليمية بقيم توضيحية فقط؛ المرجع المُلزِم هو دليل الشركة المصنِّعة وإجراءات الموقع المعتمدة.

| # | الحلقة | الملف | المدة |
|---|---|---|---|
| 1 | مبدأ الإثبات ومعادلة معامل العداد | [output/prover_ep01_principle.mp4](output/prover_ep01_principle.mp4) | 2:57 |
| 2 | الشوط والجولة والتكرارية وخصائص كوريوليس | [output/prover_ep02_passes.mp4](output/prover_ep02_passes.mp4) | 3:54 |
| 3 | بنية المعاير المدمج (10 مكوّنات) | [output/prover_ep03_components.mp4](output/prover_ep03_components.mp4) | 3:32 |
| 4 | دورة التشغيل (5 مراحل) ولماذا لا يتوقف التدفق | [output/prover_ep04_cycle.mp4](output/prover_ep04_cycle.mp4) | 3:11 |
| 5 | الكرونومتري المزدوج وضغط البلينم وحجما أعلى/أسفل المجرى وCTSp | [output/prover_ep05_chronometry.mp4](output/prover_ep05_chronometry.mp4) | 3:31 |
| 6 | FloBoss S600+ والحقيبة الميدانية وواجهة الويب وجلسة إثبات | [output/prover_ep06_floboss.mp4](output/prover_ep06_floboss.mp4) | 3:41 |
| 7 | تدقيق التقرير وإعادة حساب جولة خطوة بخطوة | [output/prover_ep07_audit.mp4](output/prover_ep07_audit.mp4) | 3:59 |
| — | **السلسلة كاملة** (مع شاشة عنوان 3 ث بين الحلقات) | [output/prover_full_series.mp4](output/prover_full_series.mp4) | 25:02 |

- السكربتات في `scripts/` (البيانات التوضيحية: `scripts/prover_demo_data.py`)، والمصادر في `sources/`.
- الدمج: `python scripts/prover_full_series.py` (نسخ مباشر للتدفقات دون إعادة ترميز).
