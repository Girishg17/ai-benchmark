# AI Benchmark

This project implements a multi-model routing system that benchmarks and routes user queries to the best AI models dynamically. It supports offline benchmarking, model routing with exploration-exploitation strategies, and API integrations with OpenAI, Perplexity AI, and others.

---

## Prerequisites

- Python 3.9 or higher
- Virtual environment tool (optional but recommended)

---

## Setup

1. **Clone the repository** using
`git clone ` and go to codebase through `cd ai-benchmark`

2. **Create and activate a virtual environment**
 ```
    python3 -m venv .venv
   
   source .venv/bin/activate # for Linux/macOS User
      or 
   .venv\Scripts\activate # for Windows user
   ```

3. **Install dependencies**

```
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root with your OpenAI API key or [RAPID API Key] (https://rapidapi.com/) (free need just to login and subscribe )

### Offline Benchmarking (Not Recommended, You can skip this step)

Evaluate models on benchmark datasets and initialize routing stats :
You can skip this step as its Time consuming process. 
```
python -m scripts.run_offline_bench
```
Basically It request for your model and assigns the score for your model with the predetermined benchmark question.

Note: not recommended as API hit extreme so you might expire api request per day

### Interactive CLI (Recommended)

Start the interactive command line interface to ask questions and get routed answers:
```
python -m scripts.cli
```

Type your question, provide feedback on answers (y/n), or exit with `exit` or `quit`.

It would update the score for model based on your feedback.

The routing system balances exploration and exploitation (using [UCB] (https://www.geeksforgeeks.org/machine-learning/upper-confidence-bound-algorithm-in-reinforcement-learning/) ) to ensure every model, including new or less-tested ones, gets a fair chance to be selected and evaluated over time 

---

## Notes

- The offline benchmark sends queries to real models as configured, so API usage applies.
- Model success rates are updated after benchmarking and feedback, improving routing decisions.
- Use `python-dotenv` package to manage environment variables loading.

---

## Troubleshooting

- If you see API key errors, check your `.env` file and ensure the environment variable is loaded.
- If benchmark reports 0 samples processed, verify the benchmark data files exist and have valid JSONL data.
- For logging or debug info, check the configured logger output.

---

Feel free to DEBUG, extend and customize models, benchmark datasets, and routing policies as needed.

Happy Coding!.

---








