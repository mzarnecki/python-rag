from service.pipeline.payload import Payload
from service.pipeline.pipeline import Pipeline


def test_pipeline_passes_output_of_each_stage_to_next_one():
    result = (Pipeline()
              .pipe(lambda payload: payload.set_prompt('a'))
              .pipe(lambda payload: payload.set_rag_prompt(payload.get_prompt() + 'b'))
              .pipe(lambda payload: payload.get_rag_prompt())
              .process(Payload()))
    assert result == 'ab'
