from redis.commands.search.field import VectorField, TextField

SCHEMA = [
    TextField("Id"),
    TextField("Content"),
    TextField("FileName"),
    VectorField("Embedding", "FLAT", {"TYPE": "FLOAT32", "DIM": 3072, "DISTANCE_METRIC": "COSINE"}),
]

EMBEDDING_MODEL = "text-embedding-3-large"

LLM_MODEL = "gpt-4o"
# LLM_MODEL = "gpt-3.5-turbo-1106"

TIKTOKEN_ENCODING = "cl100k_base"

MAX_TOKENS_PER_REQUEST = 8191
