#!/bin/bash
cd "$(dirname "$0")"

echo "============================"
echo "      PDF Konvertor"
echo "============================"
echo

if [ ! -d ".venv" ]; then
    echo "První spuštění – probíhá nastavení..."
    echo

    if ! java -version &>/dev/null 2>&1; then
        echo "CHYBA: Java není nainstalována."
        echo "Nainstalujte OpenJDK z https://adoptium.net/ nebo přes Homebrew:"
        echo "  brew install openjdk"
        echo "Pak tento soubor spusťte znovu."
        read -rp "Stiskněte Enter pro ukončení..."
        exit 1
    fi

    echo "Instaluji závislosti (může to chvíli trvat)..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "CHYBA: Nepodařilo se vytvořit virtuální prostředí. Je Python 3 nainstalován?"
        read -rp "Stiskněte Enter pro ukončení..."
        exit 1
    fi
    .venv/bin/pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "CHYBA: Instalace závislostí selhala."
        read -rp "Stiskněte Enter pro ukončení..."
        exit 1
    fi
    echo
    echo "Nastavení dokončeno!"
    echo
fi

.venv/bin/python watcher.py
echo
read -rp "Program byl ukončen. Stiskněte Enter pro zavření okna..."
