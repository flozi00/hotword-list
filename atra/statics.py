from transformers import (
    WhisperProcessor,
    WhisperForConditionalGeneration,
    M2M100ForConditionalGeneration,
    M2M100Tokenizer,
    T5ForConditionalGeneration,
    T5TokenizerFast,
)

MODEL_MAPPING = {
    "asr": {
        "small": {
            "german": {
                "name": "flozi00/whisper-small-german-cv13-simplepeft",
                "class": WhisperForConditionalGeneration,
                "processor": WhisperProcessor,
            },
            "universal": {
                "name": "openai/whisper-small",
                "class": WhisperForConditionalGeneration,
                "processor": WhisperProcessor,
            },
        },
        "large": {
            "german": {"adapter_id": "flozi00/whisper-large-german-lora-cv13"},
            "universal": {
                "name": "openai/whisper-large-v2",
                "class": WhisperForConditionalGeneration,
                "processor": WhisperProcessor,
            },
        },
    },
    "translation": {
        "small": {
            "universal": {
                "name": "facebook/m2m100_418M",
                "class": M2M100ForConditionalGeneration,
                "processor": M2M100Tokenizer,
            }
        },
        "large": {
            "universal": {
                "name": "facebook/m2m100_1.2B",
                "class": M2M100ForConditionalGeneration,
                "processor": M2M100Tokenizer,
            }
        },
    },
    "summarization": {
        "small": {
            "universal": {
                "name": "philschmid/flan-t5-base-samsum",
                "class": T5ForConditionalGeneration,
                "processor": T5TokenizerFast,
            }
        },
        "large": {
            "universal": {
                "name": "philschmid/flan-t5-base-samsum",
                "class": T5ForConditionalGeneration,
                "processor": T5TokenizerFast,
            }
        },
    },
}

LANGUAGE_CODES = {
    "en": "english",
    "zh": "chinese",
    "de": "german",
    "es": "spanish",
    "ru": "russian",
    "ko": "korean",
    "fr": "french",
    "ja": "japanese",
    "pt": "portuguese",
    "tr": "turkish",
    "pl": "polish",
    "ca": "catalan",
    "nl": "dutch",
    "ar": "arabic",
    "sv": "swedish",
    "it": "italian",
    "id": "indonesian",
    "hi": "hindi",
    "fi": "finnish",
    "vi": "vietnamese",
    "iw": "hebrew",
    "uk": "ukrainian",
    "el": "greek",
    "ms": "malay",
    "cs": "czech",
    "ro": "romanian",
    "da": "danish",
    "hu": "hungarian",
    "ta": "tamil",
    "no": "norwegian",
    "th": "thai",
    "ur": "urdu",
    "hr": "croatian",
    "bg": "bulgarian",
    "lt": "lithuanian",
    "la": "latin",
    "mi": "maori",
    "ml": "malayalam",
    "cy": "welsh",
    "sk": "slovak",
    "te": "telugu",
    "fa": "persian",
    "lv": "latvian",
    "bn": "bengali",
    "sr": "serbian",
    "az": "azerbaijani",
    "sl": "slovenian",
    "kn": "kannada",
    "et": "estonian",
    "mk": "macedonian",
    "br": "breton",
    "eu": "basque",
    "is": "icelandic",
    "hy": "armenian",
    "ne": "nepali",
    "mn": "mongolian",
    "bs": "bosnian",
    "kk": "kazakh",
    "sq": "albanian",
    "sw": "swahili",
    "gl": "galician",
    "mr": "marathi",
    "pa": "punjabi",
    "si": "sinhala",
    "km": "khmer",
    "sn": "shona",
    "yo": "yoruba",
    "so": "somali",
    "af": "afrikaans",
    "oc": "occitan",
    "ka": "georgian",
    "be": "belarusian",
    "tg": "tajik",
    "sd": "sindhi",
    "gu": "gujarati",
    "am": "amharic",
    "yi": "yiddish",
    "lo": "lao",
    "uz": "uzbek",
    "fo": "faroese",
    "ht": "haitian creole",
    "ps": "pashto",
    "tk": "turkmen",
    "nn": "nynorsk",
    "mt": "maltese",
    "sa": "sanskrit",
    "lb": "luxembourgish",
    "my": "myanmar",
    "bo": "tibetan",
    "tl": "tagalog",
    "mg": "malagasy",
    "as": "assamese",
    "tt": "tatar",
    "haw": "hawaiian",
    "ln": "lingala",
    "ha": "hausa",
    "ba": "bashkir",
    "jw": "javanese",
    "su": "sundanese",
}

LANG_MAPPING = {v: k for k, v in LANGUAGE_CODES.items()}

TODO = "***TODO***"
INPROGRESS = "***PROGRESS***"
TO_ASR = "***TO ASR***"

CACHE_SIZE = 128

TASK_MAPPING = {
    "asr": ["start", "end"],
    "translation": ["source", "target"],
    "summarization": ["long_text", "short_text"],
}