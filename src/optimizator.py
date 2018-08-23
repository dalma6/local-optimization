# ALGEBRAIC TRANSFORMATIONS

# TODO: STEP1:
# elimination of arithmetic operations that contain the neutral element
# x := x + 0
# x := x * 1

# TODO: STEP2:
# strength reduction
# x := x * 0 x := 0
# y := y ^ 2 y := y * y
# y := 2 * x y := x + x
# x := x * 8 x := x << 3
# x := x * 15 t := x << 4; x := t - x;

# TODO: STEP3:
# constant folding
# x := 2 + 2 x := 4
# if 0 < 2 then goto L goto L
#if 2 < 0 then goto L /* can be deleted */


# ELIMINATION OF MUTUAL SUBEXPRESSIONS

# TODO: STEP1:
# redction of redundat calculations
# a := b + c		a := b + c
# b := a - d        d := a - d
# c := b + c		c := d + c
# d := a - d

# DEAD CODE ELIMINATION
# TODO: liveness analysis algorithm

# CONSTANT PROPAGATION

# COPY PROPAGATION

# COMPOSITION OF LOCAL OPTIMIZATION METHODS