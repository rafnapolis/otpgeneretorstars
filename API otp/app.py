from fastapi import FastAPI, HTTPException
import pyotp

app = FastAPI()

# Generar una clave secreta para el usuario
def generate_secret():
    return pyotp.random_base32()

# Generar un código OTP basado en la clave secreta
def generate_otp(secret):
    totp = pyotp.TOTP(secret)
    return totp.now()

# Verificar si el código OTP proporcionado es válido
def verify_otp(secret, otp):
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)

# Ruta para generar una nueva clave secreta para un usuario
@app.get("/generate_secret/{user_id}")
async def generate_secret_for_user(user_id: str):
    secret = generate_secret()
    return {"user_id": user_id, "secret": secret}

# Ruta para generar un código OTP para un usuario dado su clave secreta
@app.get("/generate_otp/{user_id}/{secret}")
async def generate_otp_for_user(user_id: str, secret: str):
    otp = generate_otp(secret)
    return {"user_id": user_id, "otp": otp}

# Ruta para verificar un código OTP dado un usuario y su clave secreta
@app.get("/verify_otp/{user_id}/{secret}/{otp}")
async def verify_otp_for_user(user_id: str, secret: str, otp: str):
    is_valid = verify_otp(secret, otp)
    if is_valid:
        return {"user_id": user_id, "otp_verification": "valid"}
    else:
        raise HTTPException(status_code=400, detail="Invalid OTP")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
