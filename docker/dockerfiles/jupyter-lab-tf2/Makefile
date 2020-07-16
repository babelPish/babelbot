
help:
	@echo "make"
	@echo "    build-gpu"
	@echo "        build image(gpu)"
	@echo "    build-cpu"
	@echo "        build image(cpu)"
	@echo "    push-gpu"
	@echo "        push gpu image to repo"
	@echo "    push-cpu"
	@echo "        push cpu image to repo"

build-gpu :
	docker build -t babelpish/babelbot:tf2.2-gpu ./jupyter-lab-tf2.2-gpu

push-gpu :
	docker push babelpish/babelbot:tf2.2-gpu
