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

from dotenv import load_dotenv
from icecream import ic
from pathlib import Path
from typing import Any

import constants
import os
import reacton.ipyvuetify as rv
import solara
import time


# Declare reactive variables at the top level. Components using these variables
# will be re-executed when their values change.
rc_text__translate_input = solara.reactive(
    "At the moment, nothing is translated. This is just a demo!"
)
rc_text__translated = solara.reactive("I know nothing!! This is just a demo!")
rc_language__translate_from: solara.Reactive[str] = solara.reactive(
    constants.EMPTY_STRING
)
rc_language__translate_to: solara.Reactive[str] = solara.reactive(
    constants.EMPTY_STRING
)

rc_status_message: solara.Reactive[str] = solara.reactive(constants.EMPTY_STRING)
rc_status_message__colour: solara.Reactive[str] = solara.reactive(
    constants.EMPTY_STRING
)
rc_status_message__show: solara.Reactive[bool] = solara.reactive(False)

# Settings that can be configured through environment variables and the app UI.
rc_settings__llm_provider: solara.Reactive[str] = solara.reactive(
    constants.EMPTY_STRING
)
rc_settings__cohere_api_key: solara.Reactive[str] = solara.reactive(
    constants.EMPTY_STRING
)
rc_settings__cohere_model: solara.Reactive[str] = solara.reactive(
    constants.EMPTY_STRING
)
rc_settings__llamafile_url: solara.Reactive[str] = solara.reactive(
    constants.EMPTY_STRING
)
rc_settings__ollama_url: solara.Reactive[str] = solara.reactive(constants.EMPTY_STRING)
rc_settings__ollama_model: solara.Reactive[str] = solara.reactive(
    constants.EMPTY_STRING
)
rc_settings__openai_api_key: solara.Reactive[str] = solara.reactive(
    constants.EMPTY_STRING
)
rc_settings__openai_model: solara.Reactive[str] = solara.reactive(
    constants.EMPTY_STRING
)
rc_settings__llm_temperature: solara.Reactive[float] = solara.reactive(0.0)


def read_env_setting(
    setting: solara.Reactive,
    env_key: str,
    default_value: str = None,
    type_cast=str,
    convert_to_list=False,
    list_split_char=constants.SPACE_STRING,
):
    """
    Sets a global setting's value to the corresponding environment variable or a default value.

    Args:
        setting (solara.Reactive): The Solara reactive variable to set.
        env_key (str): The key of the environment variable.
        default_value (str): The default value to use if the environment variable is not set. Defaults to None.
        type_cast (type): The type to cast the environment variable value to. Defaults to str.
        convert_to_list (bool): Whether to convert the cast value to a list. Defaults to False.
        list_split_char (str): The character to split the value into a list. Defaults to " ".
    """

    parsed_value = None
    if type_cast == bool:
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


def show_status_message(message: str, colour: str = "info", timeout: int = 4):
    """
    Update the Solara reactive variables, which can be used to display a status message on this page. The
    message will be displayed in the form of a toast with a configurable timeout.

    Args:
        message (str): The message to be displayed.
        colour (str): The colour of the message. Defaults to "info".
        timeout (int): The time in seconds to display the message. Defaults to 4 seconds.
    """
    rc_status_message.value = message
    rc_status_message__colour.value = colour
    rc_status_message__show.value = True
    if timeout > 0:
        time.sleep(timeout)
        rc_status_message__show.value = False


def initialise_settings():
    """Initialise the settings for the app by reading from the environment variables, if available."""
    ic(load_dotenv())
    read_env_setting(
        rc_settings__llm_provider,
        constants.ENV_KEY__LLM_PROVIDER,
        constants.DEFAULT_VALUE__LLM_PROVIDER,
    )
    read_env_setting(
        rc_settings__cohere_api_key,
        constants.ENV_KEY__COHERE_API_KEY,
    )
    read_env_setting(
        rc_settings__cohere_model,
        constants.ENV_KEY__COHERE_MODEL,
        constants.DEFAULT_VALUE__COHERE_MODEL,
    )
    read_env_setting(
        rc_settings__llamafile_url,
        constants.ENV_KEY__LLAMAFILE_URL,
        constants.DEFAULT_VALUE__LLAMAFILE_URL,
    )
    read_env_setting(
        rc_settings__ollama_url,
        constants.ENV_KEY__OLLAMA_URL,
        constants.DEFAULT_VALUE__OLLAMA_URL,
    )
    read_env_setting(
        rc_settings__ollama_model,
        constants.ENV_KEY__OLLAMA_MODEL,
        constants.DEFAULT_VALUE__OLLAMA_MODEL,
    )
    read_env_setting(
        rc_settings__openai_api_key,
        constants.ENV_KEY__OPENAI_API_KEY,
    )
    read_env_setting(
        rc_settings__openai_model,
        constants.ENV_KEY__OPENAI_MODEL,
        constants.DEFAULT_VALUE__OPENAI_MODEL,
    )
    read_env_setting(
        rc_settings__llm_temperature,
        constants.ENV_KEY__LLM_TEMPERATURE,
        constants.DEFAULT_VALUE__LLM_TEMPERATURE,
        type_cast=float,
    )


@solara.component
def CustomLayout(children: Any = None):
    """
    Define a custom layout for the app.

    Args:
        children (Any): The children components to be rendered within the layout.
    """

    with solara.AppLayout(
        children=children,
        color=None,
        navigation=True,
        sidebar_open=False,
    ) as app_layout:
        with solara.AppBar():
            # Display the status message as a toast, when avaiilable.
            with rv.Snackbar(
                timeout=0,
                multi_line=True,
                color=rc_status_message__colour.value,
                v_model=rc_status_message__show.value,
            ):
                solara.Markdown(f"{rc_status_message.value}")
            with rv.Btn(
                icon=True,
                tag="a",
                attributes={
                    "href": constants.PROJECT__GIT_URL,
                    "title": f"{constants.PROJECT__NAME}: {constants.PROJECT__HEADLINE}",
                    "target": constants.HTML_HREF__BLANK,
                },
            ):
                rv.Icon(children=["mdi-github-circle"])
            solara.lab.ThemeToggle()
    return app_layout


@solara.component
def SettingsSidebar():
    """The sidebar component to configure the settings."""

    with solara.Card(
        title="Settings",
        subtitle="""
            Settings about the language model that will be used for translation.
            """,
        elevation=0,
    ):
        solara.Select(
            dense=True,
            label="Language model provider",
            value=rc_settings__llm_provider,
            values=constants.SUPPORTED_LLM_PROVIDERS,
        )
        match rc_settings__llm_provider.value:
            case constants.LLM_PROVIDER_COHERE:
                solara.InputText(
                    label="Cohere API key",
                    value=rc_settings__cohere_api_key,
                    password=True,
                    message="You can get an API key from the Cohere website.",
                )
                solara.InputText(
                    label="Cohere model",
                    value=rc_settings__cohere_model,
                )
            case constants.LLM_PROVIDER_OPENAI:
                solara.InputText(
                    label="Open AI API key",
                    value=rc_settings__openai_api_key,
                    password=True,
                    message="You can get an API key from the Open AI website.",
                )
                solara.InputText(label="Open AI model", value=rc_settings__openai_model)
            case constants.LLM_PROVIDER_LLAMAFILE:
                solara.InputText(
                    label="Llamafile URL",
                    value=rc_settings__llamafile_url,
                    message="The URL must point to a running Llamafile (HTTP endpoint).",
                )
                solara.Markdown("_The model is based on the loaded Llamafile._")
            case constants.LLM_PROVIDER_OLLAMA:
                solara.InputText(
                    label="Ollama URL",
                    value=rc_settings__ollama_url,
                    message="The URL must point to a running Ollama server.",
                )
                solara.InputText(
                    label="Ollama model",
                    value=rc_settings__ollama_model,
                    message="The model must be available on the selected Ollama server.",
                )
        solara.SliderFloat(
            label="Temperature",
            min=0.0,
            max=(
                2.0
                if rc_settings__llm_provider.value == constants.LLM_PROVIDER_OPENAI
                else 1.0
            ),
            step=0.1,
            value=rc_settings__llm_temperature,
            tick_labels="end_points",
        )


@solara.component
def Page():
    """The main page of the app."""
    initialise_settings()
    # CWD = Current Working Directory
    CWD = Path(__file__).parent
    # Load the external CSS file to be used as global styles for the page.
    extern_style = (CWD / "css/styles.css").read_text(
        encoding=constants.CHAR_ENCODING__UTF8
    )
    # Check if the external style sheet has any content.
    ic(extern_style.strip() != constants.EMPTY_STRING)
    solara.Style(extern_style)

    with solara.Sidebar():
        SettingsSidebar()

    with solara.ColumnsResponsive(
        xlarge=[6, 6], medium=[6, 6], small=[12], default=[6, 6], wrap=True
    ):
        with solara.Column():
            solara.Select(
                label="Select the language to translate from",
                value=rc_language__translate_from,
                values=constants.SUPPORTED_LANGUAGES,
            )
        with solara.Column():
            solara.Select(
                label="Select the language to translate to",
                value=rc_language__translate_to,
                # Don't show the language selected in the "Translate from" dropdown.
                values=[
                    lang
                    for lang in constants.SUPPORTED_LANGUAGES
                    if lang != rc_language__translate_from.value
                ],
            )

    solara.Button(
        "Translate!",
        color="primary",
        disabled=(
            rc_text__translate_input.value == constants.EMPTY_STRING
            or rc_language__translate_from.value == constants.EMPTY_STRING
            or rc_language__translate_to.value == constants.EMPTY_STRING
            or rc_language__translate_from.value == rc_language__translate_to.value
        ),
        on_click=lambda: show_status_message("Hello, world!"),
    )

    with solara.ColumnsResponsive(xlarge=[12], medium=[12], default=[6, 6], wrap=True):
        with solara.Column():
            rv.Textarea(
                label="Text to translate",
                v_model=rc_text__translate_input.value,
                on_v_model=rc_text__translate_input.set,
                outlined=True,
                auto_grow=True,
                rows=10,
                counter=True,
            )
        with solara.Column():
            rv.Textarea(
                label="Translated text",
                v_model=rc_text__translated.value,
                outlined=True,
                readonly=True,
                rows=10,
                auto_grow=True,
                counter=True,
            )


routes = [
    # Define the main route for the app with the custom layout.
    solara.Route(
        path="/", label=constants.PROJECT__NAME, component=Page, layout=CustomLayout
    ),
]
