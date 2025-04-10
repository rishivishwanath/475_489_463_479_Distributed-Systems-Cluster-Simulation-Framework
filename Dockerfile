FROM python:3.9-slim

WORKDIR /node

COPY nodes/node_template.py .

RUN pip install requests

CMD ["python","-u","node_template.py"]
