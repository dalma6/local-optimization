# Local optimization 

Local optimizator for 3-adress code that is in SSA format. Optimizator supports neutral elimination, constant folding, constant propagation and strenght reduction and runs those optimizations in a loop as long as there is something to optimize.

### :book: Code description:
Local optimizator works for 3-address code that has the following syntax:
1. The language consists of declarations and IF / GOTO statements ( GOTO must go to some number ).
2. Code must be in SSA (Single Static Assigment) format ( 1 declaration per variable )
2. Operators that are supported : 

      | + | - | * | / | >> | << |- (unary)|
      |---|---|---|---|----|----|---------|

 ```
x1 := 7
IF x1 < 5 GOTO 5
y := x1 * 8
x2 := y ^ 2
x3 := x2 + x2
z := 2 + 3
t := -x1 * 2
```

### :joystick: Usage
Run the following command 
```
$ python3 blockCreator.py [path_to_file]
```

If path to file is not stated program uses test/test_examples/test.txt file that consists of instructions
that demonstrate how each local optimization technique works and how they work together in a loop.

# :computer: Optimization techniques
Local optimizator optimizes the code described above using the following steps 
### 1. Basic block generator
Optimizator splits the code into basic blocks by finding _leader instructions_
```
x1 := 7
IF x1 < 5 GOTO 5
--------------
y := x1 * 8
x2 := y ^ 2
--------------
x3 := x2 + x2
z := 2 + 3
t := -x1 * 2
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
z := 1 ^ 5          => z := 
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

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details
