main:
	g++ -o hash src/hash.cpp src/main.cpp -O3
test:
	g++ -o hash-test src/hash.cpp src/test.cpp -O3
test-run: test
	python testing/testing.py