WINDOWS_DIR := windows-runnable
MACOS_DIR   := macos-runnable
DIST_DIR    := dist

.PHONY: package-windows package-macos clean

package-windows: $(DIST_DIR)/pdf-convertor-windows.zip

package-macos: $(DIST_DIR)/pdf-convertor-macos.zip

$(DIST_DIR)/pdf-convertor-windows.zip: \
		requirements.txt \
		$(WINDOWS_DIR)/pdf-convertor-windows.py \
		$(WINDOWS_DIR)/watcher.py \
		$(WINDOWS_DIR)/start.bat \
		$(WINDOWS_DIR)/README.md
	mkdir -p $(DIST_DIR)
	zip -j $@ $^
	@echo "Packaged -> $@"

$(DIST_DIR)/pdf-convertor-macos.zip: \
		pdf-convertor.py \
		requirements.txt \
		$(MACOS_DIR)/watcher.py \
		$(MACOS_DIR)/start.command \
		$(MACOS_DIR)/README.md
	mkdir -p $(DIST_DIR)
	chmod +x $(MACOS_DIR)/start.command
	zip -j $@ $^
	@echo "Packaged -> $@"

clean:
	rm -rf $(DIST_DIR)
