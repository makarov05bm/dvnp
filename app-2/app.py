from flask import Flask, render_template, render_template_string

app = Flask(__name__)

LOG_PATH = "/var/log/nginx/access_portal.log"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/logs')
def logs():
    try:
        with open(LOG_PATH, "r", errors="replace") as f:
            lines = f.readlines()[-200:]  # last 200 lines
    except FileNotFoundError:
        lines = ["(no logs yet)"]

    # Vulnerable: log lines are marked | safe, so Jinja2's default
    # auto-escaping is deliberately bypassed. Anything an attacker
    # got written into the log — including HTML/JS — renders as-is.
    template = """
    <!DOCTYPE html>
    <html>
    <head><title>nginx access log — sandbox-dev-001</title></head>
    <body style="background:#0d0d0d;color:#c9c9c9;font-family:monospace;padding:20px;">
      <h2 style="color:#e0a030;">nginx access log (last 200 lines)</h2>
      <div style="white-space:pre-wrap;">
      {% for line in lines %}{{ line | safe }}{% endfor %}
      </div>
    </body>
    </html>
    """
    return render_template_string(template, lines=lines)

@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/docs')
def docs():
    return render_template('docs.html')


@app.route('/docs/audit-report')
def report():
    return render_template('report.html')


@app.route('/repo-list')
def repo():
    return render_template('repo.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
