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
from typing import List
from llama_index.core import PromptTemplate
from llama_index.core.llms.llm import LLM
from llama_index.core.base.llms.types import CompletionResponse

import constants


class BaseTranslator:
    def __init__(self, llm: LLM, source_language: str, target_language: str):
        self._llm = llm
        self.switch_translation_languages(source_language, target_language)

    def switch_translation_languages(self, source_language: str, target_language: str):
        self._source_language = source_language
        self._target_language = target_language
        self._system_prompt = PromptTemplate(
            template=constants.PROMPT__SYSTEM_SIMPLE,
        ).format(
            source_language=self._source_language,
            target_language=self._target_language,
        )
        self._llm.system_prompt = self._system_prompt

    def translate(self, source_text: str) -> List[CompletionResponse]:
        translation_prompt = PromptTemplate(
            template=constants.PROMPT__TRANSLATE_SIMPLE,
        ).format(
            source_language=self._source_language,
            target_language=self._target_language,
            source_text=source_text,
        )
        response = self._llm.complete(prompt=translation_prompt)
        return [response]


class AgenticTranslator(BaseTranslator):
    def __init__(self, llm: LLM, source_language: str, target_language: str):
        super().__init__(llm, source_language, target_language)

    def reflective_translate(self, source_text: str) -> List[CompletionResponse]:
        result = []
        kg_extraction_prompt = PromptTemplate(
            template=constants.PROMPT__KG_EXTRACT,
        ).format(
            max_knowledge_triplets=10,
            target_language=self._target_language,
            source_text=source_text,
        )
        kg_response = self._llm.complete(prompt=kg_extraction_prompt)
        ic(kg_response.text)
        result.append(kg_response)
        initial_translation = self.translate(source_text)[0]
        ic(initial_translation.text)
        result.append(initial_translation)
        kg_assess_prompt = PromptTemplate(template=constants.PROMPT__KG_ASSESS).format(
            target_language=self._target_language,
            source_language=self._source_language,
            source_text=source_text,
            translated_text=initial_translation.text,
            knowledge_triplets=kg_response.text,
        )
        improvement_suggestions = self._llm.complete(prompt=kg_assess_prompt)
        ic(improvement_suggestions.text)
        result.append(improvement_suggestions)
        kg_improved_translation_prompt = PromptTemplate(
            template=constants.PROMPT__TRANSLATE_IMPROVE
        ).format(
            target_language=self._target_language,
            source_language=self._source_language,
            source_text=source_text,
            translated_text=initial_translation.text,
            improvement_suggestions=improvement_suggestions.text,
        )
        final_translation = self._llm.complete(prompt=kg_improved_translation_prompt)
        result.append(final_translation)
        ic(final_translation.text)
        return result
