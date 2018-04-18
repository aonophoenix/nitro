FROM python:3

WORKDIR /usr/src/nitro

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY process_input.py ./process_input.py
COPY data/*.xls ./data/
RUN mkdir results

CMD [ "python", "./process_input.py" ]
# CMD ["bash"]
