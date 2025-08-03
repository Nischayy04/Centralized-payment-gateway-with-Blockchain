from Crypto.PublicKey import RSA

def generate_and_save(name):
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open(f"{name}_private.pem", "wb") as f:
        f.write(private_key)
    with open(f"{name}_public.pem", "wb") as f:
        f.write(public_key)
    print(f"Keys generated for {name}")

if __name__ == "__main__":
    generate_and_save("user")
    generate_and_save("upi")
    generate_and_save("bank")
