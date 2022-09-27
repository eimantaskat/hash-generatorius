# Hash generatorius

## Atsisiuntimas ir build'inimas
   ```console
   > git clone https://github.com/eimantaskat/hash-generatorius.git
   > cd hash-generatorius
   > make
   ```

## Naudojimas
* Naudojant command line argumentus
   ```console
   > ./hash [Flag] <args>

   Flag'ai:
      --file arba -f: hash'inti visą failą
      --lines arba -l: atskirai hash'initi kiekvieną failo eitutę

   Args:
      Failai, kuriuos norite suhash'inti

   Pvz.:
   > ./hash -f t1.txt t2.txt ... tn.txt

   Output'as:
      <input>: <hash>
   ```
* Įvedant inputą ranka
   ```console
    > ./hash
    Iveskite teksta: <input>
    <output>
  ```

## Testavimo script'o naudojimas
   ```console
   > make test-run
   ```
   Bus sugeneruoti testavimo failai ir ištestuota hash funkcija. Rezultatai atspausdinami į komandinę eilutę

# Hash funkcijos pseudo-kodas
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
# Hash funkcijos analizė