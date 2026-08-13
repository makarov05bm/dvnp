from flask import Flask, render_template, render_template_string, request, jsonify

app = Flask(__name__)

LOG_PATH = "/var/log/nginx/access_portal.log"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "sky321blue"
ADMIN_TOKEN = "tok_SSHKEYS0000000000000000"

MOCK_SSH_KEYS = [
    {
        "name": "id_rsa (deploy key, prod)",
        "type": "PRIVATE KEY",
        "content": (
            "-----BEGIN OPENSSH PRIVATE KEY-----\n"
            "b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn\n"
            "NhAAAAAwEAAQAAAYEAwT5exampleFAKEmockDATAdoNOTuseANYWHEREb3B1YmxpY2tleQ\n"
            "MOCKDATAMOCKDATAMOCKDATAMOCKDATAMOCKDATAMOCKDATAMOCKDATAMOCKDATA\n"
            "-----END OPENSSH PRIVATE KEY-----"
        ),
    },
    {
        "name": "id_rsa.pub (deploy key, prod)",
        "type": "PUBLIC KEY",
        "content": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC7mockFAKEkeyDONOTUSE deploy@skyblue-prod",
    },
    {
        "name": "authorized_keys (jump host)",
        "type": "AUTHORIZED KEYS",
        "content": (
            "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFAKEmockKEYDATA jdev@laptop\n"
            "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQMOCKDATAonly svc-backup@skyblue-prod"
        ),
    },
]


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


@app.route('/v1/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@app.route('/v1/login', methods=['POST'])
def login_submit():
    data = request.get_json(silent=True) or request.form
    username = data.get('username', '')
    password = data.get('password', '')
 
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return jsonify({"token": ADMIN_TOKEN}), 200
 
    return jsonify({"error": "invalid credentials"}), 401


@app.route('/ssh_keys')
def ssh_keys_page():
    # The page shell itself has no server-side gate -- the actual check
    # happens client-side in JS against localStorage, then again
    # server-side when the page calls /api/ssh_keys for the real data.
    return render_template('ssh_keys.html')
 
 
@app.route('/api/ssh_keys')
def ssh_keys_api():
    auth = request.headers.get('Authorization', '')
    token = auth.replace('Bearer ', '').strip()
 
    if token != ADMIN_TOKEN:
        return jsonify({"error": "unauthorized"}), 401
 
    return jsonify({"keys": MOCK_SSH_KEYS}), 200


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
