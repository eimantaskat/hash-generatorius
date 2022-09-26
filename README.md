# Hash generatorius

sha256 - http://www.zedwood.com/article/cpp-sha256-function

--- Output'ų dydžio, to paties failo hash'o testavimas ---
Pirmas hash'avimas                                               Antras hash'avimas
Inputa'ai - failai su vienu simboliu:
49517325a2e305749bb9cbafba592d11054653207b91bc5a3b1d7a546ce36255 49217325a29305749bb9cbafba59271105365320dbbda65a3b1d7a546ce36255
ad344189b70020331c01efd63798889c2ed64668c53974279a4fad1c70786215 ad444189b77020331c01efd619b2129c2ea64668c54974279a4fad1c70786215

Inputa'ai - failai su 10 000 atsitiktinių simbolių:
f133228f10b3b0fda8bb2eeb65409da01c7e78e6ee186f2d226d4171b327aa5f f133228f10b3b0fda8bb2eebb0f618a01c7e78e6ee186f2d226d4171b327aa5f
e3f5f4f3fdaa877c2dd26ed7af9315ca1cbeb7c18caeea277bb2d5841f096503 e3f5f4f3fdaa877c2dd26ed7fc4950ca1cbeb7c18caeea277bb2d5841f096503

Inputa'ai - 10 000 simbolių failai, kurie skiriasi nuo pirmo failo vienu simboliu:
a99fd507d9789aaa5b5b0d128ac03374b98155743c0c091556c35640238776cb a99fd507d9789aaa5b5b0d1212168174b98155743c0c091556c35640238776cb
b2a0ea2c4c865d89a88d3ef09ad764655b70377730963c46f91a4b674f927809 b2a0ea2c4c865d89a88d3ef0020f52655b70377730963c46f91a4b674f927809

Inputa'ai - tušti failai:
8924948469167450646733879654151105463244673378311219286381674232 8924948469167450646733879654151105463244673378311219286381674232
8924948469167450646733879654151105463244673378311219286381674232 8924948469167450646733879654151105463244673378311219286381674232

--- Hash funkcijos efektyvumo testavimas: kostitucijos eilučių hash'avimas ---
Hashed 1 strings (72082 symbols) in 0.00651s
Average hash time: 0.00651s
Max hash time: 0.00651s
Min hash time: 0.00651s
Average input length: 72082.00000
Average hash length: 64.0
Collisions: 0

--- Atsparumo kolizijai testavimas: 25 000 porų po 10, 100, 500 ir 1 000 atsitiktinių simbolių hash'inimas ---
Hashed 200000 strings (80500000 symbols) in 16.99320s
Average hash time: 0.00008s
Max hash time: 0.00150s
Min hash time: 0.00000s
Average input length: 402.50000
Average hash length: 64.0
Number of collisions: 0

--- Lavinos efekto testavimas: 25 000 porų (poros simbolių eilutės skiriasi 1 simboliu), po 10, 100, 500 ir 1 000 atsitiktinių simbolių hash'inimas ---
Hashed 200000 strings (80500000 symbols) in 17.01487s
Average hash time: 0.00009s
Max hash time: 0.00300s
Min hash time: 0.00000s
Average input length: 402.50000
Average hash length: 64.0

Average hex simillarity: 4.82102%
Min hex simillarity: 0.00%
Max hex simillarity: 96.88%

Average bits simillarity: 26.43170%
Min bits simillarity: 37.50%
Max bits simillarity: 98.05%


# SHA256
--- Output'ų dydžio, to paties failo hash'o testavimas ---
Pirmas hash'avimas                                               Antras hash'avimas
Inputa'ai - failai su vienu simboliu:
594e519ae499312b29433b7dd8a97ff068defcba9755b6d5d00e84c524d67b06 594e519ae499312b29433b7dd8a97ff068defcba9755b6d5d00e84c524d67b06
d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35 d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Inputa'ai - failai su 10 000 atsitiktinių simbolių:
9c5f9ced10c5d9b1591de70a3ab26e3e77604e54779f5ae04b6faa9d71a14050 9c5f9ced10c5d9b1591de70a3ab26e3e77604e54779f5ae04b6faa9d71a14050
9fefe0e7c319de02eb821a6be369b690751897855418c94035f9b08d397fbae8 9fefe0e7c319de02eb821a6be369b690751897855418c94035f9b08d397fbae8

Inputa'ai - 10 000 simbolių failai, kurie skiriasi nuo pirmo failo vienu simboliu:
48902dd49e5653eddb78ea79762d0166c24194b61d2cf52e60edd1f7eb968d8a 48902dd49e5653eddb78ea79762d0166c24194b61d2cf52e60edd1f7eb968d8a
46fd5e8978d3f6d39633d0d9b13fc835844375b149733fbb768a90762e1ddced 46fd5e8978d3f6d39633d0d9b13fc835844375b149733fbb768a90762e1ddced

Inputa'ai - tušti failai:
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

--- Hash funkcijos efektyvumo testavimas: kostitucijos eilučių hash'avimas ---
Hashed 1 strings (72082 symbols) in 0.00100s
Average hash time: 0.00100s
Max hash time: 0.00100s
Min hash time: 0.00100s
Average input length: 72082.00000
Average hash length: 64.0
Collisions: 0

--- Atsparumo kolizijai testavimas: 25 000 porų po 10, 100, 500 ir 1 000 atsitiktinių simbolių hash'inimas ---
Hashed 200000 strings (80500000 symbols) in 1.68168s
Average hash time: 0.00001s
Max hash time: 0.00056s
Min hash time: 0.00000s
Average input length: 402.50000
Average hash length: 64.0
Number of collisions: 0

--- Lavinos efekto testavimas: 25 000 porų (poros simbolių eilutės skiriasi 1 simboliu), po 10, 100, 500 ir 1 000 atsitiktinių simbolių hash'inimas ---
Hashed 200000 strings (80500000 symbols) in 1.68715s
Average hash time: 0.00001s
Max hash time: 0.00055s
Min hash time: 0.00000s
Average input length: 402.50000
Average hash length: 64.0

Average hex simillarity: 3.11867%
Min hex simillarity: 0.00%
Max hex simillarity: 21.88%

Average bits simillarity: 24.99955%
Min bits simillarity: 37.11%
Max bits simillarity: 63.67%