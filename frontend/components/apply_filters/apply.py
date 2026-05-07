from frontend.utils.utils import utils
from nicegui import app


def get_context_filters():
    context = app.storage.user.get('context')
    return {
        'company_id': context.get('company_id'),
    }

def get_page_filters(page_key):
    page = app.storage.user.get('pages', {})
    return page.get(page_key)

