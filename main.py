from minimal import create_app
import os

os.environ["SESSION_SECRET"]="MySessionSecret" 

app = create_app()
app.run(debug=True,host="0.0.0.0")
