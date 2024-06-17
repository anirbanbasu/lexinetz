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
from llama_index.core.agent.react import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.core.chat_engine.types import AgentChatResponse

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

    def _translate(
        self, source_text: str, source_language: str, target_language: str
    ) -> str:
        """
        Useful for translating text from one language to another.

        Args:
            source_text (str): The text to translate.
            source_language (str): The source language of the text.
            target_language (str): The target language to translate the text to.

        Returns:
            str: The translated text.
        """
        self.switch_translation_languages(source_language, target_language)
        return self.translate(source_text).text

    def translate(self, source_text: str) -> CompletionResponse:
        """
        Useful for translating text from one language to another.

        Args:
            source_text (str): The text to translate.

        Returns:
            CompletionResponse: The LLM response containing the translated text.
        """
        simple_translation_prompt = PromptTemplate(
            template=constants.PROMPT__TRANSLATE_SIMPLE,
        ).format(
            source_language=self._source_language,
            target_language=self._target_language,
            source_text=source_text,
        )
        return self._llm.complete(prompt=simple_translation_prompt)


class AgenticTranslator(BaseTranslator):
    def __init__(self, llm: LLM, source_language: str, target_language: str):
        super().__init__(llm, source_language, target_language)

        self._fn_translate = FunctionTool.from_defaults(
            fn=self._translate,
            name="translate",
            description="Translate text from one language to another.",
        )

        self._fn_extract_knowledge_triplets = FunctionTool.from_defaults(
            fn=self._extract_knowledge_triplets,
            name="extract",
            description="""Extract knowledge graph triplets from a given text to
            represent concepts and relationships in a structured format.""",
        )

        self._fn_assess_translation = FunctionTool.from_defaults(
            fn=self._assess_translation,
            name="assess",
            description="""Assess the quality of a translation by comparing it with the knowledge graph triplets
            extracted from the original text to see if the concepts have been exhaustively represented.""",
        )

        self._llm_react_agent = ReActAgent.from_tools(
            tools=[
                self._fn_translate,
                self._fn_extract_knowledge_triplets,
                self._fn_assess_translation,
            ],
            llm=self._llm,
            name="ReAct agentic translator",
            description="""An agentic translator that can translate text from one language to another,
            extract knowledge graph triplets, and assess the quality of a translation.""",
            verbose=True,
        )

    def _extract_knowledge_triplets(
        self, source_text: str, max_triplets: int = 10
    ) -> str:
        """
        Useful for extracting knowledge graph triplets from a given text to
        represent concepts and relationships in a structured format.

        Args:
            source_text (str): The text from which to extract knowledge graph triplets.
            max_triplets (int, optional): The maximum number of triplets to extract. Defaults to 10.

        Returns:
            str: The extracted knowledge graph triplets.
        """
        return self.extract_knowledge_triplets(source_text, max_triplets).text

    def extract_knowledge_triplets(
        self, source_text: str, max_triplets: int = 10
    ) -> CompletionResponse:
        """
        Useful for extracting knowledge graph triplets from a given text to
        represent concepts and relationships in a structured format.

        Args:
            source_text (str): The text from which to extract knowledge graph triplets.
            max_triplets (int, optional): The maximum number of triplets to extract. Defaults to 10.

        Returns:
            CompletionResponse: The LLM response containing the extracted knowledge graph triplets.
        """
        kg_extraction_prompt = PromptTemplate(
            template=constants.PROMPT__KG_EXTRACT,
        ).format(
            max_knowledge_triplets=max_triplets,
            source_text=source_text,
        )
        return self._llm.complete(prompt=kg_extraction_prompt)

    def _assess_translation(
        self,
        source_text: str,
        translated_text: str,
        knowledge_triplets_response: str,
        source_language: str,
        target_language: str,
    ) -> str:
        """
        Useful for assessing the quality of a translation by comparing it with the knowledge graph triplets
        extracted from the original text to see if the concepts have been exhaustively represented.

        Args:
            source_text (str): The original text.
            translated_text (str): The translated text.
            knowledge_triplets_response (str): The extracted knowledge graph triplets from the original text.
            source_language (str): The source language of the text.
            target_language (str): The target language of the translation.

        Returns:
            str: The assessment of the translation.
        """
        self.switch_translation_languages(source_language, target_language)
        return self.assess_translation(
            source_text, translated_text, knowledge_triplets_response
        ).text

    def assess_translation(
        self, source_text: str, translated_text: str, knowledge_triplets_response: str
    ) -> CompletionResponse:
        """
        Useful for assessing the quality of a translation by comparing it with the knowledge graph triplets
        extracted from the original text to see if the concepts have been exhaustively represented.

        Args:
            source_text (str): The original text.
            translated_text (str): The translated text.
            knowledge_triplets_response (str): The extracted knowledge graph triplets from the original text.

        Returns:
            CompletionResponse: The LLM response containing the assessment of the translation.
        """
        translation_assessment_prompt = PromptTemplate(
            template=constants.PROMPT__KG_ASSESS
        ).format(
            target_language=self._target_language,
            source_language=self._source_language,
            source_text=source_text,
            translated_text=translated_text,
            knowledge_triplets=knowledge_triplets_response,
        )
        return self._llm.complete(prompt=translation_assessment_prompt)

    def agentic_translate(self, source_text: str) -> AgentChatResponse:
        react_translation_prompt = PromptTemplate(
            template=constants.PROMPT__TRANSLATE_REACT,
        ).format(
            source_language=self._source_language,
            target_language=self._target_language,
            source_text=source_text,
        )
        response: AgentChatResponse = self._llm_react_agent.chat(
            react_translation_prompt
        )
        return response.response

    def reflective_translate(self, source_text: str) -> List[CompletionResponse]:
        result = []

        kg_response = self.extract_knowledge_triplets(source_text)
        ic(kg_response.text)
        result.append(kg_response)

        initial_translation = self.translate(source_text)
        ic(initial_translation.text)
        result.append(initial_translation)

        improvement_suggestions = self.assess_translation(
            source_text, initial_translation.text, kg_response.text
        )
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
