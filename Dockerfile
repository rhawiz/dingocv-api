FROM python:2.7
RUN mkdir /app
ARG DATABASE_PATH
ARG MODELS_PATH
ENV DATABASE_PATH $DATABASE_PATH
ENV MODELS_PATH $MODELS_PATH
COPY . /app
RUN touch /app/.env
RUN pip install -r /app/requirements.txt
RUN pip install gunicorn
WORKDIR /app
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-b", "unix:dingocv.sock", "app:app"]