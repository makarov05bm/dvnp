from flask import Flask, request, Response, make_response, render_template, jsonify, g, redirect
import os
import logging
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Extract remote_addr from X-Forwarded-For (skip 1 reverse proxy from the right)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# --- Method override middleware --------------------------------------
@app.before_request
def method_override():
    override = request.headers.get("X-HTTP-Method-Override")
    if override:
        request.environ["REQUEST_METHOD"] = override.upper()
        request.method = override.upper()


# Mock in-memory "session store"
# token -> user record. In a real app this would be a DB/redis lookup.
VALID_SESSIONS = {
    "sess_VICTIM0000000000000000": {
        "username": "marshmallow",
        "email": "marshmallow@skyblue.com",
        "admin": "1",
    }
}

# Mock incident data, styled after real status-page products
# (Statuspage, Cachet). In a real deployment this would come from a
# database of actual incidents.
INCIDENTS = {
    "1042": {
        "id": "1042",
        "title": "Elevated error rates on API Gateway",
        "component": "API Gateway",
        "date": "August 9, 2026",
        "status_class": "resolved",
        "status_label": "Resolved",
        "updates": [
            {"time": "14:52 UTC", "status": "Resolved",
             "text": "This incident has been resolved. Error rates have returned to baseline."},
            {"time": "14:20 UTC", "status": "Monitoring",
             "text": "A fix has been deployed. We are monitoring error rates before marking this resolved."},
            {"time": "13:41 UTC", "status": "Investigating",
             "text": "We are investigating elevated 5xx error rates on the API Gateway."},
        ],
    },
    "1041": {
        "id": "1041",
        "title": "Increased latency on Reporting Service",
        "component": "Reporting Service",
        "date": "August 6, 2026",
        "status_class": "monitoring",
        "status_label": "Monitoring",
        "updates": [
            {"time": "09:15 UTC", "status": "Monitoring",
             "text": "Latency has improved following a database index rebuild. Continuing to monitor."},
            {"time": "08:30 UTC", "status": "Investigating",
             "text": "Users may notice slower load times on report generation. Investigating root cause."},
        ],
    },
}
 
DEFAULT_INCIDENT = {
    "id": "0000",
    "title": "All Systems Operational",
    "component": "Platform",
    "date": "August 11, 2026",
    "status_class": "resolved",
    "status_label": "Operational",
    "updates": [
        {"time": "00:00 UTC", "status": "Operational",
         "text": "All Skyblue Systems services are operating normally."},
    ],
}

# --- Endpoints -------------------------------------------------
@app.route('/admin', methods=['GET'])
def admin():
    token = request.cookies.get("session")
    user = VALID_SESSIONS.get(token)
    app.logger.info("cookie=%s", token)
 
    if not user:
        return jsonify({"error": "unauthenticated"}), 401
    
    return render_template('admin.html')


@app.route('/download')
def download():
    user_file = request.args.get("file")
    if not user_file:
        return render_template('download_error.html'), 400
    response = make_response()
    response.headers["X-Accel-Redirect"] = f"/protected/user-data/{user_file}"
    response.headers["Content-Disposition"] = f'attachment; filename="{user_file}"'
    return response


@app.route('/assets/<path:req_path>')
def read_file(req_path):
    target = os.path.join('static-data', req_path)
    try:
        with open(target, 'rb') as f:
            return f.read(), 200, {'Content-Type': 'text/plain'}
    except Exception as e:
        return f"Error: {e}", 404


@app.route("/internal/debug")
def debug():
    app.logger.info("remote_addr=%s", request.remote_addr)
    app.logger.info("headers=%s", dict(request.headers))
    # Second layer of defense, however still vulnerable as it blindly trusts X-Forwarded-For (remote_addr)
    if not request.remote_addr.startswith("10."):
        return "Forbidden", 403

    return dump_logs()


@app.route('/preview-link')
def preview_link():
    incident_id = request.args.get('incident')
    incident = INCIDENTS.get(incident_id, DEFAULT_INCIDENT)
 
    forwarded_host = request.headers.get('X-Forwarded-Host', request.host)
    canonical_url = f"https://{forwarded_host}/preview-link?incident={incident['id']}"
 
    return render_template('preview_link.html', incident=incident, canonical_url=canonical_url)

@app.route('/set_admin_session', methods=['GET'])
def login():
    """
    Toy login: issues the victim's session cookie.
    In the real world this would follow a real credential check —
    here we just hand out the mock victim's session directly so the
    lab can demonstrate the caching bug without building a full auth flow.
    """
    token = "sess_VICTIM0000000000000000"
    resp = make_response(f"Logged in. Session cookie set ({token}).")
    resp.set_cookie("session", token, httponly=True)
    return resp
 
 
@app.route('/account/session')
@app.route('/account/session/<path:extra>')
def account(extra=None):
    token = request.cookies.get("session")
    user = VALID_SESSIONS.get(token)
 
    if not user:
        return jsonify({"error": "unauthenticated"}), 401
 
    return jsonify({
        "username": user["username"],
        "email": user["email"],
        "admin": user["admin"],
        "session_token": token,
    })


@app.route("/upload", methods=["POST", "PUT"])
def upload():
    filename = request.headers.get("X-Filename")
 
    if not filename:
        return jsonify({"error": "missing X-Filename header"}), 400
 
    safe_name = os.path.basename(filename)
    target_path = os.path.join(UPLOAD_DIR, safe_name)

    if request.method == "POST":
        if os.path.exists(target_path):
            return jsonify({
                "error": "file already exists",
                "hint": "use PUT to update an existing file"
            }), 409
 
        data = request.get_data()
        with open(target_path, "wb") as f:
            f.write(data)
 
        return jsonify({
            "status": "created",
            "filename": safe_name,
            "bytes": len(data),
        }), 201
 
    if request.method == "PUT":
        data = request.get_data()
        with open(target_path, "wb") as f:
            f.write(data)
 
        return jsonify({
            "status": "overwritten",
            "filename": safe_name,
            "bytes": len(data),
        }), 200

 
@app.route('/secret', methods=['GET'])
def secret():
    return render_template('secret.html')
 

@app.route('/private', methods=['GET'])
def private():
    return render_template('private.html')


@app.route('/topsecret', methods=['GET'])
def topsecret():
    return render_template('topsecret.html')


@app.route('/status', methods=['GET'])
def api():
    return render_template('api.html')

@app.route('/changelog', methods=['GET'])
def changelog():
    return render_template('changelog.html')


@app.route('/')
def home():
    return render_template('home.html')


def dump_logs():
    logs = """
[2026-08-07 08:12:14] INFO  User 'alice' logged in from 10.0.0.12
[2026-08-07 08:13:01] INFO  User 'bob' requested /api/orders
[2026-08-07 08:13:45] WARN  Failed login attempt for user 'admin' from 203.0.113.45
[2026-08-07 08:14:20] INFO  Admin 'charlie' accessed /internal/debug
[2026-08-07 08:15:07] ERROR Database connection timeout (retry succeeded)
[2026-08-07 08:16:31] INFO  Backup completed successfully
[2026-08-07 08:17:10] INFO  User 'david' uploaded report.pdf
[2026-08-07 08:18:52] INFO  Scheduled cleanup job finished
"""
    return Response(logs, mimetype="text/plain")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000)
