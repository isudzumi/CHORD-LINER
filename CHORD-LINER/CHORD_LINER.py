from chalice import Chalice

app = Chalice(app_name="chord-liner")

@app.route('/', methods=['POST'])
def index():
    request = app.current_request
    print(request.json_body)