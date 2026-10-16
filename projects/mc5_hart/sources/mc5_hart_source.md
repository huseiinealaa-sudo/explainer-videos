# معايرة مرسلات الضغط الذكية بجهاز Beamex MC5 عبر HART — المصدر المنقّح
المراجع: [1] User Guide for MC5 HART Option (Appendix 1، ص 136–149). [2] MC5 User Guide، Firmware 1.90. [3] MC5-IS User Manual. ترتيب الأزرار والصفحات مأخوذ أيضًا من شاشات جهاز فعلي بإصدار أحدث من الدليل، فإن اختلف الدليل مع هذا النص فاعرض الفرق ولا تحسمه وحدك. كل القيم توضيحية من ملف البيانات.

## الحلقة 1: الاتصال والبرمجة
1.1 قبل أي اتصال: صفّر وحدة ضغط المرجع والمنفذ مفتوح للهواء: D/Menu ← A/Window 1 Setup ← 7/Zero Pressure Module. يُعاد التصفير كلما تغيّر وضع الجهاز أو ارتفاعه [2 ص 40]. [+ الملف الأصلي وضعه تحت Calibration Mode]
1.2 الاتصال: D/Menu ← B/Window 2 Setup (عند الحاجة) ← 5/HART [1 ص 141]. يبحث MC5 في عناوين الاستطلاع (Polling Address) من 0 إلى 15، ويصل حتى 16 جهازًا بالحلقة نفسها. تُختار المرسلة بـ D/Select.
  - العنوان 0 يعني أن خرج 4–20 mA يعمل طبيعيًا. العناوين 1–15 تعني وضع Multidrop، والتيار ثابت قرب 4 mA.
  - إن لم يجد الجهاز مرسلة: Restart بعد التحقق من التغذية ووجود مقاومة HART.
1.3 قائمة HART تحل محل قائمة النافذة، وكمية النافذة تتحول تلقائيًا إلى كمية الخرج الرقمي (PV) [1 ص 142]. عناصرها:
  - 1 Disconnect Device: لازم قبل تغيير كمية النافذة.
  - 2 Device Information، و 3 Device Settings.
  - 4 Display Unit: يغيّر عرض MC5 فقط، لا المرسلة.
  - 6 Trim Instrument، و 7 Add HART Instrument to Database.
  - الأزرار السفلية: Window 1 Setup، Window 2 Setup، Others، Close MENU.
  - نصيحة: نافذة على E: HART/PV وأخرى على E: Current Measurement، لترى في لحظة واحدة ما «تعتقده» المرسلة وما «تخرجه».
1.4 Device Information: Tag، Device ID، Serial Number، Manufacturer، Device Type، Software/Hardware Revision، Date، Descriptor، Message. القابل للتعديل: Tag، Serial Number، Date، Descriptor، Message [1 ص 142].
1.5 Device Settings: Tag، Polling Address، PV/Range Unit، Lower Range Value، Upper Range Value، Damping، Transfer Function، Burst mode، ثم Sensor: Serial Number، Lower/Upper Range Limit، Minimum Span. الأزرار: A/Close و C/Edit. القابل للتعديل: Tag، Polling Address، PV/Range Unit، Lower/Upper Range، Damping، Transfer Function، Burst Mode، Sensor Serial Number [1 ص 143].
  - Damping: بعد كل نقطة ضغط انتظر نحو 5 أضعافه.
  - Transfer Function: Linear للضغط، و Square Root لمرسلات الضغط التفاضلي في قياس الجريان فقط.
  - Burst mode: Off، أي أن المرسلة تجيب عند السؤال فقط.
  - URL/LRL حدود فيزيائية ثابتة، ولا يُبرمج المدى خارجها ولا أضيق من Minimum Span.
1.6 التعديل بـ Edit: اختر الحقل بالأسهم، وعدّل، وأكّد بـ Enter.
  - قبل التعديل سجّل القيم الأصلية.
  - أي تغيير للمدى يُعدَّل مثله في نظام التحكم، وإلا قرأت غرفة التحكم ضغطًا خاطئًا.
  - بعد التعديل افتح Device Settings مجددًا وتأكد أن القيمة كُتبت.
  - قاعدة: تغيير المدى (Rerange) ليس معايرة؛ يغيّر أي ضغط يقابل 4 و20 mA، ولا يصحح خطأ الحساس.
  - المثال المحسوب الوحيد في الحلقة: تغيير URV من 40 إلى 30 kgf/cm². ضغط 15 kgf/cm² كان يقابل 10 mA، فصار يقابل 12 mA.

## الحلقة 2: الفحص والتعديل (Trim Instrument)
2.1 مسار الإشارة (20 ثانية فقط): الضغط ← الحساس ← القيمة الرقمية PV ← دائرة الخرج D/A ← تيار 4–20 mA. لكل جزء خطؤه الخاص، و HART يتيح فحص كل جزء وحده.
2.2 الدخول: D/Menu ← 6/Trim Instrument ← قائمة منبثقة: Analog Output (AO) أو Digital Output (PV). يقرأ MC5 بيانات المرسلة ثم يفتح صفحة Instrument Input ← B/Next Page ← Instrument Output ← A/Trim، فتفتح نوافذ المعايرة مع قائمة التعديل [1 ص 143–144]. [+ الملف الأصلي أغفل هذه الصفحات]
  - Select Output يبدّل بين AO و PV.
  - تحذير الدليل: لا تغيّر شيئًا دون معرفة وتخويل [1 ص 144].
  - في الحقل: أبلغ غرفة التحكم، وضع الحلقة على اليدوي (Manual)، واعزل أنظمة الإيقاف حسب الإجراءات، لأن MC5 سيثبّت التيار على قيم يحددها هو.
2.3 دائرة الخرج (AO):
  - في الشاشة: Input = Current [Keyed]، وهو التيار الذي يأمر به MC5. و Output = Current [E: Meas]، وهو ما قاسه فعلًا. ورسم الخطأ % of span.
  - القائمة: Trim Lower 0% Range، Trim Upper 100% Range، Check Any Value، Select Output، Device Information، Device Settings، End HART Adjustment.
  - الفحص أولًا: Check Any Value عند 4 و12 و20 mA، ويُستحسن 3.8 و20.5 mA.
  - مستويات NAMUR NE43: 3.8–20.5 مجال القياس والإشباع، و ≤3.6 أو ≥21.0 إنذار عطل.
  - التعديل فقط إذا فشل الفحص: Trim Lower ← يأمر MC5 المرسلة بـ 4 mA ← خانة Enter measured 0% ← C/Fetch ينسخ قيمة نافذة الخرج (أو تُدخل يدويًا) ← D/Send [1 ص 149]. [+ الملف الأصلي كتب D Trim] ثم Trim Upper بالطريقة نفسها عند 20 mA، ثم إعادة الفحص.
  - الترتيب: الأسفل ثم الأعلى، لأن تعديل الصفر يزيح الخط كله وتعديل النهاية يغيّر الميل.
2.4 الحساس (PV):
  - في الشاشة: Input = ضغط المرجع من وحدة MC5، و Output = Pressure [E: HART/PV].
  - خانة Trim 0% to: ← C/Fetch ينسخ قيمة نافذة الدخل، أي المرجع ← D/Send [1 ص 149].
  - تعديل النهاية يُجرى عند ضغط قريب من أعلى المدى المستخدم، وبوحدة ضغط تغطيه. لا يُجرى عند نقطة بعيدة عن المدى، لأنه يصحح الميل منها.
  - صفر المرسلة يتأثر بوضعية التركيب، فتعديل الصفر عادةً في الموقع بعد التركيب النهائي والمرسلة منفّسة.
2.5 قصة الفصل بين الخطأين:
  - المرسلة منفّسة والمرجع 0.000. التيار 3.9363 mA، أي نحو −0.40% من المدى. فأين الخطأ؟
  - Check Any Value عند 4 mA يعطي 4.0003، فدائرة الخرج سليمة.
  - PV = −0.160 kgf/cm²، فالخطأ في الحساس.
  - العلاج: Trim 0% to ← Fetch (0.000) ← Send. بعده PV = 0.000 والتيار 4.0003 mA.
  - الدرس: بالفصل بين الجزأين تعرف مصدر الخطأ قبل أن تعدّل.
2.6 الإنهاء الإلزامي: End HART Adjustment يعيد المرسلة للقياس الطبيعي، ثم تحقق أن التيار يتبع الضغط، ثم Disconnect Device.

## الحلقة 3: المعايرة الموثقة (Calibration Mode)
3.1 Add HART Instrument to Database ← اختر Analog أو Digital [1 ص 145].
  - يعامل MC5 الخرجين AO و PV أداتين منفصلتين، ولمعايرة الاثنين يُنشأ ملفان [1 ص 137].
  - يجلب من المرسلة: الكميات والوحدات والمدى وطرق الدخل والخرج و Transfer Function و Setpoint Delay.
  - وسم المرسلة يذهب إلى حقل Device ID، ولا يُعيَّن Position ID تلقائيًا [1 ص 145].
  - يجب مراجعة هذه الحقول على الأقل: Error Calculation Method، Reject if >، Input Port، Calibration Method، Calibration Points، Output Port [1 ص 145].
3.2 صفحات ملف الأداة الأربع، والتنقل بـ B/Next Page، وأزرارها A/Save، B/Next Page، C/Edit، D/MENU:
  - INSTRUMENT GENERAL DATA: Position ID، Position Name، Device ID، Serial Number، Error Calc. Method (% of span)، Reject if >، Adjust if >، Do not Adjust if <، Adjust to <. [للتحقق: المعنى الدقيق للحقول الثلاثة الأخيرة]
  - INSTRUMENT INPUT: Pressure، Input Method (Measured)، Port 1، Pressure Type (Gauge)، Unit، Range 0% / 100%، Sensor supply (None). يجب أن يكون منفذ الدخل وحدة ضغط تغطي المدى دون تجاوز حدها.
  - INSTRUMENT OUTPUT: Current، Output Method (Measured)، Port E، Unit mA، Range 4 / 20، Transfer Function Linear.
  - CALIBRATION SETTINGS: Calibration Method (Manual / Automatic)، Calibration Points (5↑↓)، Setpoint Delay، Maximum Allowed Calibration Point Deviation، Calibration Repeats (As Found / As Left)، Calibration Period. Setpoint Delay هو المدة التي ينتظرها MC5 قبل حفظ قيمتي الدخل والخرج بعد تغيّر الدخل إلى النقطة التالية [3]. [للتحقق: Maximum Allowed Calibration Point Deviation و Calibration Period]
3.3 قائمة الأدوات POSITION/DEVICE ID:
  - تحت القائمة: Device ID، Position Name، وحالة المعايرة (Calibrated / Not Calibrated).
  - الأزرار: A/Basic Mode، C/Select، D/MENU.
  - [للتحقق: معنى علامة ✓ بجانب الأداة]
3.4 نافذة المعايرة: Input، Output، ورسم الخطأ.
  - قبل البدء: A/Back، B/Start، C/Adjust، D/MENU [3 ص 114].
  - قائمتها: Close، Prescan [On]، Start HART Adjustment، View Calibration Results، Zero Pressure Module [1 ص 147].
  - أثناء التسجيل: Stop Readings و Accept [1 ص 147]. [+ الملف الأصلي جعلها أزرار النافذة الدائمة]
  - [للتحقق: وظيفة C/Adjust في الإصدار الأحدث مقارنة بـ Start HART Adjustment]
3.5 النقاط القياسية: 0 و25 و50 و75 و100% صعودًا، ثم نزولًا.
  - الهدف كشف التخلف (Hysteresis): إن اختلفت قراءة النقطة نفسها صعودًا ونزولًا فالحساس فيه احتكاك أو تعب.
  - اقترب من كل نقطة من اتجاه واحد ولا تتجاوزها ثم ترجع.
3.6 المراحل الثلاث: As Found (مقارنة توثّق الحالة قبل أي تعديل)، ثم Adjustment، ثم As Left. إن كانت As Found ضمن الحد فلا حاجة للمرحلتين الأخريين.
  - التعديل من داخل المعايرة: D/MENU ← 1/Start HART Adjustment ← صفحة الدخل ← B/Next Page ← A/Trim. تفتح القائمة و PV مختار، و Select Output يبدّل إلى AO [1 ص 147–148].
  - معايرة AO لا تحتاج HART بالضرورة، فالجهاز يعاملها كأداة تناظرية عادية [1 ص 147].
3.7 تحليل الأخطاء:
  - خطأ الصفر (Offset): إزاحة ثابتة عند كل النقاط، وعلاجه Lower Trim.
  - خطأ الميل (Span): يكبر مع القيمة، وعلاجه Upper Trim.
  - اللاخطية: الطرفان صحيحان والمنتصف منحرف، ولا يُصلح بالتعديل العادي.
  - شجرة القرار: كل النقاط ضمن الحد ← Pass دون تعديل. نقطة خارج الحد ← حدّد الجزء وعدّله ثم As Left. لاخطية أو تخلف كبير أو فشل بعد التعديل ← Reject.
  - لا تعدّل جهازًا سليمًا: المرجع يجب أن يكون أدق بعدة أضعاف (TUR ≥ 4 يُفضَّل).
  - View Calibration Results يعرض الجداول والرسوم المحفوظة.
  - الخاتمة: ما تحمله شهادة المعايرة (بيانات الأداة، والمرجع، ونقاط As Found و As Left، وأقصى خطأ، والتعديل المجرى، والحكم).
