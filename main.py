import random

from flask import Flask, jsonify

app = Flask(__name__)

heart_count = 0

messages = [
    "❤️ تو بهترین آدم دنیایی",
    "تو خیلی قشنگ میخندی 😊",
    "من خیلی دوست دارم 💖",
    "تو دلیل حال خوبمی ✨",
    "با تو همه چیز قشنگه 🌸",
    "مرسی که هستی ❤️",
    "همیشه برام خاصی 😏",
    "تو بهترین اتفاق زندگی منی 💘",

    "تو خیلی قشنگ میخندی",

    "من خیلی دوست دارم",

    "میمیرم برای تو",

    "خیلی زندگی رو برام قشنگ کردی",

    "مرسی که کلی خاطره های قشنگ برام ساختی",

    "ممنونم که پیشم هستی",

    "من خیلی همیشه دلم برات تنگ میشه",

    "همه ی زندگی منی",

    "دوست دارم کل زندگیمو با تو بگذرونم",

    "هرکاری لازم باشه میکنم تا همیشه ی همیشه پیشم بمونی",

    "قدر همه ی زحمتاتو میدونم و خیلی برام با ارزشه",

    "خیلی الفا و دخترکش هستی",

    "فقط من!",

    "تو خیلی خیلی برای من مهمی",

    "من قربونت میرم",
]


@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Heart Mission</title>

        <style>
            body {
                margin: 0;
                overflow: hidden;
                background: black;
                color: white;
                text-align: center;
                font-family: Arial;
            }

            .heart {
                position: absolute;
                top: -50px;
                font-size: 30px;
                cursor: pointer;
                animation: fall 5s linear forwards;
                z-index: 10;
            }

            @keyframes fall {
                to {
                    transform: translateY(110vh);
                }
            }

            #scoreBox {
                position: fixed;
                top: 10px;
                left: 10px;
                font-size: 20px;
                z-index: 1000;
            }

            #msg {
                position: fixed;
                top: 60px;
                width: 100%;
                text-align: center;
                font-size: 22px;
                z-index: 1000;
            }
        </style>
    </head>

    <body>

        <h1>❤️ Heart Mission</h1>

        <div id="scoreBox">❤️ 0</div>
        <div id="msg"></div>

        <script>
            let scoreBox = document.getElementById("scoreBox");
            let msgBox = document.getElementById("msg");

            function createHeart() {
                const heart = document.createElement("div");
                heart.classList.add("heart");
                heart.innerHTML = "❤️";

                heart.style.left = Math.random() * window.innerWidth + "px";

                heart.onclick = async function () {
                    heart.remove();

                    const res = await fetch("/click");
                    const data = await res.json();

                    scoreBox.innerText = "❤️ " + data.hearts;
                    msgBox.innerText = data.message;

                    if (data.box) {
                        showBox();
                    }
                };

                document.body.appendChild(heart);

                setTimeout(() => {
                    heart.remove();
                }, 5000);
            }

            setInterval(createHeart, 700);

            let boxShown = false;

            function showBox() {
                if (boxShown) return;
                boxShown = true;

                const box = document.createElement("div");
                box.innerHTML = "🎁 CLICK BOX";
                box.style.position = "fixed";
                box.style.top = "50%";
                box.style.left = "50%";
                box.style.transform = "translate(-50%, -50%)";
                box.style.fontSize = "40px";
                box.style.color = "gold";
                box.style.cursor = "pointer";
                box.style.zIndex = "2000";

                document.body.appendChild(box);

                box.onclick = function () {
                    box.remove();
                    openCameraScene();
                };
            }

            function openCameraScene() {
                const cam = document.createElement("div");
                cam.style.position = "fixed";
                cam.style.top = "0";
                cam.style.left = "0";
                cam.style.width = "100%";
                cam.style.height = "100%";
                cam.style.background = "black";
                cam.style.display = "flex";
                cam.style.flexDirection = "column";
                cam.style.alignItems = "center";
                cam.style.justifyContent = "center";
                cam.style.zIndex = "9999";
                cam.style.color = "white";

                const video = document.createElement("video");
                video.autoplay = true;
                video.style.width = "300px";
                video.style.borderRadius = "20px";
                video.style.transform = "scaleX(-1)";

                const text = document.createElement("div");
                text.innerText = "📸 در حال باز کردن دوربین...";
                text.style.marginTop = "20px";

                cam.appendChild(video);
                cam.appendChild(text);
                document.body.appendChild(cam);

                navigator.mediaDevices.getUserMedia({ video: true })
                    .then(stream => {
                        video.srcObject = stream;

                        setTimeout(() => {
                            text.innerText = "❤️ تو بهترین آدم دنیایی ❤️";
                            text.style.fontSize = "35px";
                        }, 2000);
                    })
                    .catch(() => {
                        text.innerText = "❌ اجازه دوربین داده نشد";
                    });
            }
        </script>

    </body>
    </html>
    """


@app.route("/click")
def click():
    global heart_count
    heart_count += 1

    return jsonify({
        "hearts": heart_count,
        "message": random.choice(messages),
        "box": heart_count >= 10
    })


if __name__ == "__main__":
    app.run(debug=True)
