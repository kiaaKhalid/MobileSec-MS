from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
from androguard.core.apk import APK
import numpy as np
import os
import shutil

app = FastAPI(title="MobileSec AI Scanner")

# Autorise le frontend à accéder à l'API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pour plus de sécurité, tu peux mettre ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint healthcheck pour Docker
@app.get("/health")
def health():
    return {"status": "ok"}

# --- CONFIGURATION ---
MODEL_PATH = "mobilesec_model_v3.h5"

# Liste EXACTE des permissions utilisée lors de l'entraînement (copiez-collez la liste complète ici)
ALL_PERMISSIONS = [
    "android.permission.INTERNET", "android.permission.ACCESS_NETWORK_STATE",
    "android.permission.ACCESS_WIFI_STATE", "android.permission.CHANGE_WIFI_STATE",
    "android.permission.CHANGE_NETWORK_STATE", "android.permission.BLUETOOTH",
    "android.permission.BLUETOOTH_ADMIN", "android.permission.BLUETOOTH_PRIVILEGED",
    "android.permission.NFC", "android.permission.USE_SIP", "android.permission.VOIP",
    "android.permission.READ_SMS", "android.permission.SEND_SMS",
    "android.permission.RECEIVE_SMS", "android.permission.RECEIVE_MMS",
    "android.permission.RECEIVE_WAP_PUSH", "android.permission.WRITE_SMS",
    "android.permission.READ_PHONE_STATE", "android.permission.CALL_PHONE",
    "android.permission.PROCESS_OUTGOING_CALLS", "android.permission.READ_CALL_LOG",
    "android.permission.WRITE_CALL_LOG", "android.permission.ADD_VOICEMAIL",
    "android.permission.USE_USSD", "android.permission.MODIFY_PHONE_STATE",
    "android.permission.ACCESS_FINE_LOCATION", "android.permission.ACCESS_COARSE_LOCATION",
    "android.permission.ACCESS_BACKGROUND_LOCATION", "android.permission.ACCESS_MOCK_LOCATION",
    "android.permission.ACCESS_LOCATION_EXTRA_COMMANDS",
    "android.permission.READ_EXTERNAL_STORAGE", "android.permission.WRITE_EXTERNAL_STORAGE",
    "android.permission.MOUNT_UNMOUNT_FILESYSTEMS", "android.permission.MANAGE_DOCUMENTS",
    "android.permission.CAMERA", "android.permission.RECORD_AUDIO",
    "android.permission.CAPTURE_AUDIO_OUTPUT", "android.permission.CAPTURE_VIDEO_OUTPUT",
    "android.permission.BODY_SENSORS", "android.permission.USE_FINGERPRINT",
    "android.permission.VIBRATE", "android.permission.FLASHLIGHT",
    "android.permission.RECEIVE_BOOT_COMPLETED", "android.permission.WAKE_LOCK",
    "android.permission.SYSTEM_ALERT_WINDOW", "android.permission.KILL_BACKGROUND_PROCESSES",
    "android.permission.RESTART_PACKAGES", "android.permission.GET_TASKS",
    "android.permission.REORDER_TASKS", "android.permission.EXPAND_STATUS_BAR",
    "android.permission.DISABLE_KEYGUARD", "android.permission.READ_SYNC_SETTINGS",
    "android.permission.WRITE_SYNC_SETTINGS", "android.permission.READ_SYNC_STATS",
    "android.permission.PERSISTENT_ACTIVITY",
    "android.permission.INSTALL_PACKAGES", "android.permission.REQUEST_INSTALL_PACKAGES",
    "android.permission.DELETE_PACKAGES", "android.permission.CLEAR_APP_CACHE",
    "android.permission.DELETE_CACHE", "android.permission.INSTALL_SHORTCUT",
    "android.permission.UNINSTALL_SHORTCUT",
    "android.permission.GET_ACCOUNTS", "android.permission.AUTHENTICATE_ACCOUNTS",
    "android.permission.MANAGE_ACCOUNTS", "android.permission.USE_CREDENTIALS",
    "android.permission.ACCOUNT_MANAGER", "android.permission.BIND_DEVICE_ADMIN",
    "android.permission.READ_CONTACTS", "android.permission.WRITE_CONTACTS",
    "android.permission.READ_CALENDAR", "android.permission.WRITE_CALENDAR",
    "android.permission.READ_PROFILE", "android.permission.WRITE_PROFILE",
    "android.permission.READ_SOCIAL_STREAM", "android.permission.WRITE_SOCIAL_STREAM",
    "android.permission.READ_USER_DICTIONARY", "android.permission.WRITE_USER_DICTIONARY",
    "android.permission.WRITE_SETTINGS", "android.permission.WRITE_SECURE_SETTINGS",
    "android.permission.SET_WALLPAPER", "android.permission.SET_TIME_ZONE",
    "com.android.browser.permission.READ_HISTORY_BOOKMARKS",
    "com.android.browser.permission.WRITE_HISTORY_BOOKMARKS",
    "com.android.vending.BILLING", "com.android.vending.CHECK_LICENSE",
    "com.google.android.c2dm.permission.RECEIVE",
    "com.google.android.gms.permission.ACTIVITY_RECOGNITION"
]

# Chargement global du modèle au démarrage
print("Loading AI Model...")
model = tf.keras.models.load_model(MODEL_PATH)
print("AI Model Loaded!")

def extract_vector(apk_path):
    try:
        a = APK(apk_path)
        perms = a.get_permissions()
        vec = np.zeros((1, len(ALL_PERMISSIONS)))
        detected_perms = []
        for p in perms:
            if p in ALL_PERMISSIONS:
                vec[0, ALL_PERMISSIONS.index(p)] = 1
                detected_perms.append(p)
        return vec, detected_perms
    except Exception as e:
        print(f"Error parsing APK: {e}")
        return None, []

@app.post("/scan")
async def scan_apk(file: UploadFile = File(...)):
    filename = f"temp_{file.filename}"
    with open(filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        vec, detected_perms = extract_vector(filename)
        if vec is None:
            raise HTTPException(status_code=400, detail="Invalid APK")
        
        prediction = model.predict(vec)
        score = float(prediction[0][0])
        
        status = "SECURE"
        if score > 0.8: status = "MALWARE"
        elif score > 0.3: status = "SUSPICIOUS"

        # Calcul d'un score de confiance basique (distance par rapport au seuil d'incertitude 0.5)
        # Plus on est proche de 0 ou 1, plus on est confiant.
        confidence = abs(score - 0.5) * 2

        return {
            "service": "aiscanner",
            "file": file.filename,
            "risk_score": score,
            "confidence": confidence,
            "status": status,
            "permissions": detected_perms
        }
    finally:
        if os.path.exists(filename):
            os.remove(filename)