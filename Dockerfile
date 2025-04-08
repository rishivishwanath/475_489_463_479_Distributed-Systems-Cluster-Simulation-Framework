FROM python:3.9-slim

WORKDIR /node

COPY nodes/node_template.py .

# Install requests
RUN pip install requests

CMD ["python", "node_template.py"]
