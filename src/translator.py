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


from icecream import ic
from llama_index.core import PromptTemplate
from llama_index.core.llms.llm import LLM
from llama_index.core.base.llms.types import CompletionResponse

import constants


class BaseTranslator:
    def __init__(self, llm: LLM, source_language: str, target_language: str):
        self._llm = llm
        self.switch_translation_languages(source_language, target_language)
        ic(self._llm)

    def switch_translation_languages(self, source_language: str, target_language: str):
        self._source_language = source_language
        self._target_language = target_language
        self._system_prompt = PromptTemplate(
            template=constants.PROMPT__SYSTEM,
        ).format(
            source_language=self._source_language,
            target_language=self._target_language,
        )
        self._llm.system_prompt = self._system_prompt

    def translate(self, source_text: str) -> CompletionResponse:
        translation_prompt = PromptTemplate(
            template=constants.PROMPT__TRANSLATE,
        ).format(
            source_language=self._source_language,
            target_language=self._target_language,
            source_text=source_text,
        )
        response = self._llm.complete(prompt=translation_prompt)
        return response


class AgenticTranslator:
    def __init__(self):
        pass

    def translate(self):
        raise NotImplementedError
