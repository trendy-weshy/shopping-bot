
from manage import application as app
import os


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('PORT', default=5000), debug=True)