FROM python:3.9-slim

WORKDIR /node
COPY nodes/node_template.py .

CMD ["python", "node_template.py"]
