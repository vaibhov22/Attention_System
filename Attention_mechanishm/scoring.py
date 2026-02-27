class AttentionScorer:
    def calculate_score(self, EAR, looking_away):
        score = 100

        if EAR < 0.22:
            score -= 15

        if looking_away:
            score -= 30

        return max(0, score)