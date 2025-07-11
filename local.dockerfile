# Pull Python 3.12 on Debian Bookworm slim image
FROM python:3.12.3-slim-bookworm

# Upgrade and install basic packages
RUN apt-get update && apt-get -y upgrade && apt-get -y install nano build-essential && apt-get -y autoremove

# Create a non-root user
RUN useradd -m -u 1000 app_user

ENV HOME="/home/app_user"

USER app_user
# Set the working directory in the container
WORKDIR $HOME/app

# Copy only the requirements file to take advantage of layering (see: https://docs.cloud.ploomber.io/en/latest/user-guide/dockerfile.html)
COPY ./requirements.txt ./requirements.txt

# Setup Virtual environment
ENV VIRTUAL_ENV="$HOME/app/venv"
RUN python -m venv $VIRTUAL_ENV
RUN $VIRTUAL_ENV/bin/python -m ensurepip
RUN $VIRTUAL_ENV/bin/pip install --no-cache-dir --upgrade pip setuptools

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies
RUN $VIRTUAL_ENV/bin/pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY ./*.md ./LICENSE ./*.sh ./
COPY ./.env.docker /.env
COPY ./src/*.py ./src/
COPY ./src/css/*.css ./src/css/

# Expose the port to conect
EXPOSE 8765
# Run the application
ENTRYPOINT [ "/home/app_user/app/server.sh" ]
