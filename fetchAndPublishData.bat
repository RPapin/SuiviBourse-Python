start py api_app.py
timeout 2
start /wait curl http://localhost:5000/fetchData
git add .
git commit -m data.json
git push 