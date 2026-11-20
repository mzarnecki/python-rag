import math


class StringComparisonEvaluator:
    def calculate_bleu(self, reference: str, candidate: str, n: int = 1) -> float:
        candidate_words = candidate.split(' ')
        reference_words = reference.split(' ')
        candidate_length = len(candidate_words)
        reference_length = len(reference_words)

        n_gram_matches = {}
        for i in range(1, n + 1):
            candidate_n_grams = self._get_n_grams(candidate_words, i)
            reference_n_grams = self._get_n_grams(reference_words, i)

            matches = 0
            for ngram in candidate_n_grams:
                if ngram in reference_n_grams:
                    matches += 1
            n_gram_matches[i] = matches / max(len(candidate_n_grams), 1)

        precision = math.prod(n_gram_matches.values())
        brevity_penalty = 1 if candidate_length > reference_length \
            else math.exp(1 - (reference_length / max(candidate_length, 1)))

        return round(brevity_penalty * precision ** (1 / n), 2)

    def calculate_rouge(self, reference: str, candidate: str, n: int = 1) -> dict:
        candidate_words = candidate.split(' ')
        reference_words = reference.split(' ')

        candidate_n_grams = self._get_n_grams(candidate_words, n)
        reference_n_grams = self._get_n_grams(reference_words, n)

        matches = 0
        for ngram in candidate_n_grams:
            if ngram in reference_n_grams:
                matches += 1

        recall = matches / max(len(reference_n_grams), 1)
        precision = matches / max(len(candidate_n_grams), 1)
        f1_score = 2 * (recall * precision) / (recall + precision) if recall + precision > 0 else 0

        return {
            'recall': round(recall, 2),
            'precision': round(precision, 2),
            'f1': round(f1_score, 2),
        }

    def _get_n_grams(self, words: list[str], n: int) -> list[str]:
        n_grams = []
        words_count = len(words)
        for i in range(words_count - n + 1):
            n_grams.append(' '.join(words[i:i + n]))

        return n_grams
