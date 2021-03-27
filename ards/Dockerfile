FROM python:3.7 as build

WORKDIR /usr/src/app

# Copy code
COPY main.py process.py requirements.txt /usr/src/app/
COPY proto          /usr/src/app/proto
COPY config         /usr/src/app/config
COPY corpus         /usr/src/app/corpus
COPY data_loaders   /usr/src/app/data_loaders
COPY layers         /usr/src/app/layers
COPY models         /usr/src/app/models
COPY modules        /usr/src/app/modules
COPY scoring        /usr/src/app/scoring
COPY utils          /usr/src/app/utils

# Copy model
COPY model          /usr/src/app/model

# pip install
RUN python3 -m pip install --no-cache-dir -r requirements.txt  && \
    python3 -m spacy download en                                                     

CMD [ "python", "./main.py" ]