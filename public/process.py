import json
import os
import sys
import traceback

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from service.document_provider import DocumentProvider  # noqa: E402
from service.env_loader import load_env  # noqa: E402
from service.evaluate.criteria_evaluator import CriteriaEvaluator  # noqa: E402
from service.evaluate.string_comparison_evaluator import StringComparisonEvaluator  # noqa: E402
from service.pipeline.payload import Payload  # noqa: E402
from service.pipeline.pipeline import Pipeline  # noqa: E402
from service.prompt_resolver import PromptResolver  # noqa: E402
from service.rag_prompt_provider import RAGPromptProvider  # noqa: E402
from service.services_for_specific_model_factory import ServicesForSpecificModelFactory  # noqa: E402


def process(post: dict, get: dict) -> str:
    """Equivalent of public/process.php - post/get are the $_POST/$_GET dicts. Returns response body."""
    load_env()
    model = os.environ['MODEL']
    services_for_model_factory = ServicesForSpecificModelFactory()

    prompt_resolver = PromptResolver(post)
    text_encoder = services_for_model_factory.get_embeddings_service(model)
    document_provider = DocumentProvider()
    generated_text_provider = services_for_model_factory.get_generated_text_provider(model)
    rag_prompt_provider = RAGPromptProvider()

    payload = Payload().set_use_reranking(False)

    pipeline = (Pipeline()
                .pipe(prompt_resolver)  # get prompt from POST or CLI
                .pipe(text_encoder)  # get embeddings for prompt
                .pipe(document_provider)  # find documents with similarity to prompt
                .pipe(rag_prompt_provider)  # prepare RAG input - combine prompt with matched source documents
                .pipe(generated_text_provider))  # get API response

    response = pipeline.process(payload)

    output = ''
    resp = None
    if 'api' in get:
        resp = {
            'response': response,
            'documents': payload.get_similar_documents_names(),
        }
    else:
        output += '<h1>RESPONSE:</h1>'
        output += '<br /><br />'
        output += response
        output += '<br /><br /><br /><br />'
        output += '<h1>DOCUMENTS:</h1>'
        output += '<br /><br />'
        output += payload.get_rag_prompt()

    evaluate = post.get('evaluate') or get.get('evaluate')

    if evaluate and evaluate != '0':
        resp = resp or {}
        criteria_evaluator = CriteriaEvaluator(generated_text_provider)
        token_similarity_evaluator = StringComparisonEvaluator()
        compare_resp = '''Michał Żarnecki programmer is not the same person as Michał Żarnecki audio engineer. 
        Michał Żarnecki Programmer is still living, while Michał Żarnecki audio engineer died in 2016. They cannot be the same person.
        Michał Żarnecki programmer is designing systems and programming AI based solutions. He is also a lecturer.
        Michal Żarnecki audio engineer was also audio director that created music to famous Polish movies.'''

        resp['evaluation'] = {}
        try:
            resp['evaluation']['ROUGE'] = token_similarity_evaluator.calculate_rouge(compare_resp, response)
            resp['evaluation']['BLEU'] = token_similarity_evaluator.calculate_bleu(compare_resp, response)
            resp['evaluation']['criteria'] = criteria_evaluator.evaluate(payload.get_rag_prompt(), response)
        except Exception:
            traceback.print_exc()
            resp['evaluation']['error'] = 'Error occured during evaluation, check logs.'

    if resp is not None:
        output += json.dumps(resp)

    return output
