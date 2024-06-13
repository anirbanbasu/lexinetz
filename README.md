# lexinetz

lexninetz is **an experimental project** that employs knowledge graphs and agent-based reflection for natural language translation using multi-lingual language models. The project is inspired by the weekend musings on language translations using language models by [Professor Andrew Ng](https://www.andrewng.org/) and his collaborators, which have been open-sourced as the [translation-agent](https://github.com/andrewyng/translation-agent) project.

The name _lexinetz_ originates from the combination of two words: _λέξη_ (léxi) in Greek for _word_ in English, and _netz_ (e.g., das Netz) in German for _network_ in English.

lexinetz also supports language model providers other than Open AI, including Ollama. lexinetz attempts to build on the ideas in `translation-agent` by introducing knowledge graphs for concept-based translation and agent-based reflection using competing agents. For more detail about reflection capabilities in artificial intelligence (which is something lexinetz does not have), refer to the [arXiv:2301.10823 [cs.AI]](https://arxiv.org/abs/2301.10823).

## Documentation

The documentation of this project is available in the mdBook format. If you have followed the installation of both [Rust](https://www.rust-lang.org/tools/install) and [mdBook](https://rust-lang.github.io/mdBook/guide/installation.html), you can run `mdbook serve --open docs/` from the directory where you cloned this Git repository. Unless you are running a headless terminal, this command will open a web browser with the documentation at [http://localhost:3000/](http://localhost:3000). If the default IP address and port binding is not your cup of tea, run `mdbook serve --help` to see how to make the server bind to some other IP address and port.

### GitHub Pages and documentation source
If you are seeing this project on GitHub then the documentation may be available through GitHub Pages: check if there is a URL in the about section of the project on GitHub. If there is no GitHub pages deployment and you do not have the means to build the documentation using mdBook, you can always see the contents of the documentation in Markdown format by browsing its source and starting at `docs/src/SUMMARY.md` relative to the base of this repository.
