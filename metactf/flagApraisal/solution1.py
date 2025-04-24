import angr
import claripy

project = angr.Project("pawn_shop", auto_load_libs=False)

flag_len = 37 
flag_chars = [claripy.BVS(f'flag_{i}', 8) for i in range(flag_len)]
# Include null terminator if binary expects C-style strings
flag = claripy.Concat(*flag_chars + [claripy.BVV(0, 8)])

simfile = angr.storage.file.SimFileStream(name='stdin', content=flag, has_end=False)

# Simple entry state with stdin
state = project.factory.entry_state(stdin=simfile)

# Only alow printable char
for c in flag_chars:
    state.solver.add(c >= 0x20)
    state.solver.add(c <= 0x7e)

state.options.add(angr.options.ZERO_FILL_UNCONSTRAINED_MEMORY)
state.options.add(angr.options.ZERO_FILL_UNCONSTRAINED_REGISTERS)

simgr = project.factory.simgr(state)
simgr.use_technique(angr.exploration_techniques.Veritesting())

target_addr = 0x401335  #addr of the success : 
avoid_addr = 0x40134b   # addr of the fail : Unfortunately....

simgr.explore(find=target_addr, avoid=avoid_addr)

if simgr.found:
    found = simgr.found[0]
    solution = found.solver.eval(flag, cast_to=bytes)
    print("[+] Input found :", solution)
    print("[+] Decoded :", solution.decode('utf-8', errors='ignore'))
else:
    print("[-] No path found :(")
