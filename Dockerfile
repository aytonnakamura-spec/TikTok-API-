# Python 3.9 ইমেজ ব্যবহার করা হচ্ছে
FROM python:3.9-slim

# ওয়ার্কিং ডিরেক্টরি সেট করা
WORKDIR /app

# ফাইল কপি করা
COPY . /app

# রিকোয়ারমেন্টস ইন্সটল করা
RUN pip install --no-cache-dir -r requirements.txt

# পোর্ট এক্সপোজ করা (Render এর জন্য)
EXPOSE 10000

# অ্যাপ রান করা
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:10000", "app:app"]
