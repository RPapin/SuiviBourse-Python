start py api_app.py
timeout 2
start /wait curl http://localhost:5000/fetchData
git add .
git commit -m "auto push after fetch data"
git push 
taskkill /im py.exe
exit
