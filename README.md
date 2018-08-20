# Local optimization 

Local optimizator for 3-adress code.

## :muscle: Example: 
This example ilustrates how the local optimizator should work
```
x := x * 0 
y := y ^ 2 
y := 2 * x 
x := x * 8 
x := x * 15
```
is converted into following code:

```
x := 0
y := y * y
y := x + x
x := x << 3
t := x << 4; x := t - x;
```

## :wrench: Built Using
* [PLY - Python Lex-Yacc](https://github.com/dabeaz/ply)

## :mortar_board: Authors

* **Dalma Beara** - [dalma6](https://github.com/dalma6/)
* **Nikola Dimić** -  [dimaria95](https://github.com/dimaria95/)

## :book: License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
