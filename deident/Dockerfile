FROM python:3.7 as build

WORKDIR /usr/src/app

# Copy code
COPY main.py process.py requirements.txt /usr/src/app/
COPY proto          /usr/src/app/proto
COPY trained_models /usr/src/app/trained_models
COPY nn             /usr/src/app/nn

# pip install
RUN python3 -m pip install --no-cache-dir -r requirements.txt                         && \
    python3 -m spacy download en                                                      && \
    mkdir data                                                                        && \
    wget -P data/word_vectors http://neuroner.com/data/word_vectors/glove.6B.100d.zip && \
    unzip data/word_vectors/glove.6B.100d.zip -d data/word_vectors/                   && \
    rm data/word_vectors/glove.6B.100d.zip

CMD [ "python", "./main.py" ] 