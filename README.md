pacman_project/
├── config.json              # ملف الإعدادات
├── Makefile                 # يحتوي على (install, run, debug, clean, lint)
├── pyproject.toml / requirements.txt
├── README.md                # باللغة الإنجليزية حسب الشروط
├── .gitignore
├── project_management/      # مجلد التوثيق وإدارة المشروع (Gantt, Risk Analysis...)
└── src/
    ├── __init__.py
    ├── main.py              # نقطة بداية التشغيل (Entry point)
    ├── config_parser.py     # قراءة وتحليل ملف JSON وتجاهل التعليقات (#)
    ├── highscore.py         # نظام حفظ أعلى 10 نتائج
    ├── maze_adapter.py      # الـ Adapter الخاص بمكتبة A-Maze-ing الخارجية
    ├── engine/
    │   ├── game_engine.py   # الحلقة الرئيسية للعبة (Game Loop)
    │   └── state_manager.py # التنقل بين الشاشات (Menu, Game, Pause, GameOver)
    ├── models/
    │   ├── entity.py        # الكائن الأب (Base Entity)
    │   ├── pacman.py        # كائن اللاعب
    │   ├── ghost.py         # كائن الأشباح والذكاء الاصطناعي (AI)
    │   ├── maze.py          # شبكة المتاهة، الجدران، والـ Pacgums
    │   └── game_state.py    # النقاط، الأرواح، الوقت، والـ Cheat Mode
    └── views/
        ├── renderer.py      # رسم العناصر باستخدام المكتبة الرسومية
        └── ui.py            # واجهات المستخدم (القائمة الرئيسية، HUD، النتيجة)
