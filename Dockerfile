FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DOCKER=true
ENV MODEL=EpsilonGreedy

EXPOSE 8050

CMD [ "python", "./src/main.py" ]