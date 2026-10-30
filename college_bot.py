#!/usr/bin/env python3
"""
College Information Chatbot (plain Python 3, standard library only)
===================================================================

HOW TO RUN (VS Code)
--------------------
1. Open this file in VS Code (File > Open File...).
2. Press the Run button (top right) or press F5 > "Python File".
   Or open the terminal (Ctrl+`) and run:   python college_bot.py
   (use "python3 college_bot.py" on Mac/Linux)

Type a question and press Enter. Type "help" to see topics, or "quit" /
"exit" to leave.

HOW TO ADD OR UPDATE COLLEGE INFORMATION
----------------------------------------
1. Edit the COLLEGE dictionary below ("EDIT HERE"). Every topic has:
     - "keywords": words/phrases that should trigger that topic
     - "answer":   the text shown to the student
   Replace every placeholder value (the fictional "Riverside Valley College"
   details) with real data.
2. To add a topic (e.g. "scholarships"), copy any existing topic block,
   give it a new key, and fill in its keywords and answer.
3. Optional: put the same structure in a file named college_data.json next
   to this script. If it exists, it replaces the built-in data, so you can
   update information without touching the code.

EXAMPLE QUESTIONS AND SAMPLE OUTPUT
-----------------------------------
    You: What are the admission requirements?
    Bot: Admission requirements: ...

    You: how much is tuition
    Bot: Tuition and fees (per academic year): ...

    You: Where is the campus?
    Bot: Riverside Valley College is located at ...

    You: do you offer on-campus housing
    Bot: Housing: ...

    You: what's the weather like?
    Bot: Sorry, I don't have information on that. Type "help" to see topics.

    You:            (empty input)
    Bot: Please type a question, or "help" to see what I can answer.
"""

import json
import os
import re

# ---------------------------------------------------------------------------
# EDIT HERE: college information (all values below are fictional placeholders)
# ---------------------------------------------------------------------------
COLLEGE = {
    "name": "Riverside Valley College",
    "topics": {
        "admissions": {
            "keywords": ["admission", "admit", "apply", "application",
                         "requirement", "eligibility", "gpa", "sat", "act",
                         "how to apply"],
            "answer": (
                "Admission requirements:\n"
                "  - Completed online application and ₹500 fee\n"
                "  - High school transcript (minimum 3.0 GPA recommended)\n"
                "  - SAT/ACT scores are optional\n"
                "  - One letter of recommendation and a short personal essay"
            ),
        },
        "tuition": {
            "keywords": ["tuition", "fee", "cost", "price", "expensive",
                         "how much", "afford",
                         "charge", "payment", "pay", "installment", "refund",
                         "semester fee", "course fee", "tuition fee",
                         "fee structure", "fee detail"],
            "answer": (
                "Fee details (per academic year):\n"
                "Tuition by program:\n"
                "  - B.Tech (Computer Science / IT): ₹1,85,000\n"
                "  - BBA: ₹1,20,000\n"
                "  - B.Sc Nursing: ₹1,40,000\n"
                "  - B.Des (Graphic Design): ₹1,60,000\n"
                "Other charges (all programs):\n"
                "  - Student/activity fees: ₹12,000\n"
                "  - Exam fees: ₹6,000\n"
                "  - Books and supplies (estimate): ₹9,000\n"
                "Hostel (optional): room ₹90,000 + mess ₹48,000\n"
                "Transport (optional): ₹18,000 to ₹36,000 by distance\n"
                "Payment: two installments (June 15 and December 15).\n"
                "Refunds: full refund of tuition before July 1; none after.\n"
                "Scholarships and financial aid: see the Financial Aid Office."
            ),
        },
        "programs": {
            "keywords": ["major", "program", "course", "degree", "study",
                         "department", "subject", "offer", "computer science",
                         "business", "nursing"],
            "answer": (
                "Popular majors and programs:\n"
                "  - Computer Science (B.S.)\n"
                "  - Business Administration (B.B.A.)\n"
                "  - Nursing (B.S.N.)\n"
                "  - Environmental Science (B.S.)\n"
                "  - Graphic Design (B.F.A.)"
            ),
        },
        "location": {
            "keywords": ["location", "located", "where", "address", "campus",
                         "directions", "city", "map", "find you"],
            "answer": (
                "Riverside Valley College is located at 123 College Avenue, "
                "Springfield, ST 12345. The main campus is 10 minutes from "
                "downtown and is served by city bus routes 4 and 12."
            ),
        },
        "deadlines": {
            "keywords": ["deadline", "due", "date", "when", "early decision",
                         "regular decision", "last day"],
            "answer": (
                "Key application deadlines:\n"
                "  - Early Decision: November 15\n"
                "  - Regular Decision: February 1\n"
                "  - Financial aid (FAFSA) priority: March 1\n"
                "  - Enrollment deposit: May 1"
            ),
        },
        "housing": {
            "keywords": ["housing", "dorm", "residence", "live", "room",
                         "accommodation", "on-campus", "off-campus",
                         "roommate", "hostel", "hostel fee", "room rent",
                         "mess fee"],
            "answer": (
                "Housing:\n"
                "  - First-year students live in on-campus residence halls\n"
                "  - Single and double rooms; about ₹90,000 per year\n"
                "  - Meal plans are available\n"
                "  - Apply for housing by June 1 through the student portal"
            ),
        },
        "contact": {
            "keywords": ["contact", "phone", "email", "call", "reach",
                         "office", "talk to", "speak", "email address", "phone number", "contact number"],
            "answer": (
                "Contact the Admissions Office:\n"
                "  - Phone: (555) 010-1234\n"
                "  - Email: admissions@riversidevalley.example\n"
                "  - Website: www.riversidevalley.example\n"
                "  - Hours: Mon-Fri, 9:00 AM - 5:00 PM"
            ),
        },
        "transport": {
            "keywords": ["transport", "bus", "van", "shuttle", "pickup", "drop", "route", "vehicle", "parking", "bike", "travel", "commute", "bus fee", "bus pass", "college bus", "two-wheeler", "how to reach", "reach college", "get to college", "by bus"],
            "answer": (
                "Transport facilities:\n"
                "  - College buses run on 12 routes across the city and nearby towns\n"
                "  - Pickup: 7:00-8:30 AM | Drop: 4:30-6:00 PM\n"
                "Bus fee per year (by distance from campus):\n"
                "  - Up to 10 km: ₹18,000\n"
                "  - 10 to 20 km: ₹24,000\n"
                "  - 20 to 30 km: ₹30,000\n"
                "  - Above 30 km: ₹36,000\n"
                "  - Occasional use (per trip): ₹80\n"
                "  - Pay in two installments along with tuition (June 15 and December 15)\n"
                "Parking on campus:\n"
                "  - Two-wheeler permit: ₹1,000 per year\n"
                "  - Four-wheeler permit: ₹3,000 per year\n"
                "Public buses 4 and 12 also stop at the campus gate (fare about ₹20).\n"
                "Transport office: (555) 010-5678, transport@riversidevalley.example"
            ),
        },
        "facilities": {
            "keywords": ["facility", "library", "lab", "wifi", "internet", "canteen", "cafeteria", "food", "gym", "medical", "hospital", "atm", "amenity", "infrastructure", "computer lab"],
            "answer": (
                "Campus facilities:\n"
                "  - Library: 50,000+ books and e-journals, open 8:00 AM - 8:00 PM\n"
                "  - Labs: computer, electronics and design labs with modern equipment\n"
                "  - Wi-Fi across the whole campus, free for students\n"
                "  - Canteen: meals from ₹60 to ₹120\n"
                "  - Gym, playground, cricket and basketball courts\n"
                "  - Medical room with a visiting doctor on weekdays\n"
                "  - ATM and stationery shop on campus"
            ),
        },
        "placements": {
            "keywords": ["placement", "job", "recruiter", "package", "salary", "internship", "career", "company", "hiring", "lpa", "campus drive"],
            "answer": (
                "Placements and internships:\n"
                "  - About 85% of eligible students placed last year\n"
                "  - Highest package: ₹12 LPA | Average package: ₹4.5 LPA\n"
                "  - 60+ recruiters visit every year (IT, finance, core engineering)\n"
                "  - Internships in the 3rd year; training starts from the 2nd year\n"
                "  - Resume workshops, mock interviews and aptitude training\n"
                "  - Placement cell: placements@riversidevalley.example"
            ),
        },
        "scholarships": {
            "keywords": ["scholarship", "financial aid", "merit", "concession", "waiver", "grant", "bursary", "discount", "free seat"],
            "answer": (
                "Scholarships and financial aid:\n"
                "  - Merit: 50% tuition waiver for 95%+ in 12th grade; 25% for 90-95%\n"
                "  - Government scholarships available as per state rules\n"
                "  - Sports and cultural achievement concessions\n"
                "  - Education loan help through partner banks\n"
                "  - Apply by March 1 at the Financial Aid Office"
            ),
        },
        "activities": {
            "keywords": ["club", "event", "fest", "sport", "activity", "extracurricular", "cultural", "symposium", "nss", "hackathon", "student life"],
            "answer": (
                "Student life:\n"
                "  - Clubs: Coding, Robotics, Music, Drama, Photography, Entrepreneurship\n"
                "  - Annual cultural fest in February; tech symposium in September\n"
                "  - Hackathons and workshops every semester\n"
                "  - NSS and community service programs\n"
                "  - Inter-college sports meet every December"
            ),
        },
        "about": {
            "keywords": ["about us", "about the college", "about college", "history", "established", "accredit", "naac", "nirf", "ranking", "affiliation", "overview", "aicte"],
            "answer": (
                "About Riverside Valley College:\n"
                "  - Established in 1998, affiliated to Springfield State University\n"
                "  - Approved by AICTE; NAAC 'A' grade accredited\n"
                "  - 4,500 students and 250 faculty members on a 30-acre campus\n"
                "  - Strong focus on practical learning, projects and industry training"
            ),
        },
    },
}
# ---------------------------------------------------------------------------
# END OF EDITABLE DATA
# ---------------------------------------------------------------------------

# Look for college_data.json next to this script (works no matter which
# folder VS Code's terminal is opened in).
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "college_data.json")
EXIT_COMMANDS = {"quit", "exit", "bye", "q"}
GREETINGS = {"hi", "hello", "hey", "hiya"}
FALLBACK = ('Sorry, I don\'t have information on that. '
            'Type "help" to see the topics I can answer.')


def load_data(path=DATA_FILE):
    """Return college data from the JSON file if present, else the built-in dict."""
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as err:
            print(f"(Could not read {path}: {err}. Using built-in data.)")
    return COLLEGE


def stem(word):
    """Very light plural stripping so 'fees' matches 'fee' and 'majors' matches 'major'."""
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def tokenize(text):
    """Lowercase text and return a list of simplified word tokens."""
    return [stem(w) for w in re.findall(r"[a-z0-9\-]+", text.lower())]


def edit_distance(a, b):
    """Return the Levenshtein distance between two short words."""
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def word_matches(keyword, tokens):
    """True if keyword is in tokens exactly, or within 1 typo for words of 5+ letters."""
    if keyword in tokens:
        return True
    return len(keyword) >= 5 and any(
        abs(len(t) - len(keyword)) <= 1 and edit_distance(t, keyword) <= 1
        for t in tokens)


def score_topic(question_tokens, topic):
    """Score a topic: +1 per matching keyword, +2 per matching multi-word phrase."""
    joined = " " + " ".join(question_tokens) + " "
    token_set = set(question_tokens)
    score = 0
    for keyword in topic["keywords"]:
        kw_tokens = tokenize(keyword)
        if len(kw_tokens) > 1:
            if " " + " ".join(kw_tokens) + " " in joined:
                score += 2
        elif kw_tokens and word_matches(kw_tokens[0], token_set):
            score += 1
    return score


def find_best_topic(question, topics):
    """Return the key of the best-matching topic, or None if nothing matches."""
    tokens = tokenize(question)
    best_key, best_score = None, 0
    for key, topic in topics.items():
        score = score_topic(tokens, topic)
        if score > best_score:
            best_key, best_score = key, score
    return best_key


def help_text(data):
    """Return a list of available topics with a sample question style."""
    names = ", ".join(data["topics"].keys())
    return (f"I can answer questions about: {names}.\n"
            'Try: "What are the admission requirements?" or "How much is tuition?"')


def get_answer(question, data):
    """Return the chatbot's reply for a single user question."""
    question = question.strip()
    if not question:
        return 'Please type a question, or "help" to see what I can answer.'

    lowered = question.lower().strip("!?. ")
    if lowered in GREETINGS:
        return f"Hello! Ask me anything about {data['name']}."
    if lowered == "help":
        return help_text(data)

    key = find_best_topic(question, data["topics"])
    return data["topics"][key]["answer"] if key else FALLBACK


def main():
    """Run the terminal chat loop until the user quits."""
    data = load_data()
    print(f"Welcome to the {data['name']} information bot!")
    print('Ask me a question, or type "help". Type "quit" to exit.\n')

    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):  # Ctrl-D / Ctrl-C
            print("\nBot: Goodbye!")
            break

        if user_input.strip().lower() in EXIT_COMMANDS:
            print("Bot: Goodbye! Good luck with your college search.")
            break

        print(f"Bot: {get_answer(user_input, data)}\n")


if __name__ == "__main__":
    main()
