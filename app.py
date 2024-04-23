from flask import Flask, Response, redirect
from prometheus_client import Counter, generate_latest
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

# Counter to track the number of HTTP requests
http_requests_counter = Counter(
    'http_requests_total',
    'The total number of HTTP requests.',
    ['endpoint']  # Bu etiketlerin isimleri belirtiliyor
)

# Kullanıcı adı ve şifreleri tanımlayın (gerçek uygulamada bu bilgileri güvenli bir şekilde saklayın)
users = {
    "omer": "Password7"
}

# HTTPBasicAuth kullanarak kimlik doğrulaması yapın
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route("/")
def index():
    http_requests_counter.labels(endpoint="/").inc()  # Increment the counter for this endpoint
    return "/test'e gidiniz"

@app.route("/test")
def redirect_to_linkedin():
    http_requests_counter.labels(endpoint="/test").inc()  # Increment the counter for this endpoint
    return redirect("https://linkedin.com/in/omerfethicaner")

# PrometheusMetrics nesnesini oluştururken kimlik doğrulama decorator'ını kullanın
@app.route('/metrics')
@auth.login_required
def get_data():
    """Returns all data as plaintext."""
    http_requests_counter.labels(endpoint="/metrics").inc()  # Increment the counter for this endpoint
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
