import subprocess
import os

os.chdir("./backend")

subprocess.run(["uvicorn", "backend:app","--host","0.0.0.0"])