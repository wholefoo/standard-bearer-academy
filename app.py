from flask import Flask, render_template, request, jsonify, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "homeschool-lms-dev-key")

GRADE_LEVELS = {
    "prek": {"name": "Pre-Kindergarten", "short": "PreK", "order": 0},
    "grade1": {"name": "1st Grade", "short": "1st", "order": 1},
    "grade2": {"name": "2nd Grade", "short": "2nd", "order": 2},
    "grade3": {"name": "3rd Grade", "short": "3rd", "order": 3},
    "grade4": {"name": "4th Grade", "short": "4th", "order": 4},
    "grade5": {"name": "5th Grade", "short": "5th", "order": 5},
    "grade6": {"name": "6th Grade", "short": "6th", "order": 6},
    "grade7": {"name": "7th Grade", "short": "7th", "order": 7},
    "grade8": {"name": "8th Grade", "short": "8th", "order": 8},
    "grade9": {"name": "9th Grade", "short": "9th", "order": 9},
    "grade10": {"name": "10th Grade", "short": "10th", "order": 10},
    "grade11": {"name": "11th Grade", "short": "11th", "order": 11},
    "grade12": {"name": "12th Grade", "short": "12th", "order": 12},
}

SUBJECTS = {
    "science": {"name": "Science", "icon": "🔬"},
    "math": {"name": "Mathematics", "icon": "📐"},
    "reading": {"name": "Reading & Language Arts", "icon": "📖"},
    "history": {"name": "History & Social Studies", "icon": "🏛️"},
    "bible": {"name": "Bible & Scripture", "icon": "✝️"},
}

USER_ROLES = {
    "parent": {"name": "Parent / Administrator", "description": "Manage students, view progress, and configure curriculum"},
    "teacher": {"name": "Teacher", "description": "Create lessons, grade assignments, and track student progress"},
    "student": {"name": "Student", "description": "Access lessons, complete quizzes, and track your learning"},
}

GRADE1_SCIENCE_LESSONS = [
    {
        "id": 1,
        "title": "Day 1 — Light: God Creates Light and Separates It from Darkness",
        "scripture": "Genesis 1:3-5",
        "memory_verse": "\"And God said, 'Let there be light,' and there was light.\" — Genesis 1:3 (NIV)",
        "objective": "Students will learn that God created light on the first day and separated it from darkness, establishing day and night.",
        "content": [
            "On the very first day, before anything else existed, God spoke light into being. The Bible tells us, \"And God said, 'Let there be light,' and there was light\" (Genesis 1:3).",
            "God saw that the light was good. He separated the light from the darkness. He called the light \"Day\" and the darkness \"Night.\"",
            "This teaches us that God is powerful — He can create something from nothing, just by speaking! Light was the very first thing God made because He is a God of order and goodness."
        ],
        "activity": "Draw a picture showing one side bright with light (day) and the other side dark (night). Write the memory verse at the top.",
        "discussion": [
            "Why do you think God created light first?",
            "What would the world be like without light?",
            "How does light help us every day?"
        ]
    },
    {
        "id": 2,
        "title": "Day 2 — Sky: God Creates the Expanse (Sky and Atmosphere)",
        "scripture": "Genesis 1:6-8",
        "memory_verse": "\"And God said, 'Let there be a vault between the waters to separate water from water.'\" — Genesis 1:6 (NIV)",
        "objective": "Students will learn that God created the sky and atmosphere on the second day, separating the waters above from the waters below.",
        "content": [
            "On the second day, God made the sky! The Bible calls it an \"expanse\" or \"firmament.\" God placed it between the waters — separating the water in the clouds above from the water on the earth below.",
            "The sky is like a beautiful blanket that God wrapped around the earth. It holds our air so we can breathe, and it protects us from the sun's heat.",
            "God designed the atmosphere perfectly so that life could exist on Earth. This shows us God's wisdom and careful planning."
        ],
        "activity": "Go outside and look up at the sky. Draw what you see — clouds, blue sky, birds flying. Thank God for making the air we breathe.",
        "discussion": [
            "What do you see when you look up at the sky?",
            "Why is the sky important for living things?",
            "How does the sky show God's care for us?"
        ]
    },
    {
        "id": 3,
        "title": "Day 3 — Land, Seas, and Plants: God Gathers Waters and Creates Vegetation",
        "scripture": "Genesis 1:9-13",
        "memory_verse": "\"Then God said, 'Let the land produce vegetation: seed-bearing plants and trees.'\" — Genesis 1:11 (NIV)",
        "objective": "Students will learn that God created dry land, seas, and all plant life on the third day.",
        "content": [
            "On the third day, God gathered the waters together and let dry ground appear. He called the dry ground \"Land\" and the gathered waters \"Seas.\"",
            "Then God filled the land with plants — grasses, flowers, fruit trees, and vegetables. Each plant was created to produce seeds \"according to its kind,\" meaning apple trees always make apples, and oak trees always make acorns.",
            "God designed plants to reproduce after their own kind. This is one of the great wonders of creation — every seed contains a tiny plan to grow into exactly the right kind of plant!"
        ],
        "activity": "Plant a seed in a small cup of soil. Water it and watch it grow over the coming days. Keep a journal of what you observe.",
        "discussion": [
            "What is your favorite plant or flower? Why?",
            "What does 'according to its kind' mean?",
            "How do plants show us God's creativity?"
        ]
    },
    {
        "id": 4,
        "title": "Day 4 — Sun, Moon, and Stars: God Creates the Heavenly Lights",
        "scripture": "Genesis 1:14-19",
        "memory_verse": "\"God made two great lights — the greater light to govern the day and the lesser light to govern the night.\" — Genesis 1:16 (NIV)",
        "objective": "Students will learn that God created the sun, moon, and stars on the fourth day to mark seasons, days, and years.",
        "content": [
            "On the fourth day, God created the sun, moon, and stars! The sun gives us light and warmth during the day. The moon reflects the sun's light and glows softly at night.",
            "God set these lights in the sky for signs, seasons, days, and years. The sun helps us know when it's daytime, and the moon helps us know when it's nighttime. The stars fill the sky with beauty.",
            "God made billions of stars and knows each one by name (Psalm 147:4). If God cares about every single star, imagine how much He cares about you!"
        ],
        "activity": "On a clear night, go outside with your family and look at the stars. Try to count them! Draw the sun, moon, and stars, and label each one.",
        "discussion": [
            "Why did God make the sun and the moon different?",
            "How do we use the sun and moon to tell time and seasons?",
            "What does it mean that God knows every star by name?"
        ]
    },
    {
        "id": 5,
        "title": "Day 5 — Sea Creatures and Birds: God Fills the Waters and Skies",
        "scripture": "Genesis 1:20-23",
        "memory_verse": "\"So God created the great creatures of the sea and every living thing with which the water teems.\" — Genesis 1:21 (NIV)",
        "objective": "Students will learn that God created all sea creatures and birds on the fifth day.",
        "content": [
            "On the fifth day, God filled the oceans with fish, whales, dolphins, and every kind of sea creature. He also filled the skies with birds of every kind — eagles, sparrows, hummingbirds, and more!",
            "God blessed these creatures and told them to \"be fruitful and multiply.\" That means He wanted them to have babies and fill the earth with life.",
            "From the tiniest minnow to the great blue whale, God created each creature with special features. Birds have wings to fly, fish have gills to breathe underwater — each one perfectly designed by God."
        ],
        "activity": "Choose your favorite sea creature and your favorite bird. Draw them and write three facts about each one. How do their special features show God's design?",
        "discussion": [
            "What is the biggest sea creature you can think of? The smallest?",
            "How are birds designed differently from fish?",
            "What does it mean that God 'blessed' the creatures?"
        ]
    },
    {
        "id": 6,
        "title": "Day 6 — Land Animals and Man: God Creates Animals and Mankind in His Image",
        "scripture": "Genesis 1:24-31",
        "memory_verse": "\"So God created mankind in his own image, in the image of God he created them.\" — Genesis 1:27 (NIV)",
        "objective": "Students will learn that God created land animals and mankind on the sixth day, and that humans are uniquely made in God's image.",
        "content": [
            "On the sixth day, God made all the land animals — livestock like cows and sheep, wild animals like lions and bears, and creatures that move along the ground like lizards and rabbits.",
            "Then came God's most special creation: people! God created man and woman in His own image. That means we are made to reflect God's character — we can think, love, create, and know right from wrong.",
            "God gave mankind a special job: to take care of the earth and all its creatures. We are stewards of God's creation. God looked at everything He had made and said it was \"very good!\""
        ],
        "activity": "Make a list of land animals you know. Then draw a picture of Adam and Eve in the Garden of Eden with animals around them.",
        "discussion": [
            "What does it mean to be made 'in God's image'?",
            "How are people different from animals?",
            "What responsibility did God give to mankind?"
        ]
    },
    {
        "id": 7,
        "title": "Day 7 — Rest: God Rests and Makes the Sabbath Holy",
        "scripture": "Genesis 2:1-3",
        "memory_verse": "\"By the seventh day God had finished the work he had been doing; so on the seventh day he rested.\" — Genesis 2:2 (NIV)",
        "objective": "Students will learn that God rested on the seventh day, not because He was tired, but to set an example and make the day holy.",
        "content": [
            "By the seventh day, God had finished creating everything — the heavens, the earth, light, sky, land, plants, sun, moon, stars, sea creatures, birds, land animals, and people. Everything was complete and very good!",
            "On the seventh day, God rested. He wasn't tired — God never gets tired! He rested to show us that rest is important and good. He blessed the seventh day and made it holy.",
            "God set an example for us: we should work hard for six days and then take time to rest, worship, and spend time with God and family. This pattern of work and rest is a gift from our Creator."
        ],
        "activity": "As a family, plan a special restful activity for this week's Sabbath. Make a card thanking God for all seven days of creation.",
        "discussion": [
            "Why did God rest if He wasn't tired?",
            "Why is rest important for us?",
            "How can we make our rest day special and holy?"
        ]
    }
]

QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "What did God create on Day 1?",
        "options": ["Animals", "Light", "Stars", "Plants"],
        "correct": 1,
        "explanation": "God created light on Day 1 and separated it from darkness (Genesis 1:3-5)."
    },
    {
        "id": 2,
        "question": "What did God create on Day 2?",
        "options": ["The Sky (Expanse)", "Fish", "The Sun", "People"],
        "correct": 0,
        "explanation": "God created the sky (expanse/firmament) on Day 2, separating the waters above from the waters below (Genesis 1:6-8)."
    },
    {
        "id": 3,
        "question": "What did God create on Day 3?",
        "options": ["Birds", "Stars", "Land, Seas, and Plants", "Light"],
        "correct": 2,
        "explanation": "God created dry land, seas, and all vegetation on Day 3 (Genesis 1:9-13)."
    },
    {
        "id": 4,
        "question": "What did God create on Day 4?",
        "options": ["Sky", "Sun, Moon, and Stars", "Animals", "People"],
        "correct": 1,
        "explanation": "God created the sun, moon, and stars on Day 4 to govern day and night and to mark seasons (Genesis 1:14-19)."
    },
    {
        "id": 5,
        "question": "What did God create on Day 5?",
        "options": ["Land Animals", "Plants", "Sea Creatures and Birds", "Light"],
        "correct": 2,
        "explanation": "God created all sea creatures and birds on Day 5 (Genesis 1:20-23)."
    },
    {
        "id": 6,
        "question": "What makes humans special compared to the rest of creation?",
        "options": [
            "Humans are bigger than animals",
            "Humans were made in God's image",
            "Humans were created first",
            "Humans can swim"
        ],
        "correct": 1,
        "explanation": "Humans are uniquely made in God's image, meaning we can think, love, create, and have a relationship with God (Genesis 1:27)."
    },
    {
        "id": 7,
        "question": "Why did God rest on Day 7?",
        "options": [
            "He was tired from all the work",
            "He ran out of things to create",
            "To set an example and make the day holy",
            "He needed to sleep"
        ],
        "correct": 2,
        "explanation": "God rested on Day 7 not because He was tired, but to bless the day, make it holy, and set an example of rest for us (Genesis 2:2-3)."
    },
    {
        "id": 8,
        "question": "According to Genesis 1:11, plants were created to reproduce how?",
        "options": [
            "By evolving over millions of years",
            "According to their kind",
            "Randomly without any pattern",
            "By changing into new types of plants"
        ],
        "correct": 1,
        "explanation": "God designed each plant to produce seeds 'according to its kind' — apple trees always produce apples, oak trees always produce acorns (Genesis 1:11)."
    },
    {
        "id": 9,
        "question": "How many days did it take God to create everything?",
        "options": ["5 days", "6 days", "7 days", "Millions of years"],
        "correct": 1,
        "explanation": "God created everything in 6 days and rested on the 7th day (Genesis 2:1-3). Creation was complete in six literal days."
    },
    {
        "id": 10,
        "question": "What did God say when He looked at everything He had made?",
        "options": [
            "It was okay",
            "It needed more work",
            "It was very good",
            "It was almost done"
        ],
        "correct": 2,
        "explanation": "After creating mankind on Day 6, God looked at all He had made and declared it 'very good' (Genesis 1:31)."
    }
]


@app.route("/")
def homepage():
    return render_template("index.html", roles=USER_ROLES, grades=GRADE_LEVELS, subjects=SUBJECTS)


@app.route("/dashboard")
def dashboard():
    role = request.args.get("role", "parent")
    if role not in USER_ROLES:
        role = "parent"
    return render_template("dashboard.html", role=role, roles=USER_ROLES, grades=GRADE_LEVELS, subjects=SUBJECTS)


@app.route("/course/<grade>/<subject>")
def course(grade, subject):
    grade_info = GRADE_LEVELS.get(grade)
    subject_info = SUBJECTS.get(subject)
    if not grade_info or not subject_info:
        return redirect(url_for("dashboard"))

    lessons = []
    if grade == "grade1" and subject == "science":
        lessons = GRADE1_SCIENCE_LESSONS

    return render_template("course.html", grade=grade, grade_info=grade_info,
                           subject=subject, subject_info=subject_info, lessons=lessons)


@app.route("/lesson/<grade>/<subject>/<int:lesson_id>")
def lesson(grade, subject, lesson_id):
    if grade == "grade1" and subject == "science":
        lesson_data = next((l for l in GRADE1_SCIENCE_LESSONS if l["id"] == lesson_id), None)
        if lesson_data:
            return render_template("lesson.html", lesson=lesson_data,
                                   grade=grade, subject=subject,
                                   grade_info=GRADE_LEVELS[grade],
                                   subject_info=SUBJECTS[subject])
    return redirect(url_for("course", grade=grade, subject=subject))


@app.route("/quiz/<grade>/<subject>")
def quiz(grade, subject):
    grade_info = GRADE_LEVELS.get(grade)
    subject_info = SUBJECTS.get(subject)
    if grade == "grade1" and subject == "science":
        return render_template("quiz.html", questions=QUIZ_QUESTIONS,
                               grade=grade, subject=subject,
                               grade_info=grade_info, subject_info=subject_info)
    return redirect(url_for("course", grade=grade, subject=subject))


@app.route("/api/quiz/submit", methods=["POST"])
def submit_quiz():
    data = request.get_json()
    answers = data.get("answers", {})
    results = []
    score = 0
    total = len(QUIZ_QUESTIONS)

    for q in QUIZ_QUESTIONS:
        user_answer = answers.get(str(q["id"]))
        is_correct = user_answer == q["correct"]
        if is_correct:
            score += 1
        results.append({
            "id": q["id"],
            "correct": is_correct,
            "correct_answer": q["correct"],
            "user_answer": user_answer,
            "explanation": q["explanation"]
        })

    return jsonify({
        "score": score,
        "total": total,
        "percentage": round((score / total) * 100) if total > 0 else 0,
        "results": results
    })


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
