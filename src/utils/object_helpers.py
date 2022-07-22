from flask import request


def partial_update_object(object_to_update, new_info_dict, ignore_keys=[], user=None):
    for key in new_info_dict:
        # Do not update any fields in ignore_keys
        if key in ignore_keys:
            continue

        if hasattr(object_to_update, key) and new_info_dict.get(key) != getattr(
            object_to_update, key
        ):
            setattr(object_to_update, key, new_info_dict.get(key))

    # Check if the object is really change. If it is, then update the "updated_by" if the object has that field
    if len(db.session.dirty._members) > 0 and hasattr(object_to_update, "updated_by"):
        if user is None:
            user = request.user.user_id
        object_to_update.updated_by = user
        flag_modified(object_to_update, "updated_by")

    return object_to_update