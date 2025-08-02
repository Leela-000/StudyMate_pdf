from transformers import pipeline

qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-base")

def answer_question(question, context):
    prompt = f"Answer the question based on the context.\nContext: {context}\nQuestion: {question}"
    result = qa_pipeline(prompt, max_length=150)
    return result[0]["generated_text"]

