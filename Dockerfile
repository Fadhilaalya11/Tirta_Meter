# Gunakan image resmi Python
FROM python:3.10-slim

# Install dependensi sistem (termasuk libGL)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy semua file ke container
COPY . .

# Install dependensi Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Ekspos port default Railway (8080!)
EXPOSE 8080

# Jalankan Streamlit saat container dimulai (dengan port 8080)
CMD ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]
