# Local optimization 

Local optimizator for 3-adress code.

### :smile: TODO: 
* promeniti gramatiku tako da prihvata i IF 1 GOTO 12 , to sam zaboravio 
* izmeniti program tako da ovo radi tj da sve optimizacije rade kako valja
* uraditi strenght reduction [ ovo je bas malo ostalo, to mogu i ja zavrsiti ] 
* uraditi constant propagation
* uraditi redundatne kalkulacije


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
