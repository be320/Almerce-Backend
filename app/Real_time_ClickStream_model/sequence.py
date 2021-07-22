clicks_based_messages = [
{
    "message": {"TextField": " اهلا بيك، تحب ألميرس يساعدك ازاي؟"},
    "elementType": "ChoiceTemplate",
    "choices":  ["البحث من خلال تصفح الويب سايت ","البحث عن طريق الاختيارات","البحث عن طريق الصور","التحدث مع ألميرس"],
    "choiceType":"model_type"
},
{
    "message": {"TextField": "متقلقش حتي لو مش بتدور علي حاجة معينة الميرس هيقدر يساعدك و يعرف انت حابب ايه من خلال تصفحك للويب سايت, لو عجباك الفكرة دوس موافق"},
    "elementType": "ChoiceTemplate",
    "choices": ["اختيار طريقة ترشيح اخرى","موافق","عودة"],
    "choiceType":"NONE"
},
{
    "message": {"TextField": "  جاري تتبع نقراتك، تقدر تتصفح الصفحة ذي ما تحب و اما تحب الميرس يعرضلك المقترحات قولنا"},
    "elementType": "ChoiceTemplate",
    "choices": ["اختيار طريقة ترشيح اخرى","اعرض الاقتراحات","عودة"],
    "choiceType":"ClicksRecommendation"
},
{
    "elementType": "ProductCardTemplate",
    "cards": [{"imgSrc": "https://safwatoys.com/image/cache/catalog/W50-2/x122c5919-e115-43fc-a6c8-d283ce0ffb72-230x230.jpg.pagespeed.ic.ZrBiS-lubg.webp",
                "ProductUrl": "https://safwatoys.com/index.php?route=product/product&product_id=1049",
                "productHeader": "لوحة تلوين بالرمل W50-2",
                "productParagraph": "لوحة معها رمل ملون يقوم الطفل بلصقها ف مكانها المناسب حسب الصورة الملونة لتتحول الي صوره ملونه بشكل مميز ينمي العضلات الدقيقة واصابع اليد ومهارات التحكم تزيد ثقة الطفل بنفسه متاح عدة اشكال تساعد في تمييز الطفل للالوان وتنميه مهاره المطابقة مناسبه للاطفال فرط الحركه مناسب لسن 4 سنين", "id": "1049"},
                {"imgSrc": "https://safwatoys.com/image/cache/catalog/W5-11/W5--11-228x228.jpg",
                "ProductUrl": "https://safwatoys.com/index.php?route=product/product&path=67_106&product_id=2017",
                "productHeader": "صيد سمك وسط W5-11",
                "productParagraph": "تقوم فكرتها علي صيد السمك بالصنارة أو صيدها بالشاكوش لأن به ثقب في المنتصف فيلتقط القطع", "id": "2017"},
                {"imgSrc": "https://safwatoys.com/image/cache/catalog/W37-67/w37-67-230x230.jpeg",
                "ProductUrl": "https://safwatoys.com/index.php?route=product/product&path=67_113&product_id=1846", "productHeader": "سلم وثعبان وليدو خشب w37-67", "productParagraph": "لعبة 2x1 لعبة السلم والثعبان وليدو في شكل جديد مقاس 30*30 سم خامة خشبية متينه جودة أعلى تعلم الطفل العد والارقام والعمليات الحسابية بطريقة ممتعه", "id": "1846"}
                ],
    "choiceType":"ShowRecommendations"

},
{
    "message": {"TextField":"تحب نساعدك بحاجة تاني؟"},
    "elementType": "ChoiceTemplate",
    "choices":  ["نعم"],
    "choiceType":"restart"
},
{
    "message": {"TextField": "متشكر علي تقيمك جدا عشان ده هيساعدني احسن من نفسي "},
    "elementType": "MessageTemplate",
    "choices": [],
    "choiceType":"AfterRestart"
},
]