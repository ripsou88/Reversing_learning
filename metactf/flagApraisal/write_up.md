# MetaCTF - Flag Appraisal 
Let's start by reversing the binary with ghidra.
Here's the main function in pseudo C code.
```C
bool FUN_0010128e(void)

{
  int iVar1;
  size_t sVar2;
  long in_FS_OFFSET;
  char local_78 [104];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  printf("Welcome to my Pawn Shop, go ahead and show me the flag you want appraised: ");
  fgets(local_78,100,stdin);
  sVar2 = strcspn(local_78,"\n");
  local_78[sVar2] = '\0';
  sVar2 = strlen(local_78);
  FUN_00101199(local_78,sVar2 & 0xffffffff);
  iVar1 = strncmp(local_78,&DAT_00102058,0x25);
  if (iVar1 != 0) {
    puts("Unfortunately, your flag here looks to be a counterfeit.");
  }
  else {
    puts("Well good news, your flag looks to be authentic! Best I can do is $2.");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return iVar1 != 0;
}
```

The checker uses fgets to obtain the user input (so the user input is retrieved from stdin).

We can see that Strcmp compares 37 bytes with a static value.


Next analyse the function.
```C
void FUN_00101199(long param_1,uint param_2)

{
  undefined4 local_10;
  undefined4 local_c;
  
  local_10 = 0;
  for (local_c = 0; local_c < (int)(param_2 - 1); local_c = local_c + 2) {
    local_10 = local_10 * 0x21 ^
               *(char *)(param_1 + (long)local_c + 1) * 0x1fd ^ *(char *)(param_1 + local_c) * 0x101
    ;
    *(char *)(param_1 + local_c) = (char)local_10;
    *(char *)(param_1 + (long)local_c + 1) = (char)(local_10 >> 8);
  }
  if ((param_2 & 1) != 0) {
    *(byte *)(param_1 + (long)(int)param_2 + -1) =
         (char)local_10 * '!' ^ *(byte *)(param_1 + (long)(int)param_2 + -1);
  }
  return;
}
```

This modifies the user input before comparison.

So I see three approaches to solve the checker:
- Perform symbolic execution using angr. *solution1.py*
- Reverse the hashing function (this is the solution originally proposed by Meta). *solution2.py*
- Use the Z3 solver to resolve the constraints and recover the flag. *solution3.py*

You can find all these solution scripts in the current directory.
