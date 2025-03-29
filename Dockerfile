FROM python:3.10
WORKDIR /hackathon_backend

COPY ./requirements.txt /hackathon_backend/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /hackathon_backend/requirements.txt

COPY ./app /hackathon_backend/app
COPY ./alembic.ini /hackathon_backend/alembic.ini
COPY ./alembic /hackathon_backend/alembic


# Copy script to run migrations and start server
COPY ./entrypoint.sh /hackathon_backend/entrypoint.sh

# Make the script executable
RUN chmod +x /hackathon_backend/entrypoint.sh

EXPOSE 7000

CMD ["/hackathon_backend/entrypoint.sh"]

