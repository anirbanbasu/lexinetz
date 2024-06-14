# Copyright 2024 Anirban Basu

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

EMPTY_STRING = ""
SPACE_STRING = " "

COLOUR__SUCCESS = "success"
COLOUR__INFO = "info"
COLOUR__ERROR = "error"
COLOUR__WARNING = "warning"

CHAR_ENCODING__UTF8 = "utf-8"
CHAR_ENCODING__UTF16 = "utf-16"
CHAR_ENCODING__UTF32 = "utf-32"
CHAR_ENCODING__ASCII = "ascii"
CHAR_ENCODING__LATIN1 = "latin1"

HTML_HREF__BLANK = "_blank"

PROJECT__NAME = "lexinetz"
PROJECT__HEADLINE = "knowledge based language translation"
PROJECT__GIT_URL = "https://github.com/anirbanbasu/lexinetz"

LANGUAGES__SUPPORTED = [
    "English",
    "Español",  # Spanish
    "Français",  # French
    "Italiano",  # Italian
    "Deutsch",  # German
    "Português",  # Portuguese
    "Suomi",  # Finnish
    "Svenska",  # Swedish
    "Dansk",  # Danish
    "Norsk",  # Norwegian
    "Nederlands",  # Dutch
    "Polski",  # Polish
    "বাংলা",  # Bengali
    "日本語",  # Japanese
    "中文",  # Mandarin
    "한국어",  # Korean
]

LLM_PROVIDER__COHERE = "Cohere"
LLM_PROVIDER__LLAMAFILE = "Llamafile"
LLM_PROVIDER__OLLAMA = "Ollama"
LLM_PROVIDER__OPENAI = "Open AI"
LLM_PROVIDERS__SUPPORTED = [
    LLM_PROVIDER__COHERE,
    LLM_PROVIDER__LLAMAFILE,
    LLM_PROVIDER__OLLAMA,
    LLM_PROVIDER__OPENAI,
]


PROMPT__SYSTEM_SIMPLE = "You are an expert linguist, who specialises in translation from {source_language} to {target_language}."
PROMPT__TRANSLATE_SIMPLE = """This is a {source_language} to {target_language} translation task.
The text in the {source_language} may contain idiomatic expressions. You must output idiomatic equivalents for such expressions in the {target_language}.
Please provide the {target_language} translation for the following text. Do not provide any explanations or any other text apart from the translation.
{source_language}: {source_text}

{target_language}:"""

ENV_KEY__LLM_PROVIDER = "LLM_PROVIDER"
DEFAULT_VALUE__LLM_PROVIDER = "Ollama"

ENV_KEY__COHERE_API_KEY = "COHERE_API_KEY"

ENV_KEY__LLAMAFILE_URL = "LLAMAFILE_URL"
DEFAULT_VALUE__LLAMAFILE_URL = "http://localhost:8080"

ENV_KEY__OLLAMA_URL = "OLLAMA_URL"
DEFAULT_VALUE__OLLAMA_URL = "http://localhost:11434"

ENV_KEY__OPENAI_API_KEY = "OPENAI_API_KEY"

ENV_KEY__COHERE_MODEL = "COHERE_MODEL"
DEFAULT_VALUE__COHERE_MODEL = "command-r-plus"

ENV_KEY__OLLAMA_MODEL = "OLLAMA_MODEL"
DEFAULT_VALUE__OLLAMA_MODEL = "llama3"

ENV_KEY__OPENAI_MODEL = "OPENAI_MODEL"
DEFAULT_VALUE__OPENAI_MODEL = "gpt-3.5-turbo-0125"

ENV_KEY__LLM_TEMPERATURE = "LLM_TEMPERATURE"
DEFAULT_VALUE__LLM_TEMPERATURE = "0.4"


SAMPLE_TEXT__ENGLISH_PLACEHOLDER = "The quick brown fox jumps over the lazy dog."
# News article from the BBC: https://www.bbc.com/news/articles/c9eem1dkx5vo
SAMPLE_TEXT__ENGLISH_NEWS_ARTICLE = "New research is being carried out using artificial intelligence (AI) to analyse cosmic explosions. A type of AI known as machine learning will be used to make simulations of star explosions called supernovae, that release elements such as calcium and iron back into the universe. The research by the University of Warwick aims to help astronomers understand more about why and how supernovae take place. Lead author of the research Dr Mark Magee said while one model currently took up to 90 minutes to create, AI would enable thousands of supernovae models to be generated in less than a second. AI would also make research more accurate, helping to establish what models match real-life explosions, the university said. It added advancements in machine learning had made the research possible with future studies including a greater variety of explosions and supernovae.  'Machine learning approaches like this enable studies of larger numbers of supernovae, in greater detail, and with more consistency than previous approaches,' Dr Thomas Killestein said. (Source: https://www.bbc.com/news/articles/c9eem1dkx5vo)"
