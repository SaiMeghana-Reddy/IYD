# IYD
# Ramayana Fact Checker Bot

This is a chatbot that checks if a user statement is factually correct based on the Valmiki Ramayana.

It uses:
- Sentence embeddings to find relevant verses
- Groq's LLaMA-3 model to verify the statement
- Chainlit to run the chatbot interface

---

## How it works

1. Loads verses from `RamayanDataSet.csv`.
2. Uses sentence-transformers to find the top 3 most similar verses to the user's input.
3. Sends those verses and the input to Groq's LLaMA-3 model.
4. Returns one of the following:
   - ✅ True – If the statement is correct
   - ❌ False – If the statement is wrong
   - 🤔 None – If the statement is vague or irrelevant

---

## Setup Instructions

1. Install Python 3.9+ and create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
2. Install the required packages:


pip install -r requirements.txt

3.Set your Groq API Key:


export GROQ_API_KEY=your_key_here  # Linux/Mac
set GROQ_API_KEY=your_key_here     # Windows CMD
Place RamayanDataSet.csv in the same folder as app.py.

4.Run the chatbot:
   chainlit run app.py
