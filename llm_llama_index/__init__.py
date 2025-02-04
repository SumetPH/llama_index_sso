from llama_index.core import Settings
from llm_llama_index.model import huggingface_embedding

Settings.embed_model = huggingface_embedding()

# import logging
# logging.basicConfig(level=logging.DEBUG)
# set_global_handler("simple")