from service.evaluate.string_comparison_evaluator import StringComparisonEvaluator

REFERENCE = "that's the way cookie crumbles"
CANDIDATE = 'this is the way cookie is crashed'


def test_calculate_rouge():
    assert StringComparisonEvaluator().calculate_rouge(REFERENCE, CANDIDATE) == {
        'precision': 0.43,
        'recall': 0.60,
        'f1': 0.50,
    }


def test_calculate_bleu():
    assert StringComparisonEvaluator().calculate_bleu(REFERENCE, CANDIDATE, 1) == 0.43
