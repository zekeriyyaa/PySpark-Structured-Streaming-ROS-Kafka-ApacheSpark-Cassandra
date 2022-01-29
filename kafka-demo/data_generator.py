import random
import string

user_ids = list(range(1,101))
recipient_ids = list(range(1,101))

def generate_message()->dict:
    random_user_id = random.choice(user_ids)

    recipient_ids_copy = recipient_ids.copy()

    #recipient_ids.remove(random_user_id)
    random_recepient_id = random.choice(recipient_ids_copy)

    message = "".join(random.choice(string.ascii_letters) for i in range(32))

    return {
        "user_id":random_user_id,
        "recipient_id":random_recepient_id,
        "message":message
    }