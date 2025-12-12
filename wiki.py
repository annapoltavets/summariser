import wikipediaapi

from ai_summarizer import AISummarizer


def get_guest_info(guest_name: str) -> str:
    user_agent = "YourAppName/1.0 (Contact: apoltavets1@gmail.com)"
    wiki_ua = wikipediaapi.Wikipedia(language='uk', user_agent=user_agent)
    wiki_ru = wikipediaapi.Wikipedia(language='ru', user_agent=user_agent)
    page = wiki_ua.page(guest_name) or wiki_ru.page(guest_name)

    if page.exists():
        res = AISummarizer().summarize(sys_pmt = "Сфрмулюй хто ця людина в одному реченні, кратко але з пікантною подробицею життя, якщо вона є", prompt = page.summary)
        return f"({res})"
    else:
        return ""