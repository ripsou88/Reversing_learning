from z3 import *

def simulate_fun(original_chars, param_2):
    local_10 = BitVecVal(0, 32)
    static_value_result = [BitVec(f'static_value_{i}', 8) for i in range(param_2)]

    for i in range(0, param_2 - 1, 2):
        c0 = ZeroExt(24, original_chars[i])
        c1 = ZeroExt(24, original_chars[i + 1])

        local_10 = local_10 * 0x21 ^ (c1 * 0x1fd) ^ (c0 * 0x101)

        static_value_result[i] = Extract(7, 0, local_10)
        static_value_result[i + 1] = Extract(15, 8, local_10)

    if param_2 % 2 == 1:
        last_idx = param_2 - 1
        c = original_chars[last_idx]
        static_value_result[last_idx] = (Extract(7, 0, local_10 * 0x21)) ^ c

    return static_value_result

def reverse_fun_from_static_value(static_value):
    param_2 = len(static_value)
    s = Solver()

    original_chars = [BitVec(f'c{i}', 8) for i in range(param_2)]

    # only printable char
    for c in original_chars:
        s.add(c >= 0x20, c <= 0x7e)

    # simulate function
    simulated = simulate_fun(original_chars, param_2)

    # compare to real value
    for i in range(param_2):
        s.add(simulated[i] == static_value[i])

    if s.check() == sat:
        m = s.model()
        result = [m.evaluate(c).as_long() for c in original_chars]
        return bytes(result)
    else:
        return None

# compared value
static_value = [0x9c, 0x85, 0xb5, 0x8d, 0x12, 0xa0, 0x9b, 0x10, 0xe8, 0x1f, 0x2b, 0xb3, 0xdb, 0x4a, 0x87, 0x1e,
           0x39, 0xbd, 0x03, 0x32, 0xc6, 0xd0, 0x82, 0xdb, 0xcd, 0x46, 0x82, 0xa1, 0x6d, 0x09, 0x80,
           0xe5, 0x6c, 0x7f, 0x6c, 0x82, 0x91]

res = reverse_fun_from_static_value(static_value)
if res:
    print("flag found :", res.decode())
else:
    print("No solution found.")
