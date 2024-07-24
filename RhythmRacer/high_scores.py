import json
import os

class HighScores:
    def __init__(self):
        self.scores_file = "high_scores.json"
        self.scores = self.load_scores()

    def load_scores(self):
        if os.path.exists(self.scores_file):
            with open(self.scores_file, 'r') as f:
                return json.load(f)
        return {"continuous": [], "timed": []}

    def save_scores(self):
        with open(self.scores_file, 'w') as f:
            json.dump(self.scores, f)

    def add_score(self, mode, score, name):
        self.scores[mode].append({"name": name, "score": score})
        self.scores[mode] = sorted(self.scores[mode], key=lambda x: x["score"], reverse=True)[:10]
        self.save_scores()

    def get_high_scores(self, mode):
        return self.scores[mode]