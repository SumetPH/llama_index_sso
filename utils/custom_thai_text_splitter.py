from langchain.text_splitter import TextSplitter
from langchain_core.documents import Document
from pythainlp.tokenize import word_tokenize

class CustomThaiTextSplitter(TextSplitter):
    def __init__(self, chunk_size=1000, chunk_overlap=100):
        super().__init__()
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text):
        words = word_tokenize(text, keep_whitespace=False)  # ใช้ pythainlp tokenizer
        chunks = []
        start = 0

        while start < len(words):
            end = start + self.chunk_size
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            start += self.chunk_size - self.chunk_overlap  # ใช้ overlap เพื่อลดการสูญเสียข้อมูล

        return chunks

# 🔹 ใช้งาน Splitter กับ LangChain
text = "สวัสดีครับ วันนี้อากาศดีมาก ผมอยากไปเที่ยวทะเลกับเพื่อนๆ แต่ต้องทำงานก่อน"

splitter = CustomThaiTextSplitter(chunk_size=10, chunk_overlap=2)
chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {chunk}")
