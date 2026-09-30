# style_test — اختبار هوية بصرية (ليس إنتاجًا)

مشهد صامت واحد: طائرة ركاب عامة (بلا شعار) تتسارع على مدرج عند الغروب ثم تقلع، بثلاثة أنماط (10 ث لكل نمط، 720p، 24 إطارًا/ث).
الناتج: `output/style_test.mp4` (A ثم B ثم C، وحرف النمط في الزاوية العليا اليمنى).

| النمط | الملف | الأمر |
|---|---|---|
| A — Manim ثلاثي الأبعاد | `style_a_3d.py` | `python -m manim render -r 1280,720 --fps 24 projects/style_test/style_a_3d.py StyleA3D` |
| B — Manim ثنائي الأبعاد متجهي | `style_b_vector.py` | `python -m manim render -r 1280,720 --fps 24 projects/style_test/style_b_vector.py StyleBVector` |
| C — Blender دون واجهة (bpy) | `style_c_blender.py` + `run_c.sh` | `bash projects/style_test/run_c.sh` (محاولة واحدة، حدّ 15 دقيقة للتثبيت والتصيير والترميز) |

- `airliner_geom.py`: هندسة الطائرة (شبكة نقاط ووجوه) ومسار الطيران، يشتركان فيهما A وC، وB يستعمل المسار فقط.
- `build_video.sh`: يجمع المقاطع الثلاثة مع الحروف. `contact.sh`: ورقة إطارات لمقطع.
- مقاطع الأنماط الثلاثة المنفردة وأوراق الإطارات في `tmp/style_test/` (غير مُودَعة).
