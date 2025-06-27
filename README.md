# 🤗 Sentosa: A Malay Language Mental Health Question Answering System Using NLP


## 📌 Introduction  

**Sentosa** is a **mental health question answering system** developed for the **Malay language**. It aims to provide fast, reliable, and privacy-preserving answers to mental health-related queries. The system is built to help users understand symptoms, get self-care advice, and know when to seek professional help—all within a user-friendly conversational interface. It leverages state-of-the-art **natural language processing (NLP) tools**, a **knowledge graph** for structured information, and **retrieval-augmented generation (RAG)** techniques to deliver accurate responses.


## ❗ Problem Statements

🔸 **Language Accessibility** - Most mental health QA systems are English-centric, excluding non-English speaking users, especially those in Malaysia. <br>
🔸 **Stigma and Privacy** - Cultural stigma around mental health deters many from seeking help. A safe, anonymous, self-help platform is necessary. <br>
🔸 **Limited Local Resources** - There is a lack of structured, validated Malay datasets and systems to support mental health literacy.


## 🎯 Objectives  

✅ **Develop a Malay-focused QA System** - Build a question answering platform that understands and responds in Bahasa Melayu. <br>
✅ **Integrate Knowledge Graphs** - Use lightweight know    ledge graphs to capture structured insights from Malay health articles. <br>
✅ **Leverage RAG and LLMs** - Employ retrieval-augmented generation and fine-tuned language models to provide context-aware answers.


## 🔥 System Features  

🧠 **Preprocessing Pipeline** - Utilises **Malaya NLP toolkit** for stemming, tokenisation, and stopword removal tailored for Malay. <br>
🌐 **Knowledge Graph Creation** - Constructs **RDF-based graphs** with **OWL ontology support** for conditions, symptoms, triggers, and treatments. <br>
🔍 **Entity and Relation Extraction** - Automatically identifies medical conditions and builds semantic relations using heuristics. <br>
🤖 **Retrieval-Augmented Generation (RAG)** - Combines **FAISS-based vector search** with cross-encoder re-ranking. <br>
🗣️ **Fine-Tuned Instruction Model** - Trains a **Malay Qwen2.5-based model** using LoRA adapters and low-bit quantisation. <br>
💬 **Chat Interface** - Deployed using **Flask** with a smooth, interactive frontend for seamless question answering. <br>
🌍 **Bilingual Support** - Automatically translates English questions to Malay and provides English responses.


## 🛠️ Installation Guide  

1️⃣ **Clone the repository**

```bash
git clone https://github.com/rydzze/Sentosa.git
cd Sentosa
```

2️⃣ **Create a virtual environment**

```bash
python -m venv venv
```

3️⃣ **Install dependencies (activate venv first)**

```bash
pip install -r requirements.txt
```

4️⃣ **Run the application**

```bash
python run.py
```

5️⃣ **Access the system via:** 🌍

```
http://localhost:988
```


## 📸 **Screenshots of User Interface**

![image](https://github.com/user-attachments/assets/0b5aa8c7-a332-4af9-9c98-dc6a8ed4f92a)

![image](https://github.com/user-attachments/assets/8da1d614-8ae0-4188-8c4c-f5f4b1848e77)

![image](https://github.com/user-attachments/assets/f7af8874-a88d-4206-bb35-374cfd2b7a5c)


## 🏆 Contribution

We would like to thank the following team members for their contributions:

- [Muhammad Ariff Ridzlan](https://github.com/rydzze)
- [Noor Alia Alisa](https://github.com/alia4lisa)
- [Ignatius Ng Wei Siong](https://github.com/Characters88)
- [Ivanna Lin Yi Ying](https://github.com/IvannaLin)
