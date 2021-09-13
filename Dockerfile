FROM python:3.9-slim

WORKDIR /usr/src/app

RUN pip install pipenv==2021.5.29

COPY Pipfile Pipfile.lock ./
# PIP_NO_CACHE_DIR=off mean NO CACHING. This is stupid, but it's the way it is. See https://github.com/pypa/pip/issues/2897#issuecomment-115319916
RUN PIP_NO_CACHE_DIR=off pipenv install --system --deploy

COPY . .

CMD python -m uvicorn rarity_tools_scraper_api.main:app --host 0.0.0.0 --port 80
