import os

def export_vars(request):
    data = {}
    data['PAGE_NAME'] = os.environ.get("PAGE_NAME", "Baza partii szachowych")
    return data