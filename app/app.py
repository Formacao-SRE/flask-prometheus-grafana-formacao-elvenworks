from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics
import time
app = Flask(__name__)
metrics = PrometheusMetrics(app)

metrics.info('app_info', 'Application info', version='1.0.3')

@app.route('/education')
@metrics.counter('invocation_by_education', 'Request count by request paths',
        labels={'path': lambda: request.path})
def education():
    return 'Elvenwork Bootcamp education.'

@app.route('/admin')
@metrics.counter('invocation_by_admin', 'Request count by request paths',
        labels={'path': lambda: request.path})
def admin():
    return 'Elvenwork Bootcamp admin.'

@app.route('/lesson')
@metrics.gauge('in_progess', 'Long running requests in progress')
def lesson():
    time.sleep(10)
    return 'Elvenworks Bootcamp lesson!'

@app.route('/status/<int:status>')
@metrics.do_not_track()
@metrics.summary('requests_by_status', 'Request latencies by status',
                 labels={'status': lambda r: r.status_code})
@metrics.histogram('requests_by_status_and_path', 'Request latencies by status and path',
                   labels={'status': lambda r: r.status_code, 'path': lambda: request.path})
def echo_status(status):
    return 'Status: %s' % status, status

if __name__ == '__main__':
    app.run()
