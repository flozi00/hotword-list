from transformers.pipelines import AutomaticSpeechRecognitionPipeline as pipeline

from aaas.model_utils import get_model_and_processor
from aaas.statics import LANG_MAPPING
from aaas.utils import timeit
import torch


@timeit
def inference_asr(data, main_lang: str, model_config: str) -> list:
    model, processor = get_model_and_processor(main_lang, "asr", model_config)

    if torch.cuda.is_available():
        model = model.half()

    transcriber = pipeline(
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        device=0 if torch.cuda.is_available() else -1,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        ignore_warning=True,
        chunk_length_s=30,
        stride_length_s=[15, 0],
    )

    transcription = transcriber(
        data,
        generate_kwargs={
            "task": "transcribe",
            "language": f"<|{LANG_MAPPING[main_lang]}|>",
        },
    )["text"].strip()

    return transcription

