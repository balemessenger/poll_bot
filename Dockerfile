FROM python:3.7
WORKDIR /poll_bot

ENV TZ 'Asia/Tehran'
RUN pip install --upgrade pip && \
    cp /usr/share/zoneinfo/Asia/Tehran /etc/localtime && \
    echo $TZ > /etc/timezone
RUN pip install cryptography --no-binary cryptography
COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
COPY ./ ./

RUN pip install -e .
CMD ["python", "polling_bot/main.py"]
ENV PYTHONPATH /poll_bot
