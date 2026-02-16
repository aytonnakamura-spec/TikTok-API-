from flask import Flask, request, jsonify, redirect
import requests
import os

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_tiktok():
    video_url = request.args.get('url')
    format_type = request.args.get('format', 'mp4')  # mp4 or mp3

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # TikWM API Call (No Cookies Needed)
        api_url = "https://www.tikwm.com/api/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        }
        data = {"url": video_url, "hd": 1}  # hd=1 মানে আমরা HD চাই

        response = requests.post(api_url, headers=headers, data=data)
        result = response.json()

        if result.get("code") == 0:
            data = result.get("data", {})
            
            # --- 720p/HD Quality Logic ---
            # প্রথমে hdplay খুঁজবে, না পেলে play (normal) নেবে
            hd_video = data.get("hdplay") 
            normal_video = data.get("play")
            wm_video = data.get("wmplay") # ওয়াটারমার্ক সহ (ব্যাকআপ)
            
            # অডিও লিঙ্ক
            audio_url = data.get("music")

            # রিডাইরেক্ট লজিক
            if format_type == 'mp3':
                if audio_url:
                    return redirect(audio_url)
                else:
                    return jsonify({"error": "Audio not found"}), 404
            else:
                # ভিডিওর জন্য: আগে HD, না থাকলে নরমাল, তাও না থাকলে ওয়াটারমার্ক
                final_url = hd_video if hd_video else (normal_video if normal_video else wm_video)
                
                if final_url:
                    return redirect(final_url)
                else:
                    return jsonify({"error": "Video not found"}), 404

        else:
            return jsonify({"error": "Failed to fetch video. Might be private/deleted or API limit."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
