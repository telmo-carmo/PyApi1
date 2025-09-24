
dev:  main.py
	fastapi dev --port 8080 main.py
	
run:  main.py
	fastapi run --port 8080 main.py
	
setup:
	pip install -U fastapi fastapi-cli uvicorn PyJWT Jinja2 python-multipart python-dotenv sqlmodel SQLAlchemy
	

	
clean:
	del *.Log PyApi1.log.*