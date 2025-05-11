# DocQA-System

This is a system that allows users to upload a PDF of their chosing, ask natural language questions, and obtain answers based on the contents of the PDF. This is done by automatically extracting the contents of the PDF, creating embeddings, and indexing it using FAISS. 

This system uses streamlit as its front-end, and fast-api as its backend. 

# REQUIREMENTS

Clone the repository using: 
```git clone https://github.com/anumitad/DocQA-System.git```

In order to get the python dependencies required, run the command:

```pip install -r requirements.txt```

Open two python terminals. 

- To start the fastapi backend, run the following in one terminal: 
```fastapi dev main.py```

- To start the streamlit front end, run the following in the second terminal: 
```python3 -m streamlit run app.py```

After starting the frontend, and backend through the terminal:

- To acess the fastapi backend, in your browser open:
```http://127.0.0.1:8000/docs```

- To access the streamlit frontend, in your browser open:
```http://127.0.0.1:8501```
