# Standard Bearer Academy — K-12 Homeschool LMS

## Overview
A comprehensive K-12 Homeschool Resource Platform built with Python/Flask. The platform hosts 115 courses spanning PreK through 12th Grade across 10 subjects (6 core + Art & Science Projects for PreK-8, Technology and Creative Writing for grades 6-12, Life Skills for grades 6-12), all from a conservative, Judeo-Evangelical Christian, and Creation-based (Young Earth/Biblical) worldview.

## Architecture
- **Backend**: Python 3.11 + Flask
- **Database**: PostgreSQL (stores student progress, quiz scores)
- **Content**: 905 JSON files in `lessons/` directory (file-based curriculum)
- **Frontend**: Jinja2 templates with vanilla CSS/JS
- **Server**: Flask dev server on port 5000

## File Structure
```
app.py                      # Main Flask application with routes
content_loader.py           # JSON file-based curriculum content loader
db.py                       # Database utilities for progress/quiz tracking
lessons/                    # All curriculum content as JSON files
  prek/{bible,science,math,reading,history,civics,art_science_projects}/
  kindergarten/{bible,science,math,reading,history,civics,art_science_projects}/
  grade1-grade5/{science,math,reading,history,bible,civics,art_science_projects}/
  grade6-grade8/{science,math,reading,history,bible,civics,technology,creative_writing,life_skills,art_science_projects}/
  grade9-grade12/{science,math,reading,history,bible,civics,technology,creative_writing,life_skills}/
templates/
  base.html                 # Base template with header, nav, footer
  index.html                # Homepage with role selection
  dashboard.html            # Course Dashboard with available courses
  course.html               # Course page listing lessons (generic)
  lesson.html               # Lesson detail for elementary (memory verse, activity)
  lesson_civics.html        # Lesson detail for middle/high school (scripture sidebar, reflection)
  quiz.html                 # Interactive quiz with scoring
static/
  css/style.css             # All styles
```

## Database Schema (PostgreSQL)
- **students**: id, username, display_name, role, created_at
- **completed_lessons**: student_id, grade, subject, unit, lesson_id, completed_at
- **quiz_scores**: student_id, grade, subject, unit, quiz_id, score, total, percentage, answers (JSONB)

## Complete Course Catalog (115 courses)

### PreK (ages 3-5)
- Bible: Bible ABCs — Learning Letters Through Scripture
- Science: God's Beautiful World — Exploring Creation
- Math: Counting God's Blessings — Numbers and Shapes
- Reading: God's Word ABCs — Learning to Read with Scripture
- History: Heroes of the Bible — Stories of Faith and Courage
- Civics: God's Rules — Learning Right from Wrong
- Art & Science Projects: Little Creators — Exploring God's World Through Art and Play

### Kindergarten (ages 5-6)
- Bible: God's Numbers — Counting Through Scripture
- Science: Seasons and Weather — God's Amazing Design
- Math: God's Patterns — Shapes, Colors, and Counting to 20
- Reading: Reading God's Word — Phonics and Bible Stories
- History: Our Country — America the Beautiful
- Civics: Being a Good Helper — Rules and Responsibilities
- Art & Science Projects: God's Colorful World — Art and Discovery for Little Hands

### 1st Grade (ages 6-7)
- Science: The Days of Creation
- Math: God's Numbers — Addition and Subtraction
- Reading: Reading with Purpose — Phonics and Comprehension
- History: American Heroes — Leaders Who Trusted God
- Bible: The Life of Jesus — Stories from the Gospels
- Civics: My Community — Rules, Leaders, and Helpers
- Art & Science Projects: Creation Station — Hands-On Art and Science

### 2nd Grade (ages 7-8)
- Science: God's Amazing Animals
- Math: Building with Numbers — Place Value and Measurement
- Reading: Growing in Reading — Fluency and Bible Stories
- History: Pilgrims and Patriots — America's Early Days
- Bible: Old Testament Adventures — From Noah to David
- Civics: Our Nation — Symbols, Laws, and Freedom
- Art & Science Projects: Explore and Create — Science Experiments and Art Projects

### 3rd Grade (ages 8-9)
- Science: Plants and Ecosystems — God's Green Earth
- Math: Multiplication and Division — God's Order in Numbers
- Reading: Stories of Faith — Reading and Writing with Purpose
- History: Explorers and Settlers — God's Hand in the New World
- Bible: Kings and Prophets — God's Faithful Servants
- Civics: We the People — Our Government and Constitution
- Art & Science Projects: The Inventor's Workshop — Building and Discovering

### 4th Grade (ages 9-10)
- Science: Astronomy — The Heavens Declare God's Glory
- Math: Fractions and Decimals — Parts of God's Whole
- Reading: Great Stories of Faith — Reading and Writing
- History: America's Godly Heritage — From Columbus to the Constitution
- Bible: The Early Church — Acts of the Apostles
- Civics: Rights and Responsibilities — Being a Good Citizen
- Art & Science Projects: Design and Discover — Engineering and Art Challenges

### 5th Grade (ages 10-11)
- Science: The Human Body — Fearfully and Wonderfully Made
- Math: Pre-Algebra Foundations — Order in God's Creation
- Reading: Literature and Composition — Writing for God's Glory
- History: Westward Expansion — America Grows Under Providence
- Bible: Wisdom Literature — Psalms, Proverbs, and Ecclesiastes
- Civics: The Three Branches — How Our Government Works
- Art & Science Projects: The Creator's Lab — Advanced Projects and Experiments

### 6th Grade (ages 11-12) — Middle School Format
- Science: Life Science — The Miracle of Living Things
- Math: Ratios and Proportions — God's Mathematical Design
- Reading: World Literature — Stories of Faith Across Cultures
- History: Ancient Civilizations — God's Hand in History
- Bible: The Gospels — Walking with Jesus
- Civics: Ancient to Modern Government — God's Design for Order
- Technology: Digital Foundations — Technology as a Tool for God's Kingdom
- Creative Writing: The Gift of Words — Writing to Glorify God
- Life Skills: Foundations for Life — Building Good Habits God's Way
- Art & Science Projects: STEAM Explorations — Where Faith Meets Innovation

### 7th Grade (ages 12-13)
- Science: Earth Science — Exploring God's World
- Math: Pre-Algebra — Foundations of Mathematical Thinking
- Reading: Poetry and Prose — The Beauty of Language
- History: The Medieval World — Christianity and Civilization
- Bible: Paul's Letters — Doctrine and Daily Living
- Civics: American Government — The Constitution in Action
- Technology: Web and Media Literacy — Navigating the Digital World Wisely
- Creative Writing: Stories of Virtue — Crafting Fiction with Purpose
- Life Skills: Home Economics — Caring for God's Household
- Art & Science Projects: Design Thinking — Solving Problems God's Way

### 8th Grade (ages 13-14)
- Science: Physical Science — Laws of the Creator
- Math: Algebra I — Patterns in God's Creation
- Reading: Rhetoric and Persuasion — Speaking Truth
- History: American History — Providence and Liberty
- Bible: Old Testament Survey — God's Covenant Story
- Civics: Citizenship and Law — Biblical Justice in America
- Technology: Introduction to Programming — Building with Logic and Order
- Creative Writing: The Writer's Workshop — Finding Your Voice for Truth
- Life Skills: Financial Foundations — Biblical Stewardship of Money
- Art & Science Projects: Applied Science and Art — Preparing for High School

### 9th Grade (ages 14-15) — High School Format
- Science: Biology — The Design of Life
- Math: Geometry — The Architecture of Creation
- Reading: World Literature — A Christian Perspective
- History: Ancient & Medieval History — The Story of Civilization
- Bible: New Testament Survey — The Gospel and the Church
- Civics: Civics & Government — Foundations of Liberty
- Technology: Computer Science Foundations — Order in God's Digital Creation
- Creative Writing: Narrative and Imagination — Writing Stories that Matter
- Life Skills: Health and Wellness — Honoring God with Your Body

### 10th Grade (ages 15-16)
- Science: Chemistry — The Elements of Creation
- Math: Algebra II — Advanced Patterns in God's Design
- Reading: British Literature — Faith in the English Tradition
- History: World History — The Unfolding of God's Plan
- Bible: Christian Apologetics — Defending the Faith
- Civics: Comparative Government — Liberty vs. Tyranny
- Technology: Cybersecurity and Ethics — Guarding Truth in a Digital Age
- Creative Writing: Poetry and the Soul — Expressing Faith Through Verse
- Life Skills: Career Exploration — Finding Your God-Given Calling

### 11th Grade (ages 16-17)
- Science: Physics — The Laws God Wrote
- Math: Pre-Calculus — Mathematics and the Mind of God
- Reading: American Literature — Faith, Freedom, and the Written Word
- History: U.S. History — One Nation Under God
- Bible: Worldview Studies — Biblical vs. Secular Thinking
- Civics: Constitutional Law — Original Intent and Application
- Technology: Data Science and Society — Understanding God's World Through Data
- Creative Writing: Advanced Fiction — The Art of the Christian Novel
- Life Skills: Personal Finance — Managing God's Resources Wisely

### 12th Grade (ages 17-18)
- Science: Environmental Science — Stewardship of God's Earth
- Math: Statistics and Probability — Understanding God's World
- Reading: Senior Thesis and Composition — Writing with Conviction
- History: Modern World History — The 20th Century and Beyond
- Bible: Senior Capstone — A Biblical Worldview for Life
- Civics: Economics & Free Enterprise — Biblical Stewardship
- Technology: Artificial Intelligence and Ethics — Wisdom for the Age of Machines
- Creative Writing: Senior Portfolio — A Legacy of Words
- Life Skills: Independent Living — Launching with Faith and Confidence

## Content System
Lessons stored as JSON in `lessons/<grade>/<subject>/`. Each course has:
- `course.json`: metadata, unit structure, quiz references
- Individual lesson JSON files
- Quiz JSON files with questions and explanations

**Elementary format** (PreK-5): memory_verse, objective, content (string array), activity, discussion
**Middle/High school format** (6-12): scripture_connection (verses array), content (heading/paragraphs), reflection_questions, key_concepts, primary_source

Template routing: lessons with `scripture_connection` field use `lesson_civics.html`; others use `lesson.html`.

To add new courses: create directory under `lessons/`, add `course.json` and lesson files. App auto-discovers.

## Grade Levels
GRADE_LEVELS in app.py: prek, kindergarten, grade1-grade12 (15 levels total)

## Worldview Filter
- **Science**: Creationist/YEC, intelligent design, literal Genesis
- **Math**: Standard curriculum with Biblical stewardship applications
- **Reading/Literature**: Biblical values, Christian literary analysis, phonics-based
- **History**: Providential history, Western Civilization, American Exceptionalism
- **Bible**: Direct Scripture study, age-appropriate, Old and New Testament
- **Civics**: Constitutional originalism, Biblical basis for government, limited government
- **Economics**: Free market from Biblical stewardship perspective
- **Technology**: Digital citizenship, programming, cybersecurity, AI — Biblical stewardship of tools, responsible use
- **Creative Writing**: Fiction, poetry, nonfiction — writing as worship, storytelling to glorify God
- **Life Skills**: Financial literacy, home economics, career prep, independent living — Biblical stewardship of practical life
- **Art & Science Projects**: Hands-on STEAM projects, experiments, crafts — exploring God's creation through creative discovery

## Running the App
```
python app.py
```
Runs on port 5000.
