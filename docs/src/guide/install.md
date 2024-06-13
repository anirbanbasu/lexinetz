# Installation

lexinetz is written in Python. You can use it through a web app~~, a REST API or a command line interface~~. For the web app ~~and the command line interface~~, you can either set it up to work in a Python virtual environment or inside a container (Docker).

In addition to installation, you can configure the application using environment variables. Some settings can be modified through the web app. All settings can be modified by using a local `.env` file or as environment variables of your shell. However, settings that can be modified using the web app are **not** stored as environment variables, which means settings in one browser session will be independent of the settings in another browser session even if both are initialised with the settings from the environment variables. A comprehensive list of the supported environment variables is available in the `.env.template` file at the root of the repository, which can serve as a starting point.
