FROM python:3.9

ENV DISPLAY=:99

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update

RUN apt-get install -y google-chrome-stable unzip wget curl
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

WORKDIR /usr/src/app

RUN pip install pipenv==2021.5.29

COPY Pipfile Pipfile.lock ./
# PIP_NO_CACHE_DIR=off mean NO CACHING. This is stupid, but it's the way it is. See https://github.com/pypa/pip/issues/2897#issuecomment-115319916
RUN PIP_NO_CACHE_DIR=off pipenv install --system --deploy

COPY . .

CMD python -m uvicorn rarity_tools_scraper_api.main:app --host 0.0.0.0 --port 80
