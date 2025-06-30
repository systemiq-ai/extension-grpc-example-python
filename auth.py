import os
import logging
from jose import jwt, ExpiredSignatureError, JWTError

PUBLIC_KEY = os.getenv("PUBLIC_KEY")
CLIENT_IDS = [int(x) for x in os.getenv("CLIENT_IDS", "").split(",") if x]
ALGORITHM = "RS256"


def verify_token(token: str):
    """
    Decode and validate JWT; return payload or raise ValueError.
    """
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])

        cid = payload.get("client_id")
        if CLIENT_IDS and cid not in CLIENT_IDS:
            logging.warning("Unauthorized client ID %s", cid)
            raise ValueError("Unauthorized client ID")

        if payload.get("type") != "access":
            raise ValueError("Invalid token type")

        if "client_super" not in payload.get("scopes", []):
            raise ValueError("Insufficient token scopes")

        return payload

    except ExpiredSignatureError:
        raise ValueError("Access token has expired")
    except JWTError:
        raise ValueError("Invalid token")
    except Exception as exc:
        logging.error("Verification error: %s", exc)
        raise ValueError("Token verification failed") from exc