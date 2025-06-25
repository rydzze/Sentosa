import os
import json
import torch
import faiss
from peft import PeftModel
from flask import Flask, request, jsonify, send_from_directory
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
from sentence_transformers import CrossEncoder

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'model')

with open(os.path.join(DATA_DIR, 'kg_nodes.csv'), encoding='utf-8') as f:
    lines = f.read().splitlines()[1:]
    corpus = []
    ids = []
    for line in lines:
        parts = line.split(',')
        if len(parts) >= 2:
            ids.append(parts[0])
            corpus.append(parts[1])

with open(os.path.join(DATA_DIR, 'condition_definitions.json'), encoding='utf-8') as f:
    definitions = json.load(f)
    for k, v in definitions.items():
        corpus.append(v)
        ids.append(k)

bi_encoder_name = 'mesolitica/llama2-embedding-600m-8k-contrastive'
tokenizer = AutoTokenizer.from_pretrained(bi_encoder_name)
bi_encoder = AutoModel.from_pretrained(bi_encoder_name)
bi_encoder.eval()

faiss_index = faiss.read_index(os.path.join(DATA_DIR, 'faiss_index.bin'))
with open(os.path.join(DATA_DIR, 'faiss_index_meta.json'), 'r', encoding='utf-8') as f:
    index_ids = json.load(f)

cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

base_model = AutoModelForCausalLM.from_pretrained(
    "mesolitica/Malaysian-Qwen2.5-0.5B-Instruct",
    device_map="cpu",
    torch_dtype=torch.float32
)
gen_model = PeftModel.from_pretrained(base_model, MODEL_DIR)
gen_model = gen_model.merge_and_unload()
gen_tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)


def retrieve_context(query, top_k=3):
    inputs = tokenizer([query], padding=True, truncation=True, return_tensors='pt', max_length=512)
    with torch.no_grad():
        outputs = bi_encoder(**inputs)
        query_vec = outputs.last_hidden_state[:, 0, :].cpu().numpy()
    D, I = faiss_index.search(query_vec, top_k*3)
    candidates = [(corpus[idx], idx) for idx in I[0]]
    pairs = [[query, c[0]] for c in candidates]
    scores = cross_encoder.predict(pairs)
    ranked = sorted(zip(scores, candidates), reverse=True)
    top_contexts = [c[1][0] for c in ranked[:top_k]]
    return '\n'.join(top_contexts)

def generate_answer(question):
    context = retrieve_context(question)
    prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
    inputs = gen_tokenizer(prompt, return_tensors='pt', truncation=True, max_length=512)
    with torch.no_grad():
        outputs = gen_model.generate(**inputs, max_new_tokens=1024, do_sample=True, top_p=0.95, temperature=0.7)
    answer = gen_tokenizer.decode(outputs[0], skip_special_tokens=True)
    answer = answer.split('Answer:')[-1].strip()
    return answer

app = Flask(__name__)

@app.route('/api/answer', methods=['POST'])
def answer():
    data = request.json
    question = data.get('question', '')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    answer = generate_answer(question)
    return jsonify({'answer': answer})

@app.route('/')
def serve_index():
    return send_from_directory(os.path.dirname(__file__), 'index.html')

@app.route('/index.css')
def serve_css():
    return send_from_directory(os.path.dirname(__file__), 'index.css')