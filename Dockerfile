# İlk aşama: Uygulama bağımlılıklarını yükleme
FROM python:3.9-slim AS builder

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# İkinci aşama: Uygulama dosyalarını kopyalama
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies installed in the first stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port number on which the Flask app runs
EXPOSE 5000

# Define the command to run your Flask app when the container starts
CMD ["python", "app.py"]
