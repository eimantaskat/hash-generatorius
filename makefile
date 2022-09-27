main:
	g++ -o main src/*.cpp -O3
test: main
	python testing/testing.py