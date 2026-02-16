# Python ইমেজ
FROM python:3.9-slim

# ফোল্ডার সেটআপ
WORKDIR /app

# ফাইল কপি
COPY . /app

# রিকোয়ারমেন্টস ইন্সটল
RUN pip install --no-cache-dir -r requirements.txt

# Render কে বলা যে আমরা পোর্ট 10000 ব্যবহার করছি
EXPOSE 10000

# Gunicorn কমান্ড (Bind 0.0.0.0 তে হতে হবে)
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
