from errors.exception_classes import ServerUnknownError


def load_admin_appt_tmpl(**kwargs) -> str:
    try:
        html_chunk: str = ""

        with open(
                "static/html/admin_appt_tmpl.html",
                "r", encoding="utf-8"
        ) as html:
            tags_list = []

            for tag in html.readlines():
                tag = tag.strip().replace("{id}", str(kwargs.get("appt_id")))
                tag = tag.strip().replace("{issue}", str(kwargs.get("issue")))
                tag = tag.strip().replace("{created_at}", str(kwargs.get("created_at")))
                tag = tag.strip().replace("{timestamp}", str(kwargs.get("timestamp")))
                tag = tag.strip().replace("{price}", str(kwargs.get("price")))
                tags_list.append(tag)
            html_chunk = html_chunk.join(tags_list)
        return html_chunk

    except Exception as e:
        raise ServerUnknownError(detail=e) from e


def load_reminder_appt_tmpl(**kwargs) -> str:
    try:
        html_chunk: str = ""

        with open(
            "static/html/reminder_appt_tmpl.html",
            "r", encoding="utf-8"
        ) as html:
            tags_list = []

            for tag in html.readlines():
                tag = tag.strip().replace("{price}", str(kwargs.get("price")))
                tag = tag.strip().replace("{user_name}", str(kwargs.get("user")))
                tag = tag.strip().replace("{pet_name}", str(kwargs.get("pet")))
                tag = tag.strip().replace("{issue}", str(kwargs.get("issue")))
                tag = tag.strip().replace("{timestamp}", str(kwargs.get("timestamp")))
                tag = tag.strip().replace("{created_at}", str(kwargs.get("created_at")))
                tags_list.append(tag)
            html_chunk = html_chunk.join(tags_list)
        return html_chunk

    except Exception as e:
        raise ServerUnknownError(detail=e) from e
