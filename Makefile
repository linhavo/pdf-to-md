WINDOWS_DIR := windows-runnable
MACOS_DIR   := macos-runnable
DIST_DIR    := dist

.PHONY: package-windows package-macos clean

package-windows: $(DIST_DIR)/pdf-convertor-windows/.built

package-macos: $(DIST_DIR)/pdf-convertor-macos/.built

$(DIST_DIR)/pdf-convertor-windows/.built: \
		requirements.txt \
		$(WINDOWS_DIR)/pdf-convertor-windows.py \
		$(WINDOWS_DIR)/watcher.py \
		$(WINDOWS_DIR)/start.bat \
		$(WINDOWS_DIR)/README.md
	powershell -NoProfile -Command "New-Item -ItemType Directory -Force -Path $(DIST_DIR)/pdf-convertor-windows | Out-Null; Copy-Item requirements.txt, $(WINDOWS_DIR)/pdf-convertor-windows.py, $(WINDOWS_DIR)/watcher.py, $(WINDOWS_DIR)/start.bat, $(WINDOWS_DIR)/README.md -Destination $(DIST_DIR)/pdf-convertor-windows"
	@powershell -NoProfile -Command "'' | Out-File -FilePath $(DIST_DIR)/pdf-convertor-windows/.built"
	@echo "Packaged -> $(DIST_DIR)/pdf-convertor-windows"

$(DIST_DIR)/pdf-convertor-macos/.built: \
		pdf-convertor.py \
		requirements.txt \
		$(MACOS_DIR)/watcher.py \
		$(MACOS_DIR)/start.command \
		$(MACOS_DIR)/README.md
	mkdir -p $(DIST_DIR)/pdf-convertor-macos
	chmod +x $(MACOS_DIR)/start.command
	cp $^ $(DIST_DIR)/pdf-convertor-macos/
	@touch $(DIST_DIR)/pdf-convertor-macos/.built
	@echo "Packaged -> $(DIST_DIR)/pdf-convertor-macos"

clean:
	rm -rf $(DIST_DIR)
