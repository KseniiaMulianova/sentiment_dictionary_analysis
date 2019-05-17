import nltk
from src import TEXT_CHUNK_SIZE
from nltk.tokenize import sent_tokenize

class TextParser:

    def build_chunks(self, text):
        tokenizer = nltk.data.load('tokenizers/punkt/russian.pickle')
        sentences = tokenizer.tokenize(text)
        sentences.reverse()

        chunk = TextChunk()

        while len(sentences) > 0:
            sentence = sentences.pop()
            if chunk.append(sentence):
                continue
            else:
                yield chunk
                chunk = TextChunk()
                chunk.append(sentence)

        yield chunk


class TextChunk:
    def __init__(self):
        self.sentences = []
        self.free_space = TEXT_CHUNK_SIZE

    def append(self, sentence):
        sentence_length = len(sentence)
        if sentence_length <= self.free_space:
            self.sentences.append(sentence)
            self.free_space -= sentence_length
        else:
            return False

        return True

    @classmethod
    def from_text(cls, text):
        sentences = sent_tokenize(text)
        chunk = cls()
        for sentence in sentences:
            if chunk.append(sentence):
                continue
            else:
                return chunk

        return chunk

    def __str__(self):
        return ''.join(self.sentences)
