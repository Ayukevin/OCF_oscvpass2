docker run -d -p 127.0.0.1:8899:8080 \
	-v $(pwd)/setting.py:/app/setting.py \
	--link test oscv:latest

