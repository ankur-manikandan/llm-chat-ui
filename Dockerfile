FROM python:3.10

# Working directory
WORKDIR /app

# Copy all files from the current directory to the container's working directory
COPY . /app

# Install the Python packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port number that Streamlit listens on (default is 8501)
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "--server.port", "8501", "app.py"]