# best-intern

100x faster internship search

## TODOs:

- get a list of a ton of internships
- parse data for each link into txt
- go through each txt and build a data schema for each internship / job
- save them to the database
- build the same general schema for resumes
- use llm/other stuff to combine the most fitting jobs and resumes

1. make internship data schema
2. make resume data schema
3. make resume->internship match algorithm

## 🛠️ Environment Setup

Make sure Python, [ngrok](https://ngrok.com/), and [uv]() are installed.

```bash
# 1 Navigate to the repository. Install [uv](https://github.com/astral-sh/uv):
pip install uv

# 2. Create a virtual environment at .venv
uv venv

# 3. Activate environment.
source .venv/bin/activate # macOS and Linux
.venv\Scripts\activate # Windows

# 4. Install dependencies
uv pip install -r requirements.txt

# Extra: Save added dependencies
uv pip freeze > requirements.txt
```
