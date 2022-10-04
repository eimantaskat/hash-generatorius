# Hash generatorius

### Atsisiuntimas ir build'inimas
   ```console
   > git clone https://github.com/eimantaskat/hash-generatorius.git
   > cd hash-generatorius
   > make
   ```

### Naudojimas
* Naudojant command line argumentus
   ```console
   > ./hash [Flag] <args>

   Flag'ai:
      --file arba -f: hash'inti visą failą
      --lines arba -l: atskirai hash'initi kiekvieną failo eitutę
      --salt: pateikti salt'ą
      -s: (naudojant kartu su -f arba -l) hashinti naudojant programos sugeneruotą salt'ą
      -s: (įvedant duomenis ranka) prieš hash'inant kiekvieną input'ą programa paprašys įvesti salt'ą

   Args:
      Failai, kuriuos norite suhash'inti

   Pvz.:
   > ./hash -f t1.txt t2.txt ... tn.txt --salt="12345"

   Output'as:
      <input>: <hash>
   ```
* Įvedant inputą ranka
   ```console
    > ./hash
    Iveskite teksta: <input>
    <hash>
  ```

### Testavimo script'o naudojimas
   ```console
   > make test-run
   ```
   Bus sugeneruoti testavimo failai ir ištestuota hash funkcija. Rezultatai atspausdinami į komandinę eilutę

## Hash funkcijos pseudo-kodas
```c++
   Hash(string):
      v = toCharVector(string)

      asciiVal = 0
      for i = 0 to v.size()
         asciiVal += i ^ v[i]

      hex = toHex(string)
      hexVal = 0
      for i = 0 to hex.length()
         hexVal += i << hex[i]

      seed = (v.size() << asciiVal) ^ asciiVal
      seed += toDecimal(compress(v, 4)) + hexVal

      random.seed(seed)
      key = ""
      for i = 0 to 64
         key += toHex(random.randint(0, 255))

      hash = toCharVector(key) + v

      return compress(hash, 64)
```
```c++
   compress(charVector, outputLen):
      size = charVector.size()

      while size > length
         last = charVector.back()
         index = size % outputLen

         charVector[index] += last

         size--
      
      charVector.resize(size)

      output = ""
      for char in charVector
         output += toHex(char)

      return output
```
## Hash funkcijos analizė

### Output'ų dydžio, to paties failo hash'avimo testavimas
Nepriklausomai nuo input'o, output'ai visada vienodo dydžio, o antrą kartą suhash'avus tą patį failą gaunamas toks pats hash'as

#### Testavimo script'o output'as:
```console
   Pirmas hash'avimas                                               Antras hash'avimas
   Inputa'ai - failai su vienu simboliu:
   2362746f74f3467f1775182553265f850f137423075404733740635316202247 2362746f74f3467f1775182553265f850f137423075404733740635316202247
   2d0e1ffbe1aed0fdfcc20dfd1c202d1e00dbdadd22ae1feddd21cd0ac1f58566 2d0e1ffbe1aed0fdfcc20dfd1c202d1e00dbdadd22ae1feddd21cd0ac1f58566

   Inputa'ai - failai su 10 000 atsitiktinių simbolių:
   1451f65e1c0c3e71eff23d2e0e33212e2222e1d50523111104d3e263d62416f2 1451f65e1c0c3e71eff23d2e0e33212e2222e1d50523111104d3e263d62416f2
   1768aa5c474becf000ce1ec10d1fb009c9d1eeee1b00fd1eed2dfc1cfef102e0 1768aa5c474becf000ce1ec10d1fb009c9d1eeee1b00fd1eed2dfc1cfef102e0

   Inputa'ai - 10 000 simbolių failai, kurie skiriasi nuo pirmo failo vienu simboliu:
   403715d8eb8c71a114754585eb217d1dbee7e0ce6e55ad2b3ae7bb0a8edce24d 403715d8eb8c71a114754585eb217d1dbee7e0ce6e55ad2b3ae7bb0a8edce24d
   a38da570ffc3cee3a2e2e7c104939a11b2d181a968d15014713a7ac9e4229295 a38da570ffc3cee3a2e2e7c104939a11b2d181a968d15014713a7ac9e4229295

   Inputa'ai - tušti failai:
   922a51b9e63ca52339d21063c2e6f6dab0520decaa466610301b42da2cac2643 922a51b9e63ca52339d21063c2e6f6dab0520decaa466610301b42da2cac2643
   922a51b9e63ca52339d21063c2e6f6dab0520decaa466610301b42da2cac2643 922a51b9e63ca52339d21063c2e6f6dab0520decaa466610301b42da2cac2643
```


### Hash funkcijos efektyvumo testavimas: kostitucijos eilučių hash'avimas
Hash funkcija veikia pakankamai efektyviai, Lietuvos Konstitucijos hash'inimas užtrunka apie 4ms. Hash funkcijos laiko nuo inputo dydžio prikausimybė yra tiesinė O(n)

#### Testavimo script'o output'as:
```console
   20 hash'avimų vidurkis:
   1 eilutės: 0.00010s
   2 eilutės: 0.00003s
   4 eilutės: 0.00008s
   8 eilutės: 0.00010s
   16 eilutės: 0.00007s
   32 eilutės: 0.00015s
   64 eilutės: 0.00035s
   128 eilutės: 0.00047s
   256 eilutės: 0.00102s
   512 eilutės: 0.00232s
   789 eilutės: 0.00368s
```  
![image](https://user-images.githubusercontent.com/80033246/192839927-b912f03b-d12e-4301-8fb2-e6d4096d3437.png)

### Atsparumo kolizijai testavimas: 25 000 porų po 10, 100, 500 ir 1 000 atsitiktinių simbolių hash'inimas
Suhash'inus 25 000 porų po 10, 100, 500 ir 1 000 atsitiktinių simbolių, nesutapo jokių porų hash'ai, taigi hash funkcija yra pakankamai atspari kolizijai
#### Testavimo script'o output'as:
```console
Suhash'inta 200000 simbolių eillučių (80500000 simbolių) per 9.57400s
Vidutinis hash'avimo laikas: 0.00005s
Didžiausias hash'avimo laikas: 0.01150s
Mažiausias hash'avimo laikas: 0.00000s
Vidutinis input'o ilgis: 402.50000
Vidutinis hash'o ilgis: 64.0
Kolizijos: 0
```

### Lavinos efekto testavimas: 25 000 porų (poros simbolių eilutės skiriasi 1 simboliu), po 10, 100, 500 ir 1 000 atsitiktinių simbolių hash'inimas 
Suhash'inus 25 000 porų po 10, 100, 500 ir 1 000 simbolių, kurios skiriasi tik vienu simboliu, vidutinis hex'ų panašumas ~10%, o maksimalus hex'ų panašumas ~31%, vidutinis bit'ų panašumas ~53%, o maksimalus bit'ų panašumas ~70%, taigi, hash funkcija atitinka lavinos efektą

#### Testavimo script'o output'as:
```console
Suhash'inta 200000 simbolių eillučių (80500000 simbolių) per 9.42922s
Vidutinis hash'avimo laikas: 0.00005s
Didžiausias hash'avimo laikas: 0.00150s
Mažiausias hash'avimo laikas: 0.00000s
Vidutinis input'o ilgis: 402.50000
Vidutinis hash'o ilgis: 64.0

Vidutinis hex'ų panašumas: 10.1554%
Mažiausias hex'ų panašumas: 0.00%
Didžiausias hex'ų panašumas: 31.25%

Vidutinis bitų panašumas: 53.2185%
Mažiausias bitų panašumas: 35.55%
Didžiausias bitų panašumas: 69.53%
```

### Apibendrinimas
Pagal mano atliktą testavimą, hash funkcija atitinka visus reikalavimus. Man nepavyko rasti nei vienos kolizijos ir pakeitus vieną simbolį hash'ai smarkiai skiriasi, tačiau ši hash funkcija nėra labai efektyvi.

## Mano hash funkcijos palyginimas su MD5, SHA-256 ir SHA-1
Palyginimamas buvo naudojamos šios hash funkcijų realizacijos: [MD5](http://www.zedwood.com/article/cpp-md5-function), [SHA-256](http://www.zedwood.com/article/cpp-sha256-function), [SHA-1](http://www.zedwood.com/article/cpp-sha1-function)

### Efektyvumo palyginimas
Funkcijų efektyvumui palyginti pakartojau konstitucijos hash'avimo testą. Kaip matome, mano funkcija yra daug lėtesnė už kitas lyginamas funkcijas. Pati greičiausia yra MD5 funkcija, tačiau jos output'as yra tik 128 bitų dydžio. Antroje vietoje yra SHA-1 funkcija, jos output'as yra 160 bitų dydžio. Trečioje vietoje liko SHA-256 funkcija.
![image](https://user-images.githubusercontent.com/80033246/193121377-f857c7a0-7ea8-4604-8e5e-32ec83f0645a.png)

|   | Hash | MD5 | SHA-256 | SHA-1 |
|---|---|---|---|---|
| 1 | 0.00005 | 0.00 | 0.00 | 0.00002 |
| 2 | 0.0001 | 0.00003 | 0.00 | 0.00003 |
| 4 | 0.00008 | 0.00002 | 0.00 | 0.00003 |
| 8 | 0.0001 | 0.00005 | 0.00 | .000 |
| 16 | 0.0001 | 0.00003 | 0.00003 | .000 |
| 32 | 0.0002 | 0.00002 | 0.00 | 0.00005 |
| 64 | 0.00022 | 0.00 | 0.00005 | 0.00002 |
| 128 | 0.00053 | 0.00002 | 0.0001 | 0.0001 |
| 256 | 0.00092 | 0.00008 | 0.0001 | 0.00015 |
| 512 | 0.0022 | 0.00008 | 0.0003 | 0.00017 |
| 789 | 0.0034 | 0.0002 | 0.00038 | 0.00025 |


### Lavinos efekto palyginimas
Lavinos efekto palyginimui hash'inau 25 000 porų po 10, 100, 500 ir 1 000 simbolių, kurios skiriasi tik vienu simboliu. Pagal vidutinį hex'ų panašumą, mano funkcija liko paskutinėje vietoje, tačiau pagal vidutinį bitų panašumą užėmė 2-ąją vietą po SHA-256 funkcijos ir 1-ąją vietą pagal mažiausią bitų panašumą. Geriausią maksimalų hex'ų panašumą turi SHA-256 funkcija (trečdaliu mažesnis, nei kitų funkcijų), kitų lyginamų funkcijų rezultatai labai panašūs, apie 32%.

![image](https://user-images.githubusercontent.com/80033246/193892635-e68e314d-e6db-4de6-9aff-ac616e2510b1.png)


|   | Hex, avg | Hex, min | Hex, max | Bits, avg | Bits, min | Bits, max |
|---|---|---|---|---|---|---|
| Hash | 10.14256 | 0 | 31.25 | 53.21376 | 33.98 | 70.7 |
| MD5 | 6.24974 | 0 | 31.25 | 74.99832 | 66.02 | 84.77 |
| SHA-256 | 6.27668 | 0 | 21.88 | 50.00852 | 36.72 | 62.5 |
| SHA-1 | 6.24938 | 0 | 32.5 | 68.7553 | 59.38 | 80.86 |