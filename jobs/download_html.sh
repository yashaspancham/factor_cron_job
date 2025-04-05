cd src/

mprof run python3 ./src/download.py

cd ..

mprof plot -o ./logs/memory_usage.png