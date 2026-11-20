from service.claude.generated_text_from_claude_provider import GeneratedTextFromClaudeProvider
from service.deepseek.generated_text_from_deepseek_provider import GeneratedTextFromDeepSeekProvider
from service.gemini.gemini_text_encoder import GeminiTextEncoder
from service.gemini.generated_text_from_gemini_provider import GeneratedTextFromGeminiProvider
from service.generated_text_provider_interface import GeneratedTextProviderInterface
from service.ollama.generated_text_from_local_bielik_provider import GeneratedTextFromLocalBielikProvider
from service.ollama.generated_text_from_local_deepseek_coder_v2_provider import GeneratedTextFromLocalDeepSeekCoderV2Provider
from service.ollama.generated_text_from_local_deepseek_r1_7b_provider import GeneratedTextFromLocalDeepSeekR17BProvider
from service.ollama.generated_text_from_local_llama3_provider import GeneratedTextFromLocalLlama3Provider
from service.ollama.generated_text_from_mixtral_provider import GeneratedTextFromMixtralProvider
from service.ollama.mxbai_text_encoder import MxbaiTextEncoder
from service.openai.ada002_text_encoder import Ada002TextEncoder
from service.openai.generated_text_from_gpt_provider import GeneratedTextFromGPTProvider
from service.text_encoder_interface import TextEncoderInterface
from service.text_splitter import TextSplitter


class ServicesForSpecificModelFactory:
    def get_generated_text_provider(self, model: str) -> GeneratedTextProviderInterface:
        model = model.lower()
        mapping = {
            'gpt-5': GeneratedTextFromGPTProvider,
            'gpt-5-mini': GeneratedTextFromGPTProvider,
            'gpt-4.1': GeneratedTextFromGPTProvider,
            'o3': GeneratedTextFromGPTProvider,
            'o4-mini': GeneratedTextFromGPTProvider,
            'gpt-4o': GeneratedTextFromGPTProvider,
            'claude-3.7': GeneratedTextFromClaudeProvider,
            'claude-3.5': GeneratedTextFromClaudeProvider,
            'deepseek': GeneratedTextFromDeepSeekProvider,
            'llama3.2': GeneratedTextFromLocalLlama3Provider,
            'mixtral': GeneratedTextFromMixtralProvider,
            'bielik': GeneratedTextFromLocalBielikProvider,
            'deepseek-r1-7b': GeneratedTextFromLocalDeepSeekR17BProvider,
            'deepseek-coder-v2': GeneratedTextFromLocalDeepSeekCoderV2Provider,
            'gemini2': GeneratedTextFromGeminiProvider,
        }

        if model not in mapping:
            raise Exception(f'No service found for model {model}')

        # each provider uses the default model hardcoded in its class (same as php-rag)
        return mapping[model]()

    def get_embeddings_service(self, model: str) -> TextEncoderInterface:
        model = model.lower()
        mapping = {
            'gpt-5': Ada002TextEncoder,
            'gpt-5-mini': Ada002TextEncoder,
            'gpt-4.1': Ada002TextEncoder,
            'o3': Ada002TextEncoder,
            'o4-mini': Ada002TextEncoder,
            'gpt-4o': Ada002TextEncoder,
            'claude-3.7': Ada002TextEncoder,
            'claude-3.5': Ada002TextEncoder,
            'deepseek': Ada002TextEncoder,
            'llama3.2': MxbaiTextEncoder,
            'mixtral': MxbaiTextEncoder,
            'bielik': MxbaiTextEncoder,
            'deepseek-r1-7b': MxbaiTextEncoder,
            'deepseek-coder-v2': MxbaiTextEncoder,
            'gemini2': GeminiTextEncoder,
        }

        if model not in mapping:
            raise Exception(f'No service found for model {model}')

        return mapping[model](TextSplitter())
