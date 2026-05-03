DIYlayout:
	echo "Running DIYLayoutCreator via flatpak"
	flatpak run com.diy_fever.DIYLayoutCreator > /tmp/layout_log.$$$$ 2>&1 &

arduinoIDE:
	echo "Running Arduino IDE via flatpak"
	flatpak run cc.arduino.IDE2 > /tmp/ide_log.$$$$ 2>&1 &

up:
	docker compose -f docker/docker-compose.yml up --build

upd:
	docker compose -f docker/docker-compose.yml up --build -d

down:
	docker compose -f docker/docker-compose.yml down

logs:
	docker compose -f docker/docker-compose.yml logs -f
