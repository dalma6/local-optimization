# Local optimization 

Local optimizator for 3-adress code.

### :exclamation: TODO: 
* srediti kod
* brojevi skokova - treba ih azuriati 
* treba azurirati i cele blokove - jer se broj instrukcija menja i neke nestaju, neke se dodaju (nije obavezno , i sad radi super ) 

### :book: Code description:
Local optimizator works for 3-address code that has the following syntax:
1. The language consists of declarations and IF / GOTO statements
2. Operators that are supported : 

      | + | - | * | / | >> | << |- (unary)|
      |---|---|---|---|----|----|---------|

 ```
x := 7
IF x < 5 GOTO 5
y := x * 8
x := y ^ 2
x := x + x
z := 2 + 3
t := -x * 2
```

# :computer: Optimization techniques
Local optimizator optimizes the code described above using the following steps 
### 1. Basic block generator
Optimizator splits the code into basic blocks by finding _leader instructions_
```
x := 7
IF x < 5 GOTO 5
--------------
y := x * 8
x := y ^ 2
--------------
x := x + x
z := 2 + 3
t := -x * 2
```
### 2. Neutral elimination
Optimizator performs neutral elimination technique on each block
```
z := x + 0          => z := x
z := 0 + x          => z := x

y := y - 0          => y := y
y := 0 - y          => y := -y
z := 0 - (- z)      => z := z

t := t * 0          => t := 0
t := 0 * t          => t := 0

f := f * 1          => f := f
f := 1 * f          => f := f

z := 0 / y          => z := 0
t := t / 1          => t := t

z := z ^ 0          => z := 1
z := z ^ 1          => z := z
z := 1 ^ 5          => z := 1

````
###  3. Constant folding
Optimizator performs constant folding technique on each instruction after neutral elimination
```
IF 3 < 2 GOTO 0       =>                    (deleted instruction)
x := 2 + 3            => x := 5
x := 2 * 3            => x := 6
x := 6 / 3            => x := 2
x := 2 ^ 3            => x := 8
x := 2 - 3            => x := -1
IF 4 < 5 GOTO 1       => GOTO 1             ( conditionl jump => non conditional jump ) 
```

### 4. Strenght reduction
Optimizator performs strenght reduction technique on each instruction after constant folding and neutral elimination
```
y := y ^ 2            => y := y * y
t := y * 2            => y := y + y
t := 2 * (-t)         => t := -t + -t

g := x * 16           => g << 4
g := x * 32           => g << 5

g := 7 * z            => tmp_g := z << 3
                         g := tmp_g - z     

f := f * 33           => tmp_f := f << 5
                         f := tmp_f + f
```
### 5. Constant propagation 
Optimizator performs constant propagation technique on each block 
```
x := 3                
z := z + x            =>    z := z + 3
x := 5
y := x + z            =>    y := 5 + z

```
### :repeat: REPEAT 
These optimizations are runnning in a loop until there is nothing more to optimize


## :wrench: Built Using
* [PLY - Python Lex-Yacc](https://github.com/dabeaz/ply)

## :mortar_board: Authors

* **Dalma Beara** - [dalma6](https://github.com/dalma6/)
* **Nikola Dimić** -  [dimaria95](https://github.com/dimaria95/)

## :book: License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
