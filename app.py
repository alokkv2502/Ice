from flask import Flask, render_template, request, jsonify
from ice_breaker import ice_break

app = Flask(__name__)

@app.route("/")
def index():
    # This will render an index.html file located in the 'templates' directory.
    return render_template("index.html")
@app.route("/process", methods=["POST"])
def process():
    try:
        name = request.form.get("name")
        if not name:
            return jsonify({"error": "Name not provided"}), 400

        person_info, profile_pic_url = ice_break(name=name)

        return jsonify({
            "summary": person_info.summary,
            "interests": person_info.topics_of_interest,
            "facts": person_info.facts,
            "ice_breakers": person_info.ice_breakers,
            "picture_url": profile_pic_url
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
