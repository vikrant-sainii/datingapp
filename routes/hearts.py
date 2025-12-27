from models import AppState
from sqlalchemy.orm import Session
from database import get_db
from fastapi import APIRouter, Depends
from database import get_db
import copy
from sqlalchemy.orm.attributes import flag_modified


def load_data(db: Session):
    record = db.query(AppState).first()
    if not record:
        record = AppState(hearts={"sent": {}, "received": {}, "mutual": {}})
        db.add(record)
        db.commit()
        db.refresh(record)
    return record.hearts, record

def save_data(db: Session, data, record):
    record.hearts = data
    flag_modified(record, "hearts")
    db.commit()
    db.refresh(record)
def can_we_send_heart(data, senderId, receiverId):
    # 1️⃣ If mutual already exists
    if receiverId in data["mutual"].get(senderId, []):
        return False, "Already matched 💞"

    # 2️⃣ If pending request already exists
    for h in data["sent"].get(senderId, []):
        if h["receiverId"] == receiverId and h["ispending"]:
            return False, "Pending request already exists ⏳"

    # 3️⃣ If there’s a pending request from the other side (you should accept, not send)
    for h in data["sent"].get(receiverId, []):
        if h["receiverId"] == senderId and h["ispending"]:
            return False, "They already sent you a request. Accept it instead ❤️"

    return True, "Allowed"



router = APIRouter(prefix="/hearts", tags=["Hearts"])

# ---------------------------------------------------------
# 🔹 ADD HEART  (Equivalent to addHeart() in Flutter)
# ---------------------------------------------------------
@router.post("/send")
def add_heart(senderId: str, receiverId: str, db: Session = Depends(get_db)):
    data, record = load_data(db)

    # init buckets
    data["sent"].setdefault(senderId, [])
    data["received"].setdefault(receiverId, [])
    data["mutual"].setdefault(senderId, [])
    data["mutual"].setdefault(receiverId, [])

    # 🚫 Check if sending is allowed
    allowed, msg = can_we_send_heart(data, senderId, receiverId)
    if not allowed:
        return {"error": msg}

    # check duplicate pending
    for h in data["sent"][senderId]:
        if h["receiverId"] == receiverId and h["ispending"]:
            return {"message": "Already sent ❤️"}

    from datetime import datetime
    heart_obj = {
        "senderId": senderId,
        "receiverId": receiverId,
        "ispending": True,
        "sentAt": datetime.utcnow().isoformat()
    }

    data["sent"][senderId].append(heart_obj)
    data["received"][receiverId].append(copy.deepcopy(heart_obj))

    # 💞 check mutual
    reverse = any(h["receiverId"] == senderId for h in data["sent"].get(receiverId, []))
    if reverse:
        # remove pending on both sides
        data["sent"][senderId] = [h for h in data["sent"][senderId] if h["receiverId"] != receiverId]
        data["sent"][receiverId] = [h for h in data["sent"][receiverId] if h["receiverId"] != senderId]
        data["received"][senderId] = [h for h in data["received"][senderId] if h["senderId"] != receiverId]
        data["received"][receiverId] = [h for h in data["received"][receiverId] if h["senderId"] != senderId]

        # add mutual pair
        if receiverId not in data["mutual"][senderId]:
            data["mutual"][senderId].append(receiverId)
        if senderId not in data["mutual"][receiverId]:
            data["mutual"][receiverId].append(senderId)

        save_data(db, data, record)
        return {"message": "💞 MATCHED!!", "mutual": True}

    save_data(db, data, record)
    return {"message": "Heart sent ❤️", "mutual": False}



# ---------------------------------------------------------
# 🔹 REMOVE HEART  (Equivalent to removeHeart())
# ---------------------------------------------------------
@router.delete("/remove")
def remove_heart(senderId: str, receiverId: str, db: Session = Depends(get_db)):
    data, record = load_data(db)

    # Remove from SENT list
    if senderId in data["sent"]:
        data["sent"][senderId] = [
            h for h in data["sent"][senderId]
            if h["receiverId"] != receiverId
        ]

    # Remove from RECEIVED list
    if receiverId in data["received"]:
        data["received"][receiverId] = [
            h for h in data["received"][receiverId]
            if h["senderId"] != senderId
        ]

    save_data(db, data, record)
    return {"message": "Heart removed ❌"}

# ---------------------------------------------------------
# 🔹 ADD MUTUAL (Separate, clean logic)
# ---------------------------------------------------------
@router.post("/mutual")
def add_mutual(userA: str, userB: str, db: Session = Depends(get_db)):
    data, record = load_data(db)

    data["mutual"].setdefault(userA, [])
    data["mutual"].setdefault(userB, [])

    # Add both sides (like Flutter mutual[user].add)
    if userB not in data["mutual"][userA]:
        data["mutual"][userA].append(userB)
    if userA not in data["mutual"][userB]:
        data["mutual"][userB].append(userA)

    save_data(db, data, record)
    return {"message": "Match saved 💞", "pair": [userA, userB]}

# ---------------------------------------------------------
# 🔹 FETCH LISTS  (Equivalent to getSentList/getReceivedList/getMutualList)
# ---------------------------------------------------------
@router.get("/{userId}/sent")
def get_sent_list(userId: str, db: Session = Depends(get_db)):
    data, _ = load_data(db)
    return {"sent": data["sent"].get(userId, [])}

@router.get("/{userId}/received")
def get_received_list(userId: str, db: Session = Depends(get_db)):
    data, _ = load_data(db)
    return {"received": data["received"].get(userId, [])}

@router.get("/{userId}/mutual")
def get_mutual_list(userId: str, db: Session = Depends(get_db)):
    data, _ = load_data(db)
    return {"mutual": data["mutual"].get(userId, [])}
