from app import app
import os
from enrich import enrich

if __name__ == "__main__":
    print(enrich("Starting", "#FF4500"))
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
    # app.run(port=5000, debug=True)
    # app.run()

# Final
