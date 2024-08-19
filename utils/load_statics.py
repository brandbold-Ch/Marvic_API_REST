from route_resolver import get_template_path


def load_admin_appt_tmpl(
        appt_id: str,
        issue: str,
        created_at: str,
        timestamp: str,
) -> str:
    html_chunk: str = ""

    with open(
            get_template_path("admin_appt_tmpl.html"),
            "r", encoding="utf-8"
    ) as html:
        tags_list = []

        for tag in html.readlines():
            tag = tag.strip().replace("{id}", appt_id)
            tag = tag.strip().replace("{issue}", issue)
            tag = tag.strip().replace("{created_at}", created_at)
            tag = tag.strip().replace("{timestamp}", timestamp)
            tags_list.append(tag)
        html_chunk = html_chunk.join(tags_list)
    return html_chunk
