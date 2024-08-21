FROM python:3.12
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN pip install poetry
RUN poetry install --no-dev

COPY . /app
EXPOSE 8080
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV FLASK_APP=main.py


CMD ["poetry", "run", "python", "main.py"]

