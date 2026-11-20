class Pipeline:
    """Minimal equivalent of league/pipeline with FingersCrossedProcessor:
    output of each stage is passed as input to the next one."""

    def __init__(self):
        self.stages = []

    def pipe(self, stage) -> "Pipeline":
        self.stages.append(stage)
        return self

    def process(self, payload):
        for stage in self.stages:
            payload = stage(payload)
        return payload
