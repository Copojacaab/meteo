# probe_pdw.py: script usa e getta, non entra nel progetto

from pwdlib import PasswordHash

pwd = PasswordHash.recommended()

# (1) Firma delle funzioni
import inspect
print("=== firma hash === ", inspect.signature(pwd.hash))
print("=== firma verify === ", inspect.signature(pwd.verify))

# (2) Hashing di una password
raw = "pass123"
hashed  = pwd.hash(raw)
print("hash -> ", hashed)
print("lunghezza -> ", len(hashed))

# (3) Verifica
print("corretta -> ", pwd.verify(raw, hashed))
print("sbagliata -> ", pwd.verify("pass012", hashed))
