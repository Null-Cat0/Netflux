FROM ubuntu:latest
RUN apt-get update && apt-get install -y sqlite3
VOLUME ./instance
RUN sqlite3 ./instance/user.db
CMD ["sqlite3", "./instance/user.db"]
