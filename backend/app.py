import random
import re
import os
from typing import List, Pattern, Tuple

from flask import Flask, jsonify, request
from flask_cors import CORS


class ElizaBot:
    def __init__(self) -> None:
        self.reflections = {
            "am": "are",
            "was": "were",
            "i": "you",
            "i'd": "you would",
            "i've": "you have",
            "i'll": "you will",
            "my": "your",
            "are": "am",
            "you've": "I have",
            "you'll": "I will",
            "your": "my",
            "yours": "mine",
            "you": "me",
            "me": "you",
        }

        self.rules: List[Tuple[Pattern[str], List[str]]] = [
            (re.compile(r"^hello$", re.IGNORECASE), [
                "Hello. How are you feeling today?",
                "Hi there. What would you like to talk about?",
            ]),
            (re.compile(r"^hi$", re.IGNORECASE), [
                "Hi. What is on your mind?",
                "Hello. Tell me what brought you here.",
            ]),
            (re.compile(r"^hey$", re.IGNORECASE), [
                "Hey. How have things been lately?",
                "Hello. What are you thinking about right now?",
            ]),
            (re.compile(r"^good morning$", re.IGNORECASE), [
                "Good morning. How are you starting your day?",
                "Morning. What is the first thing on your mind today?",
            ]),
            (re.compile(r".*\bi need (.*)", re.IGNORECASE), [
                "Why do you need {1}?",
                "Would it really help you to get {1}?",
                "What would it mean for you to have {1}?",
            ]),
            (re.compile(r".*\bi want (.*)", re.IGNORECASE), [
                "What would it mean if you got {1}?",
                "Why do you want {1}?",
                "What is stopping you from getting {1}?",
            ]),
            (re.compile(r".*\bi wish (.*)", re.IGNORECASE), [
                "What does that wish tell you about your needs?",
                "How long have you wished {1}?",
                "What feelings come up when you think about {1}?",
            ]),
            (re.compile(r".*\bi am (.*)", re.IGNORECASE), [
                "How long have you been {1}?",
                "How do you feel about being {1}?",
                "What makes you think you are {1}?",
            ]),
            (re.compile(r".*\bi'm (.*)", re.IGNORECASE), [
                "How long have you been {1}?",
                "How does being {1} affect you?",
                "What leads you to say you are {1}?",
            ]),
            (re.compile(r".*\bi feel (.*)", re.IGNORECASE), [
                "Tell me more about feeling {1}.",
                "When do you usually feel {1}?",
                "What do you think causes that feeling of {1}?",
            ]),
            (re.compile(r".*\bi felt (.*)", re.IGNORECASE), [
                "When did you first feel {1}?",
                "What was happening when you felt {1}?",
                "How do you feel about having felt {1}?",
            ]),
            (re.compile(r".*\bi think (.*)", re.IGNORECASE), [
                "What makes you think {1}?",
                "Do you often think {1}?",
                "How certain are you that {1}?",
            ]),
            (re.compile(r".*\bi believe (.*)", re.IGNORECASE), [
                "What leads you to believe {1}?",
                "Has that belief changed over time?",
                "How strongly do you believe {1}?",
            ]),
            (re.compile(r".*\bi remember (.*)", re.IGNORECASE), [
                "What else do you remember about {1}?",
                "How does remembering {1} make you feel?",
                "Why do you think that memory stands out?",
            ]),
            (re.compile(r".*\bi forgot (.*)", re.IGNORECASE), [
                "What might forgetting {1} suggest?",
                "Do you often forget things like {1}?",
                "How do you feel when you forget {1}?",
            ]),
            (re.compile(r".*\bi can't (.*)", re.IGNORECASE), [
                "What makes you think you cannot {1}?",
                "Have you tried to {1} before?",
                "What would need to change so you could {1}?",
            ]),
            (re.compile(r".*\bi can (.*)", re.IGNORECASE), [
                "What helps you to {1}?",
                "How long have you been able to {1}?",
                "How does being able to {1} affect you?",
            ]),
            (re.compile(r".*\bi don't (.*)", re.IGNORECASE), [
                "Why do you not {1}?",
                "What would happen if you did {1}?",
                "Have you always felt that you should not {1}?",
            ]),
            (re.compile(r".*\bi do (.*)", re.IGNORECASE), [
                "What makes you do {1}?",
                "How do you feel when you do {1}?",
                "What does doing {1} do for you?",
            ]),
            (re.compile(r".*\bi like (.*)", re.IGNORECASE), [
                "What do you like most about {1}?",
                "When did you first start liking {1}?",
                "How does {1} make you feel?",
            ]),
            (re.compile(r".*\bi dislike (.*)", re.IGNORECASE), [
                "What bothers you about {1}?",
                "Have you always disliked {1}?",
                "What feeling comes up around {1}?",
            ]),
            (re.compile(r".*\bi love (.*)", re.IGNORECASE), [
                "What do you love about {1}?",
                "How does loving {1} affect your life?",
                "When did you realize you loved {1}?",
            ]),
            (re.compile(r".*\bi hate (.*)", re.IGNORECASE), [
                "What makes you hate {1}?",
                "What feelings are underneath that hatred of {1}?",
                "How do you usually react when {1} comes up?",
            ]),
            (re.compile(r".*\b(i'm sorry)\b.*", re.IGNORECASE), [
                "What are you apologizing for?",
                "It is okay to make mistakes. Tell me more.",
                "How does apologizing make you feel?",
            ]),
            (re.compile(r".*\b(sorry)\b.*", re.IGNORECASE), [
                "No need to apologize. What are you feeling?",
                "Apologies are not required here. Please continue.",
                "What led you to say sorry?",
            ]),
            (re.compile(r".*\b(because) (.*)", re.IGNORECASE), [
                "Is that the real reason?",
                "Are there any other reasons?",
                "How convincing does that reason feel to you?",
            ]),
            (re.compile(r".*\b(yes)\b.*", re.IGNORECASE), [
                "You seem quite sure.",
                "I see. Can you elaborate?",
                "What makes you so certain?",
            ]),
            (re.compile(r".*\b(no)\b.*", re.IGNORECASE), [
                "Why not?",
                "What makes you say no?",
                "How certain are you about that?",
            ]),
            (re.compile(r".*\b(maybe)\b.*", re.IGNORECASE), [
                "What keeps you uncertain?",
                "What would help you decide?",
                "What possibilities are you considering?",
            ]),
            (re.compile(r".*\b(always)\b.*", re.IGNORECASE), [
                "Can you think of a specific example?",
                "Really always?",
                "What makes it feel constant?",
            ]),
            (re.compile(r".*\b(never)\b.*", re.IGNORECASE), [
                "Never is a strong word. Can you recall one exception?",
                "Why do you think it never happens?",
                "How long has it felt like never?",
            ]),
            (re.compile(r".*\bmy mother (.*)", re.IGNORECASE), [
                "Tell me more about your mother.",
                "How is your relationship with your mother?",
                "How does your mother relate to {1}?",
            ]),
            (re.compile(r".*\bmy father (.*)", re.IGNORECASE), [
                "Tell me more about your father.",
                "How is your relationship with your father?",
                "How does your father relate to {1}?",
            ]),
            (re.compile(r".*\bmy family (.*)", re.IGNORECASE), [
                "Who in your family is most connected to this?",
                "How does your family affect {1}?",
                "What role does your family play here?",
            ]),
            (re.compile(r".*\bmy friend (.*)", re.IGNORECASE), [
                "Tell me more about your friend.",
                "What does this friend mean to you?",
                "How does your friend connect to {1}?",
            ]),
            (re.compile(r".*\bmy job (.*)", re.IGNORECASE), [
                "How do you feel about your job?",
                "What part of your job matters most to you?",
                "How does your job affect {1}?",
            ]),
            (re.compile(r".*\bschool (.*)", re.IGNORECASE), [
                "What is your experience with school like?",
                "How do you feel when you think about school?",
                "How does school relate to {1}?",
            ]),
            (re.compile(r".*\b(stress|stressed)\b(.*)", re.IGNORECASE), [
                "What contributes most to your stress?",
                "How do you cope when you feel stressed?",
                "What would reduce your stress right now?",
            ]),
            (re.compile(r".*\b(anxious|anxiety)\b(.*)", re.IGNORECASE), [
                "When do you feel most anxious?",
                "What thoughts come with your anxiety?",
                "What helps when anxiety shows up?",
            ]),
            (re.compile(r".*\b(sad|down|depressed)\b(.*)", re.IGNORECASE), [
                "I am sorry you are feeling low. Tell me more.",
                "What seems linked to those feelings?",
                "What helps even a little when you feel this way?",
            ]),
            (re.compile(r".*\b(angry|mad|furious)\b(.*)", re.IGNORECASE), [
                "What triggered that anger?",
                "How do you express anger?",
                "What is beneath the anger for you?",
            ]),
            (re.compile(r".*\b(happy|joyful|excited)\b(.*)", re.IGNORECASE), [
                "That sounds positive. What is going well?",
                "What is making you feel that way?",
                "How can you keep that feeling going?",
            ]),
            (re.compile(r".*\b(tired|exhausted)\b(.*)", re.IGNORECASE), [
                "What has been draining your energy?",
                "How has being tired affected your day?",
                "What kind of rest do you need most?",
            ]),
            (re.compile(r".*\b(lonely|alone)\b(.*)", re.IGNORECASE), [
                "When do you feel most alone?",
                "Who do you wish you could connect with?",
                "What does loneliness feel like for you?",
            ]),
            (re.compile(r".*\b(help)\b(.*)", re.IGNORECASE), [
                "What kind of help are you looking for?",
                "Who do you usually turn to for help?",
                "What would useful help look like right now?",
            ]),
            (re.compile(r".*\bwhy can't i (.*)", re.IGNORECASE), [
                "What do you think prevents you from {1}?",
                "What have you tried so far to {1}?",
                "If you could {1}, what would change?",
            ]),
            (re.compile(r".*\bwhy don't you (.*)", re.IGNORECASE), [
                "What makes you ask me that?",
                "Would you like me to {1}?",
                "What would it mean if I did {1}?",
            ]),
            (re.compile(r".*\bcan you (.*)", re.IGNORECASE), [
                "What makes you think I can {1}?",
                "If I could {1}, how would that help?",
                "Why is my ability to {1} important to you?",
            ]),
            (re.compile(r".*\bcould you (.*)", re.IGNORECASE), [
                "What would it mean if I could {1}?",
                "Why do you ask whether I could {1}?",
                "How would you feel if I could {1}?",
            ]),
            (re.compile(r".*\b(what)\b(.*)", re.IGNORECASE), [
                "What do you think?",
                "What answer are you hoping for?",
                "How would you answer that yourself?",
            ]),
            (re.compile(r".*\b(how)\b(.*)", re.IGNORECASE), [
                "How do you imagine?",
                "What possibilities do you see?",
                "How have you approached this before?",
            ]),
            (re.compile(r".*\b(who)\b(.*)", re.IGNORECASE), [
                "Who comes to mind first?",
                "Who matters most in this situation?",
                "Who do you wish would understand?",
            ]),
            (re.compile(r".*\b(where)\b(.*)", re.IGNORECASE), [
                "Where do you think this started?",
                "What place feels important here?",
                "Where do you feel most like yourself?",
            ]),
            (re.compile(r".*\b(when)\b(.*)", re.IGNORECASE), [
                "When did you first notice this?",
                "What is significant about that time?",
                "When are things easiest for you?",
            ]),
            (re.compile(r".*\b(quit|exit|bye|goodbye)\b.*", re.IGNORECASE), [
                "Goodbye. Thank you for sharing.",
                "Take care. We can talk again anytime.",
                "Goodbye. I appreciate the conversation.",
            ]),
        ]

        if len(self.rules) != 55:
            raise ValueError(f"Expected 55 regex rules, found {len(self.rules)}")

        self.default_responses = [
            "Please tell me more.",
            "Can you say more about that?",
            "How does that make you feel?",
            "What does that suggest to you?",
        ]

    def _reflect(self, fragment: str) -> str:
        words = fragment.lower().split()
        reflected = [self.reflections.get(word, word) for word in words]
        return " ".join(reflected)

    def _substitute_groups(self, template: str, match: re.Match[str]) -> str:
        result = template
        for idx, group in enumerate(match.groups(), start=1):
            if group is None:
                continue
            cleaned = group.strip(" .!?\t\n")
            result = result.replace(f"{{{idx}}}", self._reflect(cleaned))
        return result

    def reply(self, text: str) -> str:
        cleaned = text.strip()
        if not cleaned:
            return "Please type something so we can talk."

        for pattern, responses in self.rules:
            match = pattern.match(cleaned)
            if match:
                template = random.choice(responses)
                return self._substitute_groups(template, match)

        return random.choice(self.default_responses)


app = Flask(__name__)
CORS(app)
bot = ElizaBot()


@app.get("/api/health")
def health() -> tuple:
    return jsonify({"status": "ok"}), 200


@app.post("/api/chat")
def chat() -> tuple:
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    response = bot.reply(message)
    return jsonify({"response": response}), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))
    app.run(host="0.0.0.0", port=port, debug=True)
