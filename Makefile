
run:  main.py
	fastapi dev --port 8080 main.py
	
setup:
	pip install -U fastapi uvicorn PyJWT Jinja2 python-multipart sqlmodel
	

	
clean:
	del *.Log PyApi1.log.*