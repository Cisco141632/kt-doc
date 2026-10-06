# Start from an official Python image ("slim" = small Debian base)
FROM python:3.13-slim

# Work inside /app from now on (created if it does not exist)
WORKDIR /app

# Create a normal user, so the app does not run as root
RUN useradd --create-home appuser

# Copy only the dependency list first, so the install step below stays cached
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source code, owned by that user so it can read the files
COPY --chown=appuser:appuser . .

USER appuser

# Document the port the app listens on (this does not publish it)
EXPOSE 8000

# The command that runs when a container starts
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "app:app"]
