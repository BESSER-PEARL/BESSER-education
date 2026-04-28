# Use the official PostgreSQL image as a base
# You can specify a specific version, e.g., postgres:15 or postgres:latest
FROM postgres:latest

# Set environment variables for the database
# IMPORTANT: Replace 'mysecretpassword', 'myuser', and 'mydatabase'
# with your desired credentials and database name.
# It's generally recommended to pass sensitive data like passwords
# via build arguments or environment variables at runtime (`docker run -e`)
# rather than hardcoding them directly in the Dockerfile,
# especially for production environments.
ENV POSTGRES_PASSWORD=mysecretpassword
ENV POSTGRES_USER=myuser
ENV POSTGRES_DB=mydatabase

# The PostgreSQL server listens on port 5432 by default.
# Exposing the port allows communication with the container from the host
# or other containers. You'll still need to map it using `docker run -p`.
EXPOSE 5432

# Optional: Copy initialization scripts
# Any .sql or .sh files in this directory will be executed when the container
# is first started. This is useful for creating tables, seeding data, etc.
# Uncomment the following lines if you have initialization scripts
# in a local directory named 'init-db'.
# COPY ./init-db/ /docker-entrypoint-initdb.d/

# Default command to start the PostgreSQL server
# This is inherited from the base image and usually doesn't need to be changed.
CMD ["postgres"]
