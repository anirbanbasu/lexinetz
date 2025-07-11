import os
from icecream import ic
import constants

import gradio as gr

from dotenv import load_dotenv
from llama_index.llms.cohere import Cohere
from llama_index.llms.openai import OpenAI
from llama_index.llms.llamafile import Llamafile
from llama_index.llms.ollama import Ollama
from translator import AgenticTranslator


# Reload the app fast using `gradio src/gradio-ui.py` --demo-name=app
# Read more about the reload mode: https://www.gradio.app/guides/developing-faster-with-reload-mode
# TODO: Check controlling the reload: https://www.gradio.app/guides/developing-faster-with-reload-mode#controlling-the-reload
# TODO: Deploy on Docker: https://www.gradio.app/guides/deploying-gradio-with-docker

# Settings that can be configured through environment variables and the app UI.
rc_settings__llm_provider: gr.State = gr.State(constants.EMPTY_STRING)
rc_settings__cohere_api_key: gr.State = gr.State(constants.EMPTY_STRING)
rc_settings__cohere_model: gr.State = gr.State(constants.EMPTY_STRING)
rc_settings__llamafile_url: gr.State = gr.State(constants.EMPTY_STRING)
rc_settings__ollama_url: gr.State = gr.State(constants.EMPTY_STRING)
rc_settings__ollama_model: gr.State = gr.State(constants.EMPTY_STRING)
rc_settings__openai_api_key: gr.State = gr.State(constants.EMPTY_STRING)
rc_settings__openai_model: gr.State = gr.State(constants.EMPTY_STRING)
rc_settings__llm_temperature: gr.State = gr.State(0.0)

rc_settings__initialised: gr.State = gr.State(False)

rc_global__llm: gr.State = gr.State(None)


class GradioUI:
    def read_env_setting(
        self,
        setting: gr.State,
        env_key: str,
        default_value: str = None,
        type_cast=str,
        convert_to_list=False,
        list_split_char=constants.SPACE_STRING,
    ):
        """
        Sets a global setting's value to the corresponding environment variable or a default value.

        Args:
            setting (gradio.State): The Gradio state variable to set.
            env_key (str): The key of the environment variable.
            default_value (str): The default value to use if the environment variable is not set. Defaults to None.
            type_cast (type): The type to cast the environment variable value to. Defaults to str.
            convert_to_list (bool): Whether to convert the cast value to a list. Defaults to False.
            list_split_char (str): The character to split the value into a list. Defaults to " ".
        """

        parsed_value = None
        if isinstance(type_cast, bool):
            parsed_value = os.getenv(env_key, default_value).lower() in [
                "true",
                "yes",
                "t",
                "y",
                "on",
            ]
        else:
            parsed_value = os.getenv(env_key, default_value)

        setting.value = (
            type_cast(parsed_value)
            if not convert_to_list
            else [type_cast(v) for v in parsed_value.split(list_split_char)]
        )

    def update_llm(self):
        """Update the language model based on the selected provider."""
        match rc_settings__llm_provider.value:
            case constants.LLM_PROVIDER__COHERE:
                rc_global__llm.value = Cohere(
                    api_key=rc_settings__cohere_api_key.value,
                    model=rc_settings__cohere_model.value,
                    temperature=rc_settings__llm_temperature.value,
                )
            case constants.LLM_PROVIDER__OPENAI:
                rc_global__llm.value = OpenAI(
                    api_key=rc_settings__openai_api_key.value,
                    model=rc_settings__openai_model.value,
                    temperature=rc_settings__llm_temperature.value,
                )
            case constants.LLM_PROVIDER__LLAMAFILE:
                rc_global__llm.value = Llamafile(
                    url=rc_settings__llamafile_url.value,
                    temperature=rc_settings__llm_temperature.value,
                )
            case constants.LLM_PROVIDER__OLLAMA:
                rc_global__llm.value = Ollama(
                    url=rc_settings__ollama_url.value,
                    model=rc_settings__ollama_model.value,
                    temperature=rc_settings__llm_temperature.value,
                )

    def initialise_settings(self):
        """Initialise the settings for the app by reading from the environment variables, if available."""
        if not rc_settings__initialised.value:
            ic(load_dotenv())
            self.read_env_setting(
                rc_settings__llm_provider,
                constants.ENV_KEY__LLM_PROVIDER,
                constants.DEFAULT_VALUE__LLM_PROVIDER,
            )
            self.read_env_setting(
                rc_settings__cohere_api_key,
                constants.ENV_KEY__COHERE_API_KEY,
            )
            self.read_env_setting(
                rc_settings__cohere_model,
                constants.ENV_KEY__COHERE_MODEL,
                constants.DEFAULT_VALUE__COHERE_MODEL,
            )
            self.read_env_setting(
                rc_settings__llamafile_url,
                constants.ENV_KEY__LLAMAFILE_URL,
                constants.DEFAULT_VALUE__LLAMAFILE_URL,
            )
            self.read_env_setting(
                rc_settings__ollama_url,
                constants.ENV_KEY__OLLAMA_URL,
                constants.DEFAULT_VALUE__OLLAMA_URL,
            )
            self.read_env_setting(
                rc_settings__ollama_model,
                constants.ENV_KEY__OLLAMA_MODEL,
                constants.DEFAULT_VALUE__OLLAMA_MODEL,
            )
            self.read_env_setting(
                rc_settings__openai_api_key,
                constants.ENV_KEY__OPENAI_API_KEY,
            )
            self.read_env_setting(
                rc_settings__openai_model,
                constants.ENV_KEY__OPENAI_MODEL,
                constants.DEFAULT_VALUE__OPENAI_MODEL,
            )
            self.read_env_setting(
                rc_settings__llm_temperature,
                constants.ENV_KEY__LLM_TEMPERATURE,
                constants.DEFAULT_VALUE__LLM_TEMPERATURE,
                type_cast=float,
            )
            self.update_llm()
            rc_settings__initialised.value = True

    def construct_ui(self):
        """Construct the UI for the app."""
        with gr.Blocks(
            css=".column-form .wrap {flex-direction: column;} footer {visibility: hidden}"
        ) as app:
            with gr.Row():
                with gr.Column(visible=False, scale=1) as sidebar_left:
                    gr.Markdown("### Settings")
                    with gr.Group():
                        choice_llm_provider = gr.Dropdown(
                            choices=constants.LLM_PROVIDERS__SUPPORTED,
                            label="Language model provider",
                            value=rc_settings__llm_provider.value,
                            interactive=True,
                        )
                        with gr.Group(
                            visible=(
                                rc_settings__llm_provider.value
                                == constants.LLM_PROVIDER__COHERE
                            )
                        ) as group_llm_cohere:
                            gr.Textbox(
                                label="Cohere API key",
                                value=rc_settings__cohere_api_key.value,
                                type="password",
                                info="You can get an API key from the Cohere website.",
                                interactive=True,
                                # on_value=update_llm,
                            )
                            gr.Textbox(
                                label="Cohere model",
                                value=rc_settings__cohere_model.value,
                                interactive=True,
                                # on_value=update_llm,
                            )
                        with gr.Group(
                            visible=(
                                rc_settings__llm_provider.value
                                == constants.LLM_PROVIDER__OPENAI
                            )
                        ) as group_llm_openai:
                            gr.Textbox(
                                label="Open AI API key",
                                value=rc_settings__openai_api_key.value,
                                type="password",
                                info="You can get an API key from the Open AI website.",
                                interactive=True,
                                # on_value=update_llm,
                            )
                            gr.Textbox(
                                label="Open AI model",
                                value=rc_settings__openai_model.value,
                                interactive=True,
                                # on_value=update_llm,
                            )
                        with gr.Group(
                            visible=(
                                rc_settings__llm_provider.value
                                == constants.LLM_PROVIDER__LLAMAFILE
                            )
                        ) as group_llm_llamafile:
                            gr.Textbox(
                                label="Llamafile URL",
                                value=rc_settings__llamafile_url.value,
                                info="The URL must point to a running Llamafile (HTTP endpoint).",
                                interactive=True,
                                # on_value=update_llm,
                            )
                            gr.Markdown(
                                "_The model is based on the loaded Llamafile._",
                            )
                        with gr.Group(
                            visible=(
                                rc_settings__llm_provider.value
                                == constants.LLM_PROVIDER__OLLAMA
                            )
                        ) as group_llm_ollama:
                            gr.Textbox(
                                label="Ollama URL",
                                value=rc_settings__ollama_url.value,
                                info="The URL must point to a running Ollama server.",
                                interactive=True,
                                # on_value=update_llm,
                            )
                            gr.Textbox(
                                label="Ollama model",
                                value=rc_settings__ollama_model.value,
                                info="The model must be available on the selected Ollama server.",
                                interactive=True,
                                # on_value=update_llm,
                            )
                        gr.Slider(
                            label="Temperature",
                            minimum=0.0,
                            maximum=(
                                2.0
                                if rc_settings__llm_provider.value
                                == constants.LLM_PROVIDER__OPENAI
                                else 1.0
                            ),
                            step=0.1,
                            value=rc_settings__llm_temperature.value,
                            interactive=True,
                        )

                        @choice_llm_provider.change(
                            inputs=[choice_llm_provider],
                            outputs=[
                                group_llm_cohere,
                                group_llm_openai,
                                group_llm_llamafile,
                                group_llm_ollama,
                            ],
                            api_name=False,
                        )
                        def change_llm_provider(llm_provider_value):
                            match llm_provider_value:
                                case constants.LLM_PROVIDER__COHERE:
                                    rc_global__llm.value = Cohere(
                                        api_key=rc_settings__cohere_api_key.value,
                                        model=rc_settings__cohere_model.value,
                                        temperature=rc_settings__llm_temperature.value,
                                    )
                                case constants.LLM_PROVIDER__OPENAI:
                                    rc_global__llm.value = OpenAI(
                                        api_key=rc_settings__openai_api_key.value,
                                        model=rc_settings__openai_model.value,
                                        temperature=rc_settings__llm_temperature.value,
                                    )
                                case constants.LLM_PROVIDER__LLAMAFILE:
                                    rc_global__llm.value = Llamafile(
                                        url=rc_settings__llamafile_url.value,
                                        temperature=rc_settings__llm_temperature.value,
                                    )
                                case constants.LLM_PROVIDER__OLLAMA:
                                    rc_global__llm.value = Ollama(
                                        url=rc_settings__ollama_url.value,
                                        model=rc_settings__ollama_model.value,
                                        temperature=rc_settings__llm_temperature.value,
                                    )
                            return (
                                gr.update(
                                    visible=(
                                        llm_provider_value
                                        == constants.LLM_PROVIDER__COHERE
                                    ),
                                ),
                                gr.update(
                                    visible=(
                                        llm_provider_value
                                        == constants.LLM_PROVIDER__OPENAI
                                    ),
                                ),
                                gr.update(
                                    visible=(
                                        llm_provider_value
                                        == constants.LLM_PROVIDER__LLAMAFILE
                                    ),
                                ),
                                gr.update(
                                    visible=(
                                        llm_provider_value
                                        == constants.LLM_PROVIDER__OLLAMA
                                    ),
                                ),
                            )

                    rc_local__sidebar_state = gr.State(False)
                with gr.Column(scale=3):
                    with gr.Row(equal_height=True):
                        with gr.Column(scale=11):
                            gr.Markdown(
                                f"""
                                        # {constants.PROJECT__NAME}
                                        _{constants.PROJECT__HEADLINE}_"""
                            )
                        with gr.Column(scale=1):
                            btn_toggle_sidebar = gr.Button(
                                "⚙️",
                                size="sm",
                                scale=1,
                            )

                            @btn_toggle_sidebar.click(
                                inputs=[rc_local__sidebar_state],
                                outputs=[sidebar_left, rc_local__sidebar_state],
                                api_name=False,
                            )
                            def toggle_sidebar(state):
                                state = not state
                                return gr.update(visible=state), state

                    with gr.Row(equal_height=True):
                        choice_source_lang = gr.Dropdown(
                            choices=constants.LANGUAGES__SUPPORTED,
                            label="Source language",
                            interactive=True,
                        )
                        choice_target_lang = gr.Dropdown(
                            label="Target language",
                            interactive=True,
                        )
                    text_input = gr.TextArea(
                        label="Source text",
                        lines=5,
                        value=constants.SAMPLE_TEXT__ENGLISH_NEWS_ARTICLE,
                        placeholder="Enter text to translate.",
                    )
                    text_translated = gr.TextArea(
                        label="Translated text",
                        lines=5,
                        interactive=False,
                        placeholder="Translated text will appear here.",
                    )
                    btn_translate = gr.Button(
                        "Translate",
                        size="lg",
                        interactive=False,
                    )

                    @btn_translate.click(
                        inputs=[choice_source_lang, choice_target_lang, text_input],
                        outputs=[text_translated],
                        api_name="translate",
                    )
                    def translate_text(
                        source_lang_value, target_lang_value, text_input_value
                    ):
                        try:
                            if source_lang_value == target_lang_value:
                                raise ValueError(
                                    "Source and target languages are the same."
                                )
                            if source_lang_value is None or target_lang_value is None:
                                raise ValueError(
                                    "Source language and target language are both required."
                                )
                            ic(
                                f"Translating using {rc_settings__llm_provider.value}: {rc_global__llm.value.metadata.model_name}"
                            )
                            translator = AgenticTranslator(
                                llm=rc_global__llm.value,
                                source_language=source_lang_value,
                                target_language=target_lang_value,
                            )
                            translation_response = translator.agentic_translate(
                                text_input_value
                            )
                            ic("Translation completed.")
                            return translation_response
                        except Exception as e:
                            ic(f"Error while translating. {str(e)}")
                            return f"An error occurred while translating. {str(e)}"

                    @choice_source_lang.change(
                        inputs=[choice_source_lang],
                        outputs=[choice_target_lang],
                        api_name=False,
                    )
                    def change_source_language(source_lang_value):
                        return gr.update(
                            choices=[
                                lang
                                for lang in constants.LANGUAGES__SUPPORTED
                                if lang != source_lang_value
                            ],
                            value=None,
                        )

                    @choice_target_lang.change(
                        inputs=[choice_source_lang, choice_target_lang],
                        outputs=[btn_translate],
                        api_name=False,
                    )
                    def change_target_language(source_lang_value, target_lang_value):
                        return gr.update(
                            interactive=(
                                source_lang_value is not None
                                and target_lang_value is not None
                            ),
                        )

        return app


if __name__ == "__main__":
    gradio_ui = GradioUI()
    gradio_ui.initialise_settings()
    app = gradio_ui.construct_ui()
    app.launch()
