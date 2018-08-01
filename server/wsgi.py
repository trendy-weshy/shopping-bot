
from manage import application as app
import os
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    app.run(port=os.getenv('PORT', default=5000), debug=True)