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

## Progress Tracking

- [x] make resume -> data extraction + upload to db endpoints
- [x] make job description -> data extraction + upload to db endpoints
- [ ] make resume data -> job matching algorithm
- [ ] config database and test uploading and fetching for resumes and jobs
- [ ] write api combining all logic
  - make sure to have protective logic, only 2 pages of all resumes are read, etc.
- [ ] connect to frontend
- [ ] loc frontend behind login and account logic
  - upload resume
  - runs the api
  - shows the 'best' or 'worst' internship match
  - has the rest of them blurred
  - if user tries to interact, put a login popup
  - once user logs in, save their user data, resume, internships
  - every time they login, it will show the saved data
  - only interaction user will have is the ability to upload a new resume for more jobs
  - can do a lil bit of post processing where llm gives user some advice / give a complement

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
